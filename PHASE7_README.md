# Phase 7: Backend API Development - Instructions

## Overview
Build a production-ready FastAPI backend that serves ML predictions via REST endpoints.

## Prerequisites
✅ Phases 1-6 must be complete (model trained, risk scoring working)

## Files Created
- `main.py` - FastAPI application with all endpoints
- `models.py` - Pydantic models for validation
- `test_api.py` - API testing script
- `run_phase7.py` - Master script to start server

---

## Quick Start (Recommended)

### Start the API Server
```powershell
# Navigate to src/backend directory
cd E:\disaster_management\disaster-warning-platform\src\backend

# Activate virtual environment
..\..\venv\Scripts\Activate.ps1

# Start the server
python run_phase7.py
```

The server will start at: **http://localhost:8000**

### Test the API (in a separate terminal)
```powershell
# Open a NEW terminal window
cd E:\disaster_management\disaster-warning-platform\src\backend

# Activate venv
..\..\venv\Scripts\Activate.ps1

# Run tests
python test_api.py
```

---

## API Endpoints

### 1. **Root** - `GET /`
Get API information and available endpoints

**Example:**
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "message": "Flood Early Warning API",
  "version": "1.0.0",
  "status": "operational",
  "endpoints": {
    "health": "/health",
    "predict": "/predict (POST)",
    "quick_check": "/quick-check (POST)",
    "docs": "/docs"
  }
}
```

---

### 2. **Health Check** - `GET /health`
Check if API and model are loaded

**Example:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2025-02-15T15:30:45.123456",
  "version": "1.0.0"
}
```

---

### 3. **Predict** - `POST /predict`
Full flood risk prediction with alerts

**Request Body:**
```json
{
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
  },
  "location": "Delhi",
  "include_detailed_analysis": true
}
```

**Response:**
```json
{
  "success": true,
  "alert": {
    "timestamp": "2025-02-15T15:30:45",
    "location": "Delhi",
    "risk_level": 2,
    "risk_label": "High Risk",
    "risk_color": "orange",
    "severity": "High",
    "title": "🚨 Flood Warning for Delhi",
    "message": "High flood risk expected in Delhi within...",
    "recommended_actions": [
      "PREPARE TO EVACUATE - Pack essential items now",
      "Move vehicles to higher ground immediately",
      ...
    ],
    "emergency_contacts": {
      "national_emergency": "112",
      "disaster_management": "1078",
      ...
    },
    "additional_info": [
      "🌧️ Heavy rainfall: 150.0 mm in last 24 hours",
      "🌊 WARNING: River at 9.5 meters (above normal)"
    ]
  },
  "prediction": {
    "probability": 0.87,
    "confidence": 0.87,
    "all_probabilities": {
      "safe": 0.02,
      "warning": 0.11,
      "high_risk": 0.87,
      "critical": 0.00
    }
  },
  "risk_score": {
    "numeric_level": 2,
    "label": "High Risk",
    "threshold_min": 0.6,
    "threshold_max": 0.8
  },
  "processing_time_ms": 125.43
}
```

---

### 4. **Quick Check** - `POST /quick-check`
Simplified risk assessment

**Request Body:**
```json
{
  "features": {
    "rainfall_mm": 95.0,
    "rainfall_7day_avg": 65.0,
    "rainfall_intensity": 10.0,
    "river_level_m": 7.2,
    "river_level_change": 0.8,
    "soil_moisture_percent": 72.0,
    "elevation_m": 85.0,
    "temperature_celsius": 26.0,
    "humidity_percent": 82.0,
    "wind_speed_kmh": 18.0,
    "distance_to_river_km": 2.3,
    "month": 7
  }
}
```

**Response:**
```json
{
  "success": true,
  "risk_level": 1,
  "risk_label": "Warning",
  "confidence": 0.78,
  "action": "Prepare emergency kit. Stay informed about weather."
}
```

---

### 5. **Batch Predict** - `POST /batch-predict`
Process multiple predictions at once (max 10)

**Request Body:**
```json
{
  "predictions": [
    {
      "features": { /* features */ },
      "location": "Mumbai"
    },
    {
      "features": { /* features */ },
      "location": "Delhi"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "results": [
    { /* prediction 1 */ },
    { /* prediction 2 */ }
  ],
  "total_processed": 2,
  "processing_time_ms": 250.67
}
```

