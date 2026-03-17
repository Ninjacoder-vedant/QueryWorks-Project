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

class AuthRequest(BaseModel):
    code: str

# -------------------------------------------------------------------
# 1. LOGIN ROUTE: Validates with Google & Creates the JWT
# -------------------------------------------------------------------
@app.post("/login")
async def google_auth(request: AuthRequest):
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




@app.get("/")
def root():
    return {"Message": "Successful Welcome to RideShare Portal"}