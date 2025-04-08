from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
from motor.motor_asyncio import AsyncIOMotorClient
import os
import datetime


app = FastAPI(title="Weather Rest API")

# CORS handling
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup MongoDB Connection with authentication
try:
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL", "localhost:27017"), 
                                                    username=os.getenv("MONGODB_USERNAME", "root"), 
                                                    password=os.getenv("MONGODB_PASSWORD", "example"))
    db = client[os.getenv("MONGODB_DB", "weather_db")]
except Exception as e:
    print(f"Failed to connect to MongoDB: {str(e)}")
    raise HTTPException(status_code=500, detail=str(e))


@app.get("/{location}")
async def get_weather(request: Request, location: str):
    try:
        # Get weather data from NWS API
        weather_req = requests.get(f"https://api.weather.gov/points/{location}")
        weather_res = weather_req.json()

        # Log request to MongoDB
        await db.requests.insert_one({
            "location": str(location),
            "timestamp": str(datetime.datetime.utcnow()),
            "headers": {str(k): str(v) for k, v in request.headers.items()},
            "weather_res": weather_res
        })

        if weather_res.get("status"):
            raise HTTPException(status_code=500, detail=weather_res.get("detail"))
            
        return weather_res
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/requests/{limit}")
async def get_recent_requests(limit: int = 10):
    try:
        cursor = db.requests.find().sort("timestamp", -1).limit(limit)
        requests = await cursor.to_list(length=limit)

        for req in requests:
            req["_id"] = str(req["_id"])
        
        return {"requests": requests}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

