from fastapi import FastAPI
from api import rides # requests  # Import from the api folder

app = FastAPI(title="IITGN RideShare Portal")

# Include routers
app.include_router(rides.router)
# app.include_router(requests.router)

@app.get("/")
def root():
    return {"Message": "Successful Welcome to RideShare Portal"}