---

### 6. **Risk Levels Info** - `GET /risk-levels`
Get risk level definitions

**Response:**
```json
{
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
    ...
  }
}
```

---

### 7. **Features Info** - `GET /features`
Get input feature descriptions

**Response:**
```json
{
  "features": {
    "rainfall_mm": {
      "name": "Rainfall (24h)",
      "unit": "mm",
      "range": "0-500",
      "description": "Rainfall in last 24 hours"
    },
    ...
  },
  "total_features": 12
}
```

---

## Interactive API Documentation

FastAPI automatically generates interactive docs!

### Swagger UI
Visit: **http://localhost:8000/docs**

Features:
- ✅ Interactive API testing
- ✅ Try out endpoints in browser
- ✅ Auto-generated request examples
- ✅ Response schema documentation
- ✅ No Postman needed!

### ReDoc
Visit: **http://localhost:8000/redoc**

Features:
- ✅ Clean, readable documentation
- ✅ Searchable
- ✅ Export to OpenAPI spec

---

## Testing the API

### Option 1: Automated Tests (Recommended)
```powershell
# Start server in one terminal
python run_phase7.py

# Run tests in another terminal
python test_api.py
```

**Expected Output:**
```
🧪 FLOOD WARNING API TESTS
======================================================================

1️⃣  Testing Root Endpoint
======================================================================
Status Code: 200
✅ PASS

2️⃣  Testing Health Check
======================================================================
Status Code: 200
Status: healthy
Model Loaded: True
✅ PASS

3️⃣  Testing Prediction - Safe Conditions
======================================================================
📊 Prediction Result:
   Location: Mumbai
   Risk Level: 0 (Safe)
   Confidence: 100.0%
   Processing Time: 125.43 ms
✅ PASS

...

📊 TEST SUMMARY
======================================================================
✅ PASS - Root Endpoint
✅ PASS - Health Check
✅ PASS - Prediction - Safe
✅ PASS - Prediction - Critical
✅ PASS - Quick Check
✅ PASS - Risk Levels Info
✅ PASS - Features Info

Results: 7/7 tests passed (100%)
🎉 All tests passed! API is working perfectly!
```

### Option 2: Manual Testing with cURL

```powershell
# Health check
curl http://localhost:8000/health

# Simple prediction
curl -X POST http://localhost:8000/predict `
  -H "Content-Type: application/json" `
  -d '{
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
    },
    "location": "Test City"
  }'
```

### Option 3: Interactive Docs (Easiest!)

1. Start server: `python run_phase7.py`
2. Open browser: http://localhost:8000/docs
3. Click on any endpoint
4. Click "Try it out"
5. Fill in example data
6. Click "Execute"
7. See the response!

---

## Input Validation

The API automatically validates all inputs using Pydantic:

### Valid Input
```json
{
  "rainfall_mm": 150.0  // ✅ Valid: 0-500 range
}
```

### Invalid Input
```json
{
  "rainfall_mm": -10.0  // ❌ Error: must be >= 0
}
```

