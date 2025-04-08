from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import requests


app = FastAPI(title="Weather Rest API")

# CORS handling
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/{location}")
def get_weather(request: Request, location: str):
    try:
        req = requests.get(f"https://api.weather.gov/points/{location}")
        res = req.json()

        if res.get("status"):
            raise HTTPException(status_code=500, detail=res.get("detail"))
            
        return res
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/requests")
def get_recent_requests(limit: int = 10):
    return []