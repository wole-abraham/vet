from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class vet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    position: str
 
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
    appointment_date: datetime
    reason: Optional[str] = None