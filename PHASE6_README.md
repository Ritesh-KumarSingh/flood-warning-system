# Phase 6: Risk Scoring Logic - Instructions

## Overview
Transform ML predictions into actionable alerts with risk levels, messages, and safety recommendations.

## Prerequisites
✅ Phase 5 must be complete (flood_model.pkl must exist)

## Files Created
- `risk_scoring.py` - Core risk scoring and alert generation
- `flood_assessment.py` - Integrated prediction + scoring system
- `run_phase6.py` - Master script (runs all examples)
- `schema.py` - Shared configuration (copied from ML)
- `__init__.py` - Backend module initialization

---

## Quick Start (Recommended)

### Run Everything at Once
```powershell
# Navigate to src/backend directory
cd E:\disaster_management\disaster-warning-platform\src\backend

# Activate virtual environment (if not already active)
..\..\venv\Scripts\Activate.ps1

# Run the master script
python run_phase6.py
```

**Runtime:** ~10-20 seconds

---

## What Phase 6 Does

### 1. Risk Level Classification
Converts model probabilities to 4 risk levels:
- **Level 0 (Safe):** Probability < 0.3
- **Level 1 (Warning):** Probability 0.3 - 0.6
- **Level 2 (High Risk):** Probability 0.6 - 0.8
- **Level 3 (Critical):** Probability > 0.8

### 2. Alert Message Generation
Creates contextual alerts with:
- ✅ Alert title (location-specific)
- ✅ Main message
- ✅ Risk description
- ✅ Recommended actions (prioritized list)
- ✅ Emergency contacts (when relevant)
- ✅ Timestamp and severity level

### 3. Feature Analysis
Automatically identifies critical conditions:
- ✅ Extreme rainfall (>200mm)
- ✅ Dangerous river levels (>11m)
- ✅ Saturated soil (>85%)
- ✅ Low elevation (<30m)
- ✅ Proximity to river (<1km)
- ✅ Rapid water rise (>2m/6h)

### 4. Action Recommendations
Provides specific, actionable guidance:
- **Safe:** Continue normal activities
- **Warning:** 7 preparedness actions
- **High Risk:** 9 evacuation preparation steps
- **Critical:** 9 immediate evacuation instructions

### 5. Emergency Integration
Includes relevant emergency contacts:
- National Emergency: 112
- Disaster Management: 1078
- Police: 100
- Fire: 101
- Ambulance: 102

---

## Expected Output Files

Phase 6 doesn't create files - it's a pure code module. But you'll have:

```
src/backend/
├── __init__.py
├── schema.py
├── risk_scoring.py          (Core scoring logic)
├── flood_assessment.py      (Integrated system)
└── run_phase6.py           (Examples)
```

---

## System Architecture

```
Input Features
     ↓
ML Model (Phase 5)
     ↓
Prediction Probability
     ↓
Risk Scorer
     ↓
Risk Level (0-3)
     ↓
Alert Generator
     ↓
Formatted Alert
     ↓
User Display / API Response
```

---

## Understanding the Output

### Console Output Example

```
🚀 PHASE 6: RISK SCORING LOGIC
======================================================================

STEP 1: Risk Scoring Module Demo
----------------------------------------------------------------------
✅ Risk scorer initialized

📊 Generating Safe alert for Mumbai...
   ✅ Title: ✅ All Clear in Mumbai
   ✅ Actions: 3 recommended

📊 Generating Warning alert for Kolkata...
   ✅ Title: ⚠️ Flood Watch for Kolkata
   ✅ Actions: 7 recommended
   ✅ Emergency contacts: 2

📊 Generating High Risk alert for Patna...
   ✅ Title: 🚨 Flood Warning for Patna
   ✅ Actions: 9 recommended
   ✅ Emergency contacts: 5

📊 Generating Critical alert for Guwahati...
   ✅ Title: 🔴 CRITICAL FLOOD ALERT - GUWAHATI
   ✅ Actions: 9 recommended
   ✅ Emergency contacts: 5

✅ Step 1 Complete!

STEP 2: Integrated Flood Assessment System
----------------------------------------------------------------------

EXAMPLE 1: Normal Weather Conditions
======================================================================
              ✅ All Clear in Lucknow
======================================================================

📍 Location: Lucknow
🕐 Time: 2025-02-15 15:30:45
⚠️  Severity: Low

Weather conditions in Lucknow are normal. No flood risk detected...

📋 RECOMMENDED ACTIONS:
   1. Continue normal activities
   2. Stay updated on weather forecasts
   3. Review your emergency plan periodically

🌡️  CURRENT CONDITIONS:
   Rainfall (24h): 15.0 mm
   River Level: 3.5 meters
   Soil Moisture: 45.0%

======================================================================


EXAMPLE 4: Critical Flood Emergency
======================================================================
          🔴 CRITICAL FLOOD ALERT - AYODHYA
======================================================================

📍 Location: Ayodhya
🕐 Time: 2025-02-15 15:30:48
⚠️  Severity: Critical

CRITICAL FLOOD DANGER in Ayodhya! Extreme weather conditions...

🔍 CRITICAL CONDITIONS:
   🌧️ EXTREME rainfall detected: 340.0 mm in last 24 hours
   🌊 DANGER LEVEL: River at 13.2 meters (critical threshold)
   💧 Ground saturated: 96.0% moisture (high runoff risk)
   ⚠️ Very close to river: 0.4 km (immediate flood zone)
   📈 Rapidly rising water: +4.1 meters in 6 hours
   ⬇️ Low elevation: 18.0 meters (flood-prone area)

📋 RECOMMENDED ACTIONS:
   1. 🚨 EVACUATE IMMEDIATELY to designated shelter...
   2. 🚨 Do NOT wait for further instructions
   3. Take ONLY essential items (ID, medications, phone)
   4. Do NOT attempt to drive through floodwater
   5. If trapped, move to highest floor or rooftop
   6. Call emergency services: 112 / 101 (India)
   7. Signal for help if stranded
   8. Do NOT return home until authorities declare it safe
   9. Avoid contact with floodwater (contamination risk)

📞 EMERGENCY CONTACTS:
   National Emergency: 112
   Disaster Management: 1078
   Police: 100
   Fire: 101
   Ambulance: 102

🌡️  CURRENT CONDITIONS:
   Rainfall (24h): 340.0 mm
   River Level: 13.2 meters
   Soil Moisture: 96.0%

======================================================================
```

