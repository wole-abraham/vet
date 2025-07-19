from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from pydantic import SecretStr
from .database import engine
from sqlmodel import Session, select
from .database import get_session
from .models import User, Booking, Vet, SERVICE_CHOICES, PET_TYPE_CHOICES
from datetime import datetime, timedelta, date
from fastapi.middleware.cors import CORSMiddleware
from fastapi import BackgroundTasks
from typing import List
import json


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
    print("shutting down")

app = FastAPI(lifespan=lifespan,root_path="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


conf = ConnectionConfig(
    MAIL_USERNAME = "testprojectmail755@gmail.com",
    MAIL_PASSWORD=SecretStr('ovzjsfnshxxunmuj'),
    MAIL_FROM="testprojectmail755@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=True,
    USE_CREDENTIALS=True

 )

@app.post("/book/")
async def root(
    background_tasks: BackgroundTasks,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    appointment_date: datetime = Form(...),
    image: UploadFile = File(...),
    phone_number: str = Form(...),
    reason: str = Form(...),
    service_type: str = Form(...),  # Changed from doctor to service_type
    pet_type: str = Form(...),      # Added pet_type
    session: Session = Depends(get_session) 
):
    print(appointment_date)
    user = session.exec(select(User).where(User.email==email)).first()
    if not user:
        user = User(first_name=first_name, last_name=
                    last_name, email=email, phone_number=phone_number)
        session.add(user)
        session.commit()
        session.refresh(user)

    existing = session.exec(select(Booking).where(
        Booking.appointment_date == appointment_date
    )).first()
    if existing:
        raise HTTPException(status_code=409, detail="This time slot has already been booked")
    
    # Find vet by specialization (service type)
    vet_id = session.exec(select(Vet).where(Vet.specialization==service_type)).first()
    if not vet_id:
        raise HTTPException(status_code=409, detail=f"No vet available for {service_type} service")
    
    booking = Booking(
        user_id=user.id, 
        appointment_date=appointment_date, 
        reason=reason, 
        vet_id=vet_id.id,
        service_type=service_type,
        pet_type=pet_type
    )
    session.add(booking)
    session.commit()
    from .messages import messages

    message = MessageSchema(
        subject="Booking Confirmation",
        recipients=[user.email],
        body=messages(booking.appointment_date, user.last_name),
        subtype=MessageType.html
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)

    return {"message": "Booking successful",
            "booking_id": booking.id,
            "vet": f"{vet_id.first_name} {vet_id.last_name}",
            "service": booking.service_type,
            "pet_type": booking.pet_type
    }
    
@app.get("/bookings/")
async def bookings(
    email: str,
    session: Session = Depends(get_session)
    ):
    user = session.exec(select(User).where(User.email==email)).first()
    booking = session.exec(select(Booking).where(Booking.user_id==user.id)).first()
    if not booking:
        raise HTTPException(status_code=409, detail='User not found')
    return {
        "user": booking.reason
    }
@app.post("/vet/")
async def add_vet(
    first_name: str,
    last_name: str,
    specialization: str,  # Changed from position to specialization
    session: Session=Depends(get_session)
):
    add = Vet(first_name=first_name, last_name=last_name, specialization=specialization)
    session.add(add)
    session.commit()
    return {"message": "added"}
    
@app.get("/vets")
async def get_vets(
    session: Session=Depends(get_session)
):
    vets = session.exec(select(Vet)).all()
    return {
    "vets": [vet.specialization for vet in vets]
    }

@app.get("/services")
async def get_services():
    """Get all available services"""
    return {
        "services": SERVICE_CHOICES,
        "pet_types": PET_TYPE_CHOICES
    }

@app.get("/available-slots/")
async def get_available_slots(
    selected_date: str,
    session: Session = Depends(get_session)
):
    """
    Get available time slots for a given date.
    Returns booked times so frontend can disable them.
    """
    try:
        # Parse the date
        target_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
        
        # Define business hours (9 AM to 5 PM, 1-hour intervals)
        start_time = datetime.combine(target_date, datetime.min.time().replace(hour=9))
        end_time = datetime.combine(target_date, datetime.min.time().replace(hour=17))
        
        # Generate all possible time slots
        time_slots = []
        current_time = start_time
        while current_time < end_time:
            time_slots.append(current_time)
            current_time += timedelta(hours=1)
        
        # Get booked appointments for this date
        booked_appointments = session.exec(
            select(Booking).where(
                Booking.appointment_date >= start_time,
                Booking.appointment_date < end_time
            )
        ).all()
        
        # Extract booked times
        booked_times = [appointment.appointment_date for appointment in booked_appointments]
        
        # Filter out booked times from available slots
        available_slots = []
        for slot in time_slots:
            # Check if this slot is booked
            is_booked = any(
                abs((slot - booked_time).total_seconds()) < 900  # 15 minutes = 900 seconds
                for booked_time in booked_times
            )
            
            if not is_booked:
                available_slots.append(slot.strftime("%Y-%m-%d %H:%M"))
        
        return {
            "date": selected_date,
            "available_slots": available_slots,
            "booked_times": [time.strftime("%Y-%m-%d %H:%M") for time in booked_times],
            "business_hours": {
                "start": "09:00",
                "end": "17:00"
            }
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting available slots: {str(e)}")

@app.get("/availability-calendar/")
async def get_availability_calendar(
    start_date: str,
    end_date: str | None = None,
    session: Session = Depends(get_session)
):
    """
    Get availability summary for multiple days.
    Useful for showing calendar view with availability indicators.
    """
    try:
        # Parse start date
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        
        # If no end date provided, default to 7 days from start
        if end_date:
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
        else:
            end = start + timedelta(days=7)
        
        # Ensure end date is not more than 30 days from start
        if (end - start).days > 30:
            end = start + timedelta(days=30)
        
        calendar_data = []
        current_date = start
        
        while current_date <= end:
            # Skip weekends (Saturday = 5, Sunday = 6)
            if current_date.weekday() < 5:  # Monday to Friday
                # Get availability for this date
                date_str = current_date.strftime("%Y-%m-%d")
                start_time = datetime.combine(current_date, datetime.min.time().replace(hour=9))
                end_time = datetime.combine(current_date, datetime.min.time().replace(hour=17))
                
                # Generate time slots for this date
                time_slots = []
                current_time = start_time
                while current_time < end_time:
                    time_slots.append(current_time)
                    current_time += timedelta(hours=1)
                
                # Get booked appointments for this date
                booked_appointments = session.exec(
                    select(Booking).where(
                        Booking.appointment_date >= start_time,
                        Booking.appointment_date < end_time
                    )
                ).all()
                
                # Calculate availability percentage
                total_slots = 8  # 9 AM to 5 PM = 8 hours = 8 slots (1-hour intervals)
                booked_count = len(booked_appointments)
                available_count = total_slots - booked_count
                availability_percentage = (available_count / total_slots) * 100
                
                # Determine availability status
                if availability_percentage >= 70:
                    status = "high"
                elif availability_percentage >= 30:
                    status = "medium"
                else:
                    status = "low"
                
                calendar_data.append({
                    "date": date_str,
                    "available_slots": available_count,
                    "total_slots": total_slots,
                    "booked_slots": booked_count,
                    "availability_percentage": round(availability_percentage, 1),
                    "status": status,
                    "day_name": current_date.strftime("%A"),
                    "is_available": available_count > 0
                })
            else:
                # Weekend - no availability
                calendar_data.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "available_slots": 0,
                    "total_slots": 0,
                    "booked_slots": 0,
                    "availability_percentage": 0,
                    "status": "closed",
                    "day_name": current_date.strftime("%A"),
                    "is_available": False
                })
            
            current_date += timedelta(days=1)
        
        return {
            "start_date": start_date,
            "end_date": end.strftime("%Y-%m-%d"),
            "calendar": calendar_data,
            "business_hours": {
                "start": "09:00",
                "end": "17:00"
            },
            "note": "Weekends are closed. Emergency care available 24/7."
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting calendar: {str(e)}")