"""
FastAPI Backend Application
Main API server for flood prediction system
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
from datetime import datetime
import os
from contextlib import asynccontextmanager

# Ensure backend dir is on the path for sibling imports
import sys
_backend_dir = os.path.dirname(os.path.abspath(__file__))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from models import (
    PredictionRequest, PredictionResponse, HealthResponse,
    ErrorResponse, QuickCheckRequest, QuickCheckResponse,
    BatchPredictionRequest, BatchPredictionResponse
)
from flood_assessment import FloodRiskAssessor

# Global assessor instance
assessor = None

# --- Lifespan (replaces deprecated @app.on_event) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle"""
    global assessor
    try:
        print("\n" + "="*70)
        print(" "*20 + "🚀 STARTING FLOOD WARNING API")
        print("="*70 + "\n")

        # Initialize assessor (loads model)
        assessor = FloodRiskAssessor()

        # Initialize weather endpoints client + assessor
        from weather_endpoints import init_weather_client
        init_weather_client()

        print("✅ API started successfully!")
        print(f"📍 Docs available at: http://localhost:8000/docs")
        print(f"📍 Health check: http://localhost:8000/health")
        print("="*70 + "\n")
    except Exception as e:
        print(f"❌ Error during startup: {e}")
        import traceback
        traceback.print_exc()

    yield  # app runs here