---

## Risk Level Details

### Level 0: Safe 🟢
- **Threshold:** Probability < 30%
- **Title:** "✅ All Clear in {location}"
- **Actions:** 3 basic preparedness tips
- **Emergency Contacts:** None
- **Message Tone:** Reassuring, informative

### Level 1: Warning 🟡
- **Threshold:** Probability 30-60%
- **Title:** "⚠️ Flood Watch for {location}"
- **Actions:** 7 preparation steps
- **Emergency Contacts:** 2 (Emergency, Disaster Management)
- **Message Tone:** Cautionary, proactive

### Level 2: High Risk 🟠
- **Threshold:** Probability 60-80%
- **Title:** "🚨 Flood Warning for {location}"
- **Actions:** 9 evacuation preparation steps
- **Emergency Contacts:** 5 (All services)
- **Message Tone:** Urgent, directive

### Level 3: Critical 🔴
- **Threshold:** Probability > 80%
- **Title:** "🔴 CRITICAL FLOOD ALERT - {LOCATION}"
- **Actions:** 9 immediate evacuation instructions
- **Emergency Contacts:** 5 (All services)
- **Message Tone:** Emergency, life-or-death

---

## Using the Risk Scoring System

### Basic Usage

```python
from risk_scoring import RiskScorer

# Initialize
scorer = RiskScorer()

# Generate alert for a risk level
alert = scorer.generate_alert_message(
    risk_level=2,
    location="Delhi",
    features={
        'rainfall_mm': 150.0,
        'river_level_m': 9.5,
        # ... other features
    }
)

print(alert['title'])
print(alert['message'])
for action in alert['recommended_actions']:
    print(f"- {action}")
```

### Integrated Assessment

```python
from flood_assessment import FloodRiskAssessor

# Initialize (loads model automatically)
assessor = FloodRiskAssessor()

# Complete assessment
features = {
    'rainfall_mm': 150.0,
    'rainfall_7day_avg': 95.0,
    # ... all 12 features
}

assessment = assessor.assess_flood_risk(features, location="Chennai")

# Get formatted alert text
alert_text = assessor.get_formatted_alert(features, "Chennai")
print(alert_text)

# Quick check (simplified)
quick = assessor.quick_check(features)
print(f"Risk: {quick['risk_label']}, Confidence: {quick['confidence']}")
```

### Batch Assessment

```python
# Assess multiple locations at once
features_list = [features1, features2, features3]
locations = ["Mumbai", "Pune", "Nagpur"]

assessments = assessor.batch_assess(features_list, locations)

for assessment in assessments:
    print(f"{assessment['location']}: {assessment['risk_label']}")
```

---

## Critical Features Analysis

The system automatically identifies dangerous conditions:

| Feature | Threshold | Warning Generated |
|---------|-----------|-------------------|
| **Rainfall** | >200mm | 🌧️ EXTREME rainfall |
| **Rainfall** | >100mm | 🌧️ Heavy rainfall |
| **River Level** | >11m | 🌊 DANGER LEVEL |
| **River Level** | >8m | 🌊 WARNING level |
| **Soil Moisture** | >85% | 💧 Ground saturated |
| **Distance** | <1km | ⚠️ Very close to river |
| **Level Change** | >2m/6h | 📈 Rapidly rising water |
| **Elevation** | <30m | ⬇️ Low elevation |

---

## Action Recommendations by Risk Level

### Safe (3 actions)
1. Continue normal activities
2. Stay updated on weather forecasts  
3. Review emergency plan periodically

