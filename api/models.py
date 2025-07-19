from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

# Define service choices as constants
SERVICE_CHOICES = [
    "Vaccination",
    "Physiotherapy", 
    "Dermatology",
    "Operation",
    "General Checkup",
    "Dental Care"
]

PET_TYPE_CHOICES = [
    "dog",
    "cat", 
    "bird",
    "reptile"
]

STATUS_CHOICES = [
    "scheduled",
    "completed", 
    "cancelled"
]

class Vet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    specialization: str = Field(description="Vet specialization")
    is_available: bool = Field(default=True)
 
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str = Field(index=True, unique=True)
    phone_number: str

class Booking(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    vet_id: int = Field(foreign_key="vet.id")
    service_type: str = Field(description="Type of service requested")
    pet_type: str = Field(description="Type of pet")
    appointment_date: datetime
    reason: Optional[str] = None
    status: str = Field(default="scheduled", description="Booking status")