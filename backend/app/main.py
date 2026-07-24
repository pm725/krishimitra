# backend/app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from typing import Optional, List
from datetime import datetime
import pandas as pd
import numpy as np

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title="KrishiMitra API",
    description="🌾 AI-Powered Agricultural Advisory System for Nepal",
    version="1.0.0"
)

# --- Models ---
class LocationRequest(BaseModel):
    lat: float
    lon: float
    district: str

class FarmerRegister(BaseModel):
    phone: str
    name: str
    district: str
    village: str
    crop_type: str
    language: str = "ne"

# --- In-memory storage ---
farmers_db = []
advisories_db = []

# --- Root Endpoint ---
@app.get("/")
async def root():
    return {
        "message": "🌾 KrishiMitra API is running!",
        "version": "1.0.0",
        "status": "online",
        "farmers_registered": len(farmers_db),
        "endpoints": {
            "GET /": "This help message",
            "GET /health": "Health check",
            "GET /api/farmers/list": "List all farmers",
            "POST /api/weather/current": "Get current weather",
            "POST /api/weather/forecast": "Get weather forecast",
            "POST /api/advisory/generate": "Generate farming advice",
            "POST /api/farmers/register": "Register a farmer"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "KrishiMitra Backend",
        "timestamp": datetime.now().isoformat(),
        "python_version": "3.14.6"
    }

# --- Weather Endpoint ---
@app.post("/api/weather/current")
async def get_current_weather(location: LocationRequest):
    """Get current weather for a district"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    # If no API key, return simulated data
    if not api_key:
        return {
            "district": location.district,
            "temperature": 25.5,
            "humidity": 65,
            "rainfall": 2.3,
            "weather": "Partly cloudy",
            "wind_speed": 12.5,
            "timestamp": datetime.now().isoformat(),
            "note": "Using simulated data. Add OPENWEATHER_API_KEY to .env for real data."
        }
    
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": location.lat,
            "lon": location.lon,
            "appid": api_key,
            "units": "metric"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return {
            "district": location.district,
            "temperature": data['main']['temp'],
            "humidity": data['main']['humidity'],
            "rainfall": data.get('rain', {}).get('1h', 0),
            "weather": data['weather'][0]['description'],
            "wind_speed": data['wind']['speed'],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weather API error: {str(e)}")

# --- Advisory Endpoint ---
@app.post("/api/advisory/generate")
async def generate_advisory(location: LocationRequest, crop_type: str = "rice"):
    """Generate farming advisory based on weather"""
    # Get weather
    weather = await get_current_weather(location)
    
    advice = []
    severity = "normal"
    
    # Temperature rules
    if weather['temperature'] > 35:
        advice.append("☀️ HIGH TEMPERATURE WARNING: Irrigate crops in early morning or evening.")
        severity = "warning"
    elif weather['temperature'] > 30:
        advice.append("🌤️ Warm conditions. Ensure adequate water supply.")
    elif weather['temperature'] < 5:
        advice.append("❄️ FROST ALERT! Cover seedlings with plastic or straw.")
        severity = "warning"
    elif weather['temperature'] < 10:
        advice.append("❄️ Cold weather. Protect young plants from frost.")
    
    # Rainfall rules
    if weather['rainfall'] > 50:
        advice.append("🌧️ HEAVY RAIN WARNING! Ensure proper drainage.")
        severity = "warning"
    elif weather['rainfall'] > 20:
        advice.append("🌧️ Good rainfall. Ideal for sowing and transplanting.")
    elif weather['rainfall'] < 5:
        advice.append("💧 Low rainfall. Consider irrigating.")
    
    # Crop-specific advice
    crop_advice = {
        "rice": [
            "🌾 Rice: Maintain 5-10cm water level in fields.",
            "Apply nitrogen fertilizer 2 weeks after transplanting."
        ],
        "potato": [
            "🥔 Potato: Prepare well-drained, loose soil.",
            "Plant when soil temperature is 10-15°C."
        ],
        "maize": [
            "🌽 Maize: Plant seeds 5cm deep with 75cm row spacing.",
            "Apply compost before planting."
        ],
        "wheat": [
            "🌾 Wheat: Sow in well-drained soil.",
            "Apply phosphorus fertilizer at planting."
        ]
    }
    
    crop_lower = crop_type.lower()
    if crop_lower in crop_advice:
        advice.extend(crop_advice[crop_lower][:2])
    
    advice.append("📱 Contact your local agriculture extension officer for personalized advice.")
    
    # Save advisory
    advisory_data = {
        "district": location.district,
        "crop_type": crop_type,
        "weather": weather,
        "advice": advice,
        "severity": severity,
        "created_at": datetime.now().isoformat()
    }
    advisories_db.append(advisory_data)
    
    return {
        "district": location.district,
        "crop_type": crop_type,
        "current_weather": weather,
        "advice": advice,
        "severity": severity,
        "timestamp": datetime.now().isoformat()
    }

# --- Farmer Registration ---
@app.post("/api/farmers/register")
async def register_farmer(farmer: FarmerRegister):
    """Register a new farmer"""
    for f in farmers_db:
        if f['phone'] == farmer.phone:
            return {"message": "⚠️ Farmer already registered", "farmer": f}
    
    farmer_data = farmer.dict()
    farmer_data['registered_at'] = datetime.now().isoformat()
    farmers_db.append(farmer_data)
    
    return {
        "message": "✅ Farmer registered successfully!",
        "farmer": farmer_data,
        "total_farmers": len(farmers_db)
    }

@app.get("/api/farmers/list")
async def list_farmers():
    """List all registered farmers"""
    return {
        "total": len(farmers_db),
        "farmers": farmers_db
    }

# --- Run Server ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)