**Error Response:**
```json
{
  "detail": [
    {
      "loc": ["body", "features", "rainfall_mm"],
      "msg": "ensure this value is greater than or equal to 0",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

---

## Error Handling

The API returns descriptive errors:

### Model Not Loaded (503)
```json
{
  "detail": "Model not loaded. Service unavailable."
}
```

### Invalid Input (422)
```json
{
  "detail": [
    {
      "loc": ["body", "features", "month"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Server Error (500)
```json
{
  "success": false,
  "error": "Internal server error",
  "detail": "Prediction failed: ...",
  "timestamp": "2025-02-15T15:30:45"
}
```

---

## CORS Configuration

CORS is enabled for frontend integration:

```python
# main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production!
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**For production**, replace `["*"]` with specific origins:
```python
allow_origins=[
    "http://localhost:3000",  # React dev server
    "https://yourdomain.com"  # Production domain
]
```

---

## Performance

### Processing Times
- Single prediction: ~100-200ms
- Quick check: ~50-100ms
- Batch prediction (10): ~1-2 seconds

### Model Loading
- Startup time: ~5-10 seconds
- Model loads once on startup
- Stays in memory for fast predictions

---

## Troubleshooting

### Problem: "Address already in use"
**Solution:** Port 8000 is busy
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <PID> /F

# Or use a different port in run_phase7.py:
# uvicorn.run(..., port=8001)
```

### Problem: "Model not loaded"
**Solution:** Phase 5 must be complete
```powershell
cd ..\ml
python run_phase5.py
cd ..\backend
python run_phase7.py
```

### Problem: "ModuleNotFoundError: models"
**Solution:** Run from correct directory
```powershell
cd E:\disaster_management\disaster-warning-platform\src\backend
python run_phase7.py
```

### Problem: Tests fail with connection error
**Solution:** Start the server first
```powershell
# Terminal 1: Start server
python run_phase7.py

# Terminal 2: Run tests (after server starts)
python test_api.py
```

---

## For Your Hackathon Presentation

### Demo Flow

1. **Start Server:**
   ```powershell
   python run_phase7.py
   ```

2. **Open Interactive Docs:**
   - Browser: http://localhost:8000/docs
   - Show the judges the auto-generated documentation

3. **Live Demo:**
   - Click on `/predict` endpoint
   - Click "Try it out"
   - Use the example data (already filled in)
   - Click "Execute"
   - Show the real-time response

4. **Highlight Features:**
   > "Our API provides comprehensive flood assessments in under 200ms..."
   
   > "Input validation ensures data integrity with automatic error messages..."
   
   > "Interactive documentation makes integration easy for any frontend..."

### Key Talking Points

> **"We built a production-ready REST API with FastAPI - one of the fastest Python frameworks..."**

> **"The API validates all 12 input features automatically and returns descriptive errors..."**

> **"Processing time is under 200 milliseconds - fast enough for real-time applications..."**

> **"We support batch predictions for up to 10 locations simultaneously..."**

> **"The API is CORS-enabled and ready for frontend integration..."**

---

## Integration with Frontend (Phase 10)

### JavaScript/React Example
```javascript
// Fetch prediction
const response = await fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    features: {
      rainfall_mm: 150.0,
      // ... other features
    },
    location: 'Mumbai'
  })
});

const data = await response.json();
console.log(`Risk: ${data.alert.risk_label}`);
console.log(`Action: ${data.alert.recommended_actions[0]}`);
```

### Python Client Example
```python
import requests

response = requests.post(
    'http://localhost:8000/predict',
    json={
        'features': {
            'rainfall_mm': 150.0,
            # ... other features
        },
        'location': 'Mumbai'
    }
)

data = response.json()
print(f"Risk: {data['alert']['risk_label']}")
```

---

## Verification Checklist

After running Phase 7:

- [ ] Server starts without errors
- [ ] Can access http://localhost:8000
- [ ] Interactive docs work at /docs
- [ ] Health check returns "healthy"
- [ ] `/predict` endpoint returns predictions
- [ ] `/quick-check` works
- [ ] All tests pass (7/7)
- [ ] Processing time < 200ms

---

## Deployment Notes (Optional)

For production deployment:

### Render.com (Free tier)
1. Push code to GitHub
2. Create new Web Service on Render
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn src.backend.main:app --host 0.0.0.0 --port $PORT`

### Railway (Free tier)
1. Connect GitHub repo
2. Railway auto-detects FastAPI
3. Deploys automatically

### Heroku
1. Add `Procfile`: `web: uvicorn src.backend.main:app --host 0.0.0.0 --port $PORT`
2. Push to Heroku
3. Scale: `heroku ps:scale web=1`

---

## What's Next?

After Phase 7 is complete, you'll have:
- ✅ Production-ready REST API
- ✅ 7 working endpoints
- ✅ Auto-generated documentation
- ✅ Input validation
- ✅ Error handling
- ✅ CORS enabled
- ✅ Fast processing (<200ms)
- ✅ Ready for frontend integration

**Next:** Phase 8 - Live Data Integration
- Connect weather APIs
- Real-time data fetching
- Location-based predictions
- Automatic updates

---

## Quick Reference

### Start Server
```powershell
python run_phase7.py
```

### Test API
```powershell
python test_api.py
```

### View Docs
```
http://localhost:8000/docs
```

### Stop Server
```
Press Ctrl+C
```

---

**Ready to start your API?** Run `python run_phase7.py` and watch your backend come alive! 🚀