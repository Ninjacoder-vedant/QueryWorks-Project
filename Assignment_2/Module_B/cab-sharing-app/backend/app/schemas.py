from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RideBase(BaseModel):
    Source: str
    Destination: str
    StartTime: datetime
    AvailableSeats: int
    VehicleType: str
    FemaleOnly: bool = False

class RideCreate(RideBase):
    AdminID: int
    PassengerCount: int
    EstimatedTime: int

class RideOut(RideBase):
    RideID: str
    AdminID: int
    
    class Config:
        from_attributes = True