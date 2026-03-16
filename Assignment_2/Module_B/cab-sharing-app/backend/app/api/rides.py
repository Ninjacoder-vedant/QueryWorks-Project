from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
import models, schemas, database  # Absolute imports

router = APIRouter(
    prefix="/rides",
    tags=["Rides Management"]
)

@router.get("/", response_model=list[schemas.RideOut])
def read_rides(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return db.query(models.ActiveRide).offset(skip).limit(limit).all()

# ... other ride endpoints