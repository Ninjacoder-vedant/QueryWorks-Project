from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
import models, schemas, database  # Absolute imports

router = APIRouter(
    prefix="/rides",
    tags=["Rides Management"]
)

from sqlalchemy.orm import joinedload

from sqlalchemy.orm import joinedload

@router.get("/active-rides", response_model=list[schemas.RideFull])
def get_active_rides(db: Session = Depends(database.get_db)):

    rides = db.query(models.ActiveRide).options(
        joinedload(models.ActiveRide.passengers)
        .joinedload(models.RidePassengerMap.member),
        joinedload(models.ActiveRide.admin)   # 👈 NEW
    ).all()

    res = []

    for r in rides:
        members = [
            {"MemberID": p.member.MemberID, "FullName": p.member.FullName}
            for p in r.passengers if p.member
        ]

        res.append({
            "RideID": r.RideID,
            "AdminID": r.AdminID,
            "AdminName": r.admin.FullName if r.admin else None,  # 👈 NEW
            "AvailableSeats": r.AvailableSeats,
            "PassengerCount": r.PassengerCount,
            "Source": r.Source,
            "Destination": r.Destination,
            "VehicleType": r.VehicleType,
            "StartTime": r.StartTime,
            "EstimatedTime": r.EstimatedTime,
            "FemaleOnly": r.FemaleOnly,
            "Passengers": members
        })

    return res

@router.get("/profile/{profile_id}")
def get_profile(profile_id: int, db: Session = Depends(database.get_db)):

    member = db.query(models.Member).filter(
        models.Member.MemberID == profile_id
    ).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    stats = db.query(models.MemberStats).filter(
        models.MemberStats.MemberID == profile_id
    ).first()

    return {
        "MemberID": member.MemberID,
        "FullName": member.FullName,
        "Email": member.Email,
        "Programme": member.Programme,
        "Branch": member.Branch,
        "BatchYear": member.BatchYear,
        "ContactNumber": member.ContactNumber,
        "Age": member.Age,
        "Gender": member.Gender,
        "ProfileImageURL": member.ProfileImageURL,

        "Stats": {
            "AverageRating": float(stats.AverageRating) if stats else 0,
            "TotalRidesTaken": stats.TotalRidesTaken if stats else 0,
            "TotalRidesHosted": stats.TotalRidesHosted if stats else 0,
            "NumberOfRatings": stats.NumberOfRatings if stats else 0,
        }
    }