### Warning (7 actions)
1. Monitor weather updates closely
2. Prepare emergency kit
3. Identify evacuation routes
4. Move important documents to higher floors
5. Charge electronic devices
6. Fill containers with clean water
7. Stay in contact with family

### High Risk (9 actions)
1. PREPARE TO EVACUATE - Pack now
2. Move vehicles to higher ground
3. Turn off utilities if instructed
4. Move valuables to upper floors
5. Secure outdoor items
6. Stay tuned to emergency broadcasts
7. Do NOT walk/drive through flooded areas
8. Keep emergency kit ready
9. Inform neighbors

### Critical (9 actions)
1. 🚨 EVACUATE IMMEDIATELY
2. 🚨 Do NOT wait
3. Take ONLY essentials (ID, meds, phone)
4. Do NOT drive through floodwater
5. If trapped, move to highest floor/rooftop
6. Call emergency: 112 / 101
7. Signal for help if stranded
8. Do NOT return until safe
9. Avoid floodwater contact

---

## Emergency Contacts (India)

The system includes these emergency numbers:

| Service | Number | When Shown |
|---------|--------|------------|
| National Emergency | 112 | Warning, High, Critical |
| Disaster Management | 1078 | Warning, High, Critical |
| Police | 100 | High Risk, Critical |
| Fire | 101 | High Risk, Critical |
| Ambulance | 102 | High Risk, Critical |

---

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'predict'"
**Solution:** The backend needs access to ML modules
```powershell
# Make sure you're running from src/backend/
cd E:\disaster_management\disaster-warning-platform\src\backend
python run_phase6.py
```

### Problem: "FileNotFoundError: flood_model.pkl not found"
**Solution:** Phase 5 must be completed first
```powershell
cd ..\ml
python run_phase5.py
cd ..\backend
python run_phase6.py
```

### Problem: Import errors with schema
**Solution:** schema.py should be in both src/ml/ and src/backend/
```powershell
# Copy if missing
cp ..\ml\schema.py schema.py
```

---

## Verification Checklist

After running Phase 6:

- [ ] Ran `python run_phase6.py` successfully
- [ ] File exists: `src\backend\risk_scoring.py`
- [ ] File exists: `src\backend\flood_assessment.py`
- [ ] File exists: `src\backend\schema.py`
- [ ] Console shows all 4 risk level examples
- [ ] Alerts include recommended actions
- [ ] Emergency contacts appear for high-risk alerts
- [ ] Feature warnings detected automatically

---

## For Your Hackathon Presentation

### Key Points to Mention

> **"Our system doesn't just predict floods - it provides actionable intelligence..."**

> **"For critical floods, we provide 9 specific evacuation instructions, not just 'be careful'..."**

> **"The system automatically analyzes 6 critical features like rainfall intensity and river rise rate..."**

> **"Alerts are contextual - safe conditions get 3 tips, critical emergencies get life-saving instructions..."**

### Demo Script

1. **Show Safe Alert:**
   > "In normal conditions, users get reassuring updates and basic preparedness tips."

2. **Show Critical Alert:**
   > "But when danger strikes, notice how the system transforms - red alert, immediate evacuation orders, emergency contacts, and specific critical conditions highlighted."

3. **Highlight Features:**
   > "See these warnings? The AI detected extreme rainfall of 340mm, dangerous river levels, and saturated ground - all automatically analyzed."

---

## Integration with Other Phases

### From Phase 5 (ML Model)
```python
# Phase 5 gives you
prediction = model.predict(features)  # Probability

# Phase 6 converts it to
alert = scorer.generate_alert(risk_level, location)  # Actionable message
```

### To Phase 7 (Backend API)
```python
# Phase 6 output becomes API response
@app.post("/predict")
async def predict(features: dict):
    assessment = assessor.assess_flood_risk(features)
    return assessment  # Send to frontend
```

---

## What's Next?

After Phase 6 is complete, you'll have:
- ✅ Complete risk scoring system
- ✅ 4-level alert classification
- ✅ Actionable recommendations
- ✅ Emergency contact integration
- ✅ Automatic feature analysis
- ✅ Ready for API integration

**Next:** Phase 7 - Backend API Development
- Build FastAPI endpoints
- Create prediction API
- Handle real-time requests
- Return JSON responses
- Add input validation

---

## Key Takeaways

🎯 **Risk scoring bridges ML and users** - Transforms probabilities into action  
🎯 **Context matters** - Same 70% probability means different things in different conditions  
🎯 **Specificity saves lives** - "Evacuate immediately" > "Be careful"  
🎯 **Automation is key** - System identifies critical features without human analysis  
🎯 **Emergency integration** - Direct access to help when needed most  

---

**Ready to run Phase 6?** Just execute the command in Quick Start and watch your risk scoring system come alive! 🚀

The output will show you exactly how your AI transforms raw predictions into life-saving alerts! 🌊⚡