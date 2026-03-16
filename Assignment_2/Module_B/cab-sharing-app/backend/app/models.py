from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Numeric, Boolean, Date, Time, CheckConstraint
from sqlalchemy.orm import relationship
import database
Base = database.Base

class Member(Base):
    __tablename__ = "Members"
    MemberID = Column(Integer, primary_key=True, autoincrement=True)
    FullName = Column(String(100), nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    Programme = Column(String(50), nullable=False)
    Branch = Column(String(50))
    BatchYear = Column(Integer, nullable=False)  # MySQL YEAR translates well to Integer
    ContactNumber = Column(String(15), unique=True, nullable=False)
    Age = Column(Integer)
    Gender = Column(String(1))

# In backend/app/models.py
class ActiveRide(Base):
    __tablename__ = "ActiveRides"
    # Match the varchar(50) from your DDL
    RideID = Column(String(50), primary_key=True) 
    AdminID = Column(Integer, ForeignKey("Members.MemberID"))
    AvailableSeats = Column(Integer, nullable=False)
    PassengerCount = Column(Integer, nullable=False)
    Source = Column(String(100), nullable=False)
    Destination = Column(String(100), nullable=False)
    VehicleType = Column(String(30), nullable=False)
    StartTime = Column(DateTime, nullable=False)
    EstimatedTime = Column(Integer, nullable=False)
    FemaleOnly = Column(Boolean, default=False)

    __table_args__ = (
        CheckConstraint('AvailableSeats >= 0', name='ActiveRides_chk_1'),
        CheckConstraint('PassengerCount >= 1', name='ActiveRides_chk_2'),
    )

class BookingRequest(Base):
    __tablename__ = "BookingRequests"
    RequestID = Column(Integer, primary_key=True, autoincrement=True)
    RideID = Column(String(50), ForeignKey("ActiveRides.RideID", ondelete="CASCADE"), nullable=False)
    PassengerID = Column(Integer, ForeignKey("Members.MemberID", ondelete="CASCADE"), nullable=False)
    RequestStatus = Column(String(20), nullable=False, default='PENDING')
    RequestedAt = Column(DateTime, nullable=False)