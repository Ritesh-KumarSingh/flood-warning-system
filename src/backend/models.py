"""
API Models
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional
from datetime import datetime


class FloodFeaturesInput(BaseModel):
    """Input features for flood prediction"""
    
    rainfall_mm: float = Field(
        ..., 
        ge=0, 
        le=500, 
        description="Rainfall in last 24 hours (mm)"
    )
    rainfall_7day_avg: float = Field(
        ..., 
        ge=0, 
        le=300, 
        description="7-day average rainfall (mm)"
    )
    rainfall_intensity: float = Field(
        ..., 
        ge=0, 
        le=50, 
        description="Current rainfall rate (mm/hour)"
    )
    river_level_m: float = Field(
        ..., 
        ge=0, 
        le=15, 
        description="Current river water level (meters)"
    )
    river_level_change: float = Field(
        ..., 
        ge=-2, 
        le=5, 
        description="River level change in last 6 hours (meters)"
    )
    soil_moisture_percent: float = Field(
        ..., 
        ge=0, 
        le=100, 
        description="Soil saturation level (%)"
    )
    elevation_m: float = Field(
        ..., 
        ge=0, 
        le=1000, 
        description="Location elevation above sea level (meters)"
    )
    temperature_celsius: float = Field(
        ..., 
        ge=-10, 
        le=45, 
        description="Current temperature (°C)"
    )
    humidity_percent: float = Field(
        ..., 
        ge=0, 
        le=100, 
        description="Relative humidity (%)"
    )
    wind_speed_kmh: float = Field(
        ..., 
        ge=0, 
        le=100, 
        description="Wind speed (km/h)"
    )
    distance_to_river_km: float = Field(
        ..., 
        ge=0, 
        le=50, 
        description="Distance to nearest water body (km)"
    )
    month: int = Field(
        ..., 
        ge=1, 
        le=12, 
        description="Month of year (1-12)"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "rainfall_mm": 150.0,
                "rainfall_7day_avg": 95.0,
                "rainfall_intensity": 15.0,
                "river_level_m": 9.5,
                "river_level_change": 1.8,
                "soil_moisture_percent": 85.0,
                "elevation_m": 45.0,
                "temperature_celsius": 26.0,
                "humidity_percent": 88.0,
                "wind_speed_kmh": 12.0,
                "distance_to_river_km": 1.2,
                "month": 7
            }
        }


class PredictionRequest(BaseModel):
    """Request for flood prediction"""
    
    features: FloodFeaturesInput
    location: Optional[str] = Field(
        "Unknown Location",
        description="Location name for alert"
    )
    include_detailed_analysis: bool = Field(
        True,
        description="Include detailed feature analysis"
    )


class RiskScore(BaseModel):
    """Risk score details"""
    
    numeric_level: int = Field(..., ge=0, le=3, description="Risk level (0-3)")
    label: str = Field(..., description="Risk label (Safe/Warning/High Risk/Critical)")
    threshold_min: float = Field(..., description="Minimum probability threshold")
    threshold_max: float = Field(..., description="Maximum probability threshold")


class Prediction(BaseModel):
    """Model prediction details"""
    
    probability: float = Field(..., description="Predicted probability")
    confidence: float = Field(..., description="Model confidence")
    all_probabilities: Dict[str, float] = Field(..., description="Probabilities for all classes")


class Alert(BaseModel):
    """Alert information"""
    
    timestamp: str = Field(..., description="Alert timestamp")
    location: str = Field(..., description="Location name")
    risk_level: int = Field(..., ge=0, le=3, description="Risk level (0-3)")
    risk_label: str = Field(..., description="Risk label")
    risk_color: str = Field(..., description="Color code (green/yellow/orange/red)")
    severity: str = Field(..., description="Severity text")
    title: str = Field(..., description="Alert title")
    message: str = Field(..., description="Main alert message")
    description: str = Field(..., description="Risk description")
    recommended_actions: List[str] = Field(..., description="List of recommended actions")
    emergency_contacts: Dict[str, str] = Field(default={}, description="Emergency phone numbers")
    additional_info: List[str] = Field(default=[], description="Critical feature warnings")
    detailed_conditions: Optional[Dict[str, str]] = Field(None, description="Current weather conditions")


class PredictionResponse(BaseModel):
    """Complete prediction response"""
    
    success: bool = Field(..., description="Request success status")
    alert: Alert
    prediction: Prediction
    risk_score: RiskScore
    input_features: FloodFeaturesInput
    processing_time_ms: Optional[float] = Field(None, description="Processing time in milliseconds")


class HealthResponse(BaseModel):
    """Health check response"""
    
    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Model loaded successfully")
    timestamp: str = Field(..., description="Current server time")
    version: str = Field(..., description="API version")


class ErrorResponse(BaseModel):
    """Error response"""
    
    success: bool = Field(False, description="Request success status")
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: str = Field(..., description="Error timestamp")


class QuickCheckRequest(BaseModel):
    """Quick risk check request (simplified)"""
    
    features: FloodFeaturesInput
    
    class Config:
        schema_extra = {
            "example": {
                "features": {
                    "rainfall_mm": 150.0,
                    "rainfall_7day_avg": 95.0,
                    "rainfall_intensity": 15.0,
                    "river_level_m": 9.5,
                    "river_level_change": 1.8,
                    "soil_moisture_percent": 85.0,
                    "elevation_m": 45.0,
                    "temperature_celsius": 26.0,
                    "humidity_percent": 88.0,
                    "wind_speed_kmh": 12.0,
                    "distance_to_river_km": 1.2,
                    "month": 7
                }
            }
        }


class QuickCheckResponse(BaseModel):
    """Quick risk check response (simplified)"""
    
    success: bool = Field(..., description="Request success status")
    risk_level: int = Field(..., ge=0, le=3, description="Risk level")
    risk_label: str = Field(..., description="Risk label")
    confidence: float = Field(..., description="Prediction confidence")
    action: str = Field(..., description="Recommended action summary")


class BatchPredictionRequest(BaseModel):
    """Batch prediction request"""
    
    predictions: List[PredictionRequest] = Field(
        ...,
        min_items=1,
        max_items=10,
        description="List of prediction requests (max 10)"
    )


class BatchPredictionResponse(BaseModel):
    """Batch prediction response"""
    
    success: bool = Field(..., description="Overall success status")
    results: List[PredictionResponse] = Field(..., description="List of prediction results")
    total_processed: int = Field(..., description="Number of requests processed")
    processing_time_ms: float = Field(..., description="Total processing time")