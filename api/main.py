from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from pydantic import SecretStr
from .database import engine
from sqlmodel import Session, select
from .database import get_session
from .models import User, Booking, vet
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi import BackgroundTasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
    print("shutting down")

app = FastAPI(lifespan=lifespan)
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
    doctor: str = Form(...),
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
    vet_id = session.exec(select(vet).where(vet.position==doctor)).first()
    if not vet_id:
        raise HTTPException(status_code=409, detail="Vet doesnt't exist")
    booking = Booking(user_id=user.id, appointment_date=appointment_date, reason=reason, vet_id=vet_id.id)
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

    return {"message": "Booking sucessful",
            "booking_id": booking.id,
            "doctor": f"{vet_id.first_name} {vet_id.last_name}",
            "reason": booking.reason
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
    position: str,
    session: Session=Depends(get_session)
):
    add = vet(first_name=first_name, last_name=last_name,position=
              position)
    session.add(add)
    session.commit()
    return {"message": "added"}
    
@app.get("/vets")
async def get_vets(
    session: Session=Depends(get_session)
):
    vets = session.exec(select(vet)).all()
    return {
    "vets": [vet.position for vet in vets]
    }