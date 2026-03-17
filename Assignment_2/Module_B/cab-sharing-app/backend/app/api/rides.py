from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from google.oauth2 import id_token
from google.auth.transport import requests
from . import auth
import models, schemas, database  

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from api import rides 
from pydantic import BaseModel
import httpx
import os
import jwt # Added import
from datetime import datetime, timedelta # Added imports
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="IITGN RideShare Portal")

# Add the CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rides.router)

# Use your .env variables
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI", "postmessage")
JWT_SECRET = os.environ.get("JWT_SECRET_KEY") # Load the new secret
ALGORITHM = "HS256"

router = APIRouter(
    prefix="/rides",
    tags=["Rides Management"]
)

from sqlalchemy.orm import joinedload

@router.get("/active-rides", response_model=list[schemas.RideFull])
def get_active_rides(db: Session = Depends(database.get_db)):

    rides = db.query(models.ActiveRide).options(
        joinedload(models.ActiveRide.passengers)
        .joinedload(models.RidePassengerMap.member),
        joinedload(models.ActiveRide.admin)  
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
            "AdminName": r.admin.FullName if r.admin else None, 
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



@router.get("/your-rides", response_model=list[schemas.RideFull])
def get_your_rides(
    member_id: int = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):

    rides = db.query(models.ActiveRide).options(
        joinedload(models.ActiveRide.passengers)
        .joinedload(models.RidePassengerMap.member),
        joinedload(models.ActiveRide.admin)
    ).filter(
        (models.ActiveRide.AdminID == member_id) |
        (models.ActiveRide.passengers.any(
            models.RidePassengerMap.PassengerID == member_id
        ))
    ).all()

    res = []

    for r in rides:
        passengers = [
            {"MemberID": p.member.MemberID, "FullName": p.member.FullName}
            for p in r.passengers if p.member
        ]

        res.append({
            "RideID": r.RideID,
            "AdminID": r.AdminID,
            "AdminName": r.admin.FullName if r.admin else None,
            "AvailableSeats": r.AvailableSeats,
            "PassengerCount": r.PassengerCount,
            "Source": r.Source,
            "Destination": r.Destination,
            "VehicleType": r.VehicleType,
            "StartTime": r.StartTime,
            "EstimatedTime": r.EstimatedTime,
            "FemaleOnly": r.FemaleOnly,
            "Passengers": passengers
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


@router.post("/create-ride", response_model=schemas.RideOut)
def create_ride(
    ride: schemas.RideCreate,
    member_id: int = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):

    new_ride = models.ActiveRide(
        RideID=str(uuid.uuid4()),
        AdminID=member_id,   
        AvailableSeats=ride.AvailableSeats,
        PassengerCount=1,   
        Source=ride.Source,
        Destination=ride.Destination,
        VehicleType=ride.VehicleType,
        StartTime=ride.StartTime,
        EstimatedTime=ride.EstimatedTime,
        FemaleOnly=ride.FemaleOnly
    )

    db.add(new_ride)
    db.commit()
    db.refresh(new_ride)
    admin = db.query(models.Member).filter(models.Member.MemberID == ride.AdminID).first()

    if not admin:
        raise HTTPException(status_code=400, detail="Invalid AdminID")

    admin_entry = models.RidePassengerMap(
        RideID=new_ride.RideID,
        PassengerID=member_id,
        IsConfirmed=True
    )

    db.add(admin_entry)
    db.commit()

    return new_ride

@router.get("/requests/{ride_id}")
def get_requests_by_ride(ride_id: str, db: Session = Depends(database.get_db)):

    data = db.query(models.BookingRequest, models.Member)\
        .join(models.Member, models.Member.MemberID == models.BookingRequest.PassengerID)\
        .filter(models.BookingRequest.RideID == ride_id)\
        .all()

    res = []

    for req, member in data:
        res.append({
            "RequestID": req.RequestID,
            "RideID": req.RideID,
            "PassengerID": req.PassengerID,
            "PassengerName": member.FullName,
            "RequestStatus": req.RequestStatus,
            "RequestedAt": req.RequestedAt
        })

    return res



class AuthRequest(BaseModel):
    code: str

# -------------------------------------------------------------------
# 1. LOGIN ROUTE: Validates with Google & Creates the JWT
# -------------------------------------------------------------------
@app.post("/login")
async def google_auth(request: AuthRequest,  db: Session = Depends(database.get_db)):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": request.code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        token_data = response.json()
        
    if "error" in token_data:
        raise HTTPException(status_code=400, detail=token_data.get("error_description"))

    user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    async with httpx.AsyncClient() as client:
        user_info_res = await client.get(
            user_info_url, 
            headers={"Authorization": f"Bearer {token_data['access_token']}"}
        )
        user_info = user_info_res.json()

    # --- Domain Check ---
    user_email = user_info.get("email", "")
    if not user_email.endswith("@iitgn.ac.in"):
        raise HTTPException(status_code=403, detail="Access restricted to university students only.")

    # --- Create the Local JWT ---
    expire = datetime.utcnow() + timedelta(hours=24) # Token expires in 24 hours
    payload = {
        "sub": user_info.get("sub"),          
        "name": user_info.get("name"),
        "picture": user_info.get("picture"),
        "exp": expire               
    }
    user = db.query(models.Member).filter(
        models.Member.GoogleSub == payload["sub"]
    ).first()

    if not user:
        return {"message": "User Not Found"}
    # add logic here
    
    
    # Sign the token using your server's secret key
    access_token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)

    # Return the newly minted token to React
    return {"message": "Success", "token": access_token, "user": user_info}


# -------------------------------------------------------------------
# 2. THE GUARD: Dependency to check the token on protected routes
# -------------------------------------------------------------------
def verify_token(authorization: str = Header(None)):
    """
    This function checks the Authorization header for a valid JWT.
    If it's missing, expired, or tampered with, it blocks the request.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authentication token")
    
    # Extract the token string (remove the "Bearer " part)
    token = authorization.split(" ")[1]
    
    try:
        # Decode and verify the token using your secret key
        decoded_payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return decoded_payload # Returns the user data dictionary
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")


"""
@router.post("/auth/google")
def google_login(token: str,):

    try:
        info = id_token.verify_oauth2_token(token, requests.Request())
        gsub = info["sub"]
        email = info["email"]
        name = info["name"]

    except:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    user = db.query(models.Member).filter(
        models.Member.GoogleSub == gsub
    ).first()

    if not user:
        user = models.Member(
            FullName=name,
            Email=email,
            Programme="NA",
            BatchYear=2023,
            ContactNumber="0000000000",
            GoogleSub=gsub
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    jwt_token = auth.create_jwt(user.MemberID)

    return {"access_token": jwt_token}
    """