# Initialize FastAPI app
app = FastAPI(
    title="Flood Early Warning API",
    description="AI-powered flood prediction and early warning system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS (allow frontend to access API)
_cors_origins = os.environ.get(
    "CORS_ORIGINS", "http://localhost:8501,http://localhost:3000"
).split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all uncaught exceptions"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Flood Early Warning API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST)",
            "quick_check": "/quick-check (POST)",
            "batch_predict": "/batch-predict (POST)",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if assessor is not None else "unhealthy",
        "model_loaded": assessor is not None,
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_flood_risk(request: PredictionRequest):
    """
    Predict flood risk and generate alert
    
    Returns comprehensive risk assessment with:
    - Risk level (0-3)
    - Probability and confidence
    - Alert message with recommendations
    - Emergency contacts
    - Critical feature warnings
    """
    start_time = time.time()
    
    try:
        if assessor is None:
            raise HTTPException(
                status_code=503,
                detail="Model not loaded. Service unavailable."
            )
        
        # Convert Pydantic model to dict
        features = request.features.dict()
        
        # Perform assessment
        assessment = assessor.assess_flood_risk(
            features,
            location=request.location,
            include_detailed_conditions=request.include_detailed_analysis
        )
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000  # Convert to ms
        
        # Build response
        response = PredictionResponse(
            success=True,
            alert=assessment,
            prediction=assessment['prediction'],
            risk_score=assessment['risk_score'],
            input_features=request.features,
            processing_time_ms=processing_time
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@app.post("/quick-check", response_model=QuickCheckResponse, tags=["Prediction"])
async def quick_risk_check(request: QuickCheckRequest):
    """
    Quick risk check (simplified response)
    
    Returns only essential information:
    - Risk level
    - Confidence
    - Brief action recommendation
    """
    try:
        if assessor is None:
            raise HTTPException(
                status_code=503,
                detail="Model not loaded. Service unavailable."
            )
        
        # Convert to dict
        features = request.features.dict()
        
        # Quick check
        result = assessor.quick_check(features)
        
        return QuickCheckResponse(
            success=True,
            risk_level=result['risk_level'],
            risk_label=result['risk_label'],
            confidence=result['confidence'],
            action=result['action']
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Quick check failed: {str(e)}"
        )


@app.post("/batch-predict", response_model=BatchPredictionResponse, tags=["Prediction"])
async def batch_predict(request: BatchPredictionRequest):
    """
    Batch prediction for multiple locations
    
    Process up to 10 predictions in a single request
    """
    start_time = time.time()
    
    try:
        if assessor is None:
            raise HTTPException(
                status_code=503,
                detail="Model not loaded. Service unavailable."
            )
        
        if len(request.predictions) > 10:
            raise HTTPException(
                status_code=400,
                detail="Maximum 10 predictions per batch request"
            )
        
        results = []
        
        for pred_request in request.predictions:
            try:
                # Convert to dict
                features = pred_request.features.dict()
                
                # Perform assessment
                assessment = assessor.assess_flood_risk(
                    features,
                    location=pred_request.location,
                    include_detailed_conditions=pred_request.include_detailed_analysis
                )
                
                # Build individual response
                result = PredictionResponse(
                    success=True,
                    alert=assessment,
                    prediction=assessment['prediction'],
                    risk_score=assessment['risk_score'],
                    input_features=pred_request.features,
                    processing_time_ms=None
                )
                
                results.append(result)
                
            except Exception as e:
                # Add error entry for failed prediction
                error_result = PredictionResponse(
                    success=False,
                    alert=None,
                    prediction=None,
                    risk_score=None,
                    input_features=pred_request.features,
                    processing_time_ms=None
                )
                results.append(error_result)
        
        # Calculate total processing time
        total_time = (time.time() - start_time) * 1000
        
        return BatchPredictionResponse(
            success=True,
            results=results,
            total_processed=len(results),
            processing_time_ms=total_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch prediction failed: {str(e)}"
        )


@app.get("/risk-levels", tags=["Information"])
async def get_risk_levels():
    """Get information about risk levels"""
    return {
        "risk_levels": {
            "0": {
                "label": "Safe",
                "color": "green",
                "threshold": "< 30%",
                "description": "No flood risk detected"
            },
            "1": {
                "label": "Warning",
                "color": "yellow",
                "threshold": "30% - 60%",
                "description": "Moderate flood risk"
            },
            "2": {
                "label": "High Risk",
                "color": "orange",
                "threshold": "60% - 80%",
                "description": "High flood risk expected"
            },
            "3": {
                "label": "Critical",
                "color": "red",
                "threshold": "> 80%",
                "description": "Critical flood danger"
            }
        }
    }


@app.get("/features", tags=["Information"])
async def get_feature_info():
    """Get information about input features"""
    return {
        "features": {
            "rainfall_mm": {
                "name": "Rainfall (24h)",
                "unit": "mm",
                "range": "0-500",
                "description": "Rainfall in last 24 hours"
            },
            "rainfall_7day_avg": {
                "name": "Rainfall (7-day avg)",
                "unit": "mm",
                "range": "0-300",
                "description": "7-day average rainfall"
            },
            "rainfall_intensity": {
                "name": "Rainfall Intensity",
                "unit": "mm/h",
                "range": "0-50",
                "description": "Current rainfall rate"
            },
            "river_level_m": {
                "name": "River Level",
                "unit": "meters",
                "range": "0-15",
                "description": "Current river water level"
            },
            "river_level_change": {
                "name": "River Level Change",
                "unit": "meters",
                "range": "-2 to +5",
                "description": "Change in last 6 hours"
            },
            "soil_moisture_percent": {
                "name": "Soil Moisture",
                "unit": "%",
                "range": "0-100",
                "description": "Soil saturation level"
            },
            "elevation_m": {
                "name": "Elevation",
                "unit": "meters",
                "range": "0-1000",
                "description": "Location elevation"
            },
            "temperature_celsius": {
                "name": "Temperature",
                "unit": "°C",
                "range": "-10 to 45",
                "description": "Current temperature"
            },
            "humidity_percent": {
                "name": "Humidity",
                "unit": "%",
                "range": "0-100",
                "description": "Relative humidity"
            },
            "wind_speed_kmh": {
                "name": "Wind Speed",
                "unit": "km/h",
                "range": "0-100",
                "description": "Current wind speed"
            },
            "distance_to_river_km": {
                "name": "Distance to River",
                "unit": "km",
                "range": "0-50",
                "description": "Distance to nearest water body"
            },
            "month": {
                "name": "Month",
                "unit": "1-12",
                "range": "1-12",
                "description": "Month of year"
            }
        },
        "total_features": 12
    }


if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Starting Flood Warning API Server...")
    print("📍 Visit http://localhost:8000/docs for interactive API documentation\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )