"""
Live Weather Prediction Endpoints
Add these endpoints to your main.py
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from weather_api import WeatherAPIClient

# Create router for live weather endpoints
weather_router = APIRouter(prefix="/live", tags=["Live Weather"])

# Initialize weather client (will be set on startup)
weather_client = None


class LivePredictionRequest(BaseModel):
    """Request for live weather-based prediction"""
    
    city: str = Field(..., description="City name (e.g., 'Lucknow')")
    country_code: str = Field("IN", description="Country code (default: IN)")
    
    class Config:
        schema_extra = {
            "example": {
                "city": "Lucknow",
                "country_code": "IN"
            }
        }


class LivePredictionResponse(BaseModel):
    """Response for live prediction"""
    
    success: bool
    city: str
    weather_data: dict
    features: dict
    alert: dict
    prediction: dict
    risk_score: dict
    processing_time_ms: float


@weather_router.on_event("startup")
async def init_weather_client():
    """Initialize weather client on startup"""
    global weather_client
    weather_client = WeatherAPIClient()


@weather_router.post("/predict-city", response_model=LivePredictionResponse)
async def predict_from_city(request: LivePredictionRequest):
    """
    Predict flood risk using live weather data for a city
    
    Fetches current weather from OpenWeatherMap and makes prediction
    """
    import time
    start_time = time.time()
    
    try:
        if weather_client is None:
            raise HTTPException(
                status_code=503,
                detail="Weather API client not initialized"
            )
        
        # Fetch live weather data
        weather_data = weather_client.get_current_weather(
            request.city,
            request.country_code
        )
        
        # Transform to model features
        features = weather_client.transform_to_features(
            weather_data,
            request.city
        )
        
        # Make prediction using the assessor
        from flood_assessment import FloodRiskAssessor
        assessor = FloodRiskAssessor()
        
        assessment = assessor.assess_flood_risk(
            features,
            location=request.city,
            include_detailed_conditions=True
        )
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        return LivePredictionResponse(
            success=True,
            city=request.city,
            weather_data=weather_data,
            features=features,
            alert=assessment,
            prediction=assessment['prediction'],
            risk_score=assessment['risk_score'],
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Live prediction failed: {str(e)}"
        )


@weather_router.get("/weather/{city}")
async def get_weather(city: str, country_code: str = "IN"):
    """
    Get current weather for a city
    
    Returns raw weather data from OpenWeatherMap
    """
    try:
        if weather_client is None:
            raise HTTPException(
                status_code=503,
                detail="Weather API client not initialized"
            )
        
        weather_data = weather_client.get_current_weather(city, country_code)
        
        return {
            "success": True,
            "city": city,
            "data": weather_data
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Weather fetch failed: {str(e)}"
        )


@weather_router.post("/transform-weather")
async def transform_weather(city: str, country_code: str = "IN"):
    """
    Get weather data and transform to model features
    
    Useful for debugging feature transformation
    """
    try:
        if weather_client is None:
            raise HTTPException(
                status_code=503,
                detail="Weather API client not initialized"
            )
        
        # Get weather
        weather_data = weather_client.get_current_weather(city, country_code)
        
        # Transform
        features = weather_client.transform_to_features(weather_data, city)
        
        return {
            "success": True,
            "city": city,
            "weather": weather_data,
            "features": features
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Transform failed: {str(e)}"
        )


# Instructions to add to main.py:
"""
To integrate live weather endpoints, add to your main.py:

1. Import the router:
   from weather_endpoints import weather_router, init_weather_client

2. Include the router in your app:
   app.include_router(weather_router)

3. Initialize weather client on startup:
   @app.on_event("startup")
   async def startup_event():
       # ... existing code ...
       init_weather_client()

New endpoints will be available at:
- POST /live/predict-city
- GET /live/weather/{city}
- POST /live/transform-weather
"""