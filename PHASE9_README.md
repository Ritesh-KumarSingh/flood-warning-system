# Phase 9: Alert Engine - Instructions

## Overview
Build an alert delivery system that sends notifications via SMS, Email, and Push when flood risk is detected.

## Prerequisites
✅ Phases 1-8 must be complete (model, API, weather integration working)

## Files Created
- `alert_engine.py` - Alert delivery engine (SMS, Email, Push)
- `run_phase9.py` - Demonstration script

---

## Quick Start (Demo Mode)

### Run the Demo
```powershell
# Navigate to src/backend
cd E:\disaster_management\disaster-warning-platform\src\backend

# Activate virtual environment
..\..\venv\Scripts\Activate.ps1

# Run Phase 9 demo
python run_phase9.py
```

**Demo mode simulates all notifications - perfect for hackathon presentations!**

---

## What Phase 9 Does

### 1. **Alert Triggering**
Automatically sends alerts when risk exceeds threshold:
- **Level 0 (Safe):** No alert
- **Level 1 (Warning):** ⚠️  Alert sent
- **Level 2 (High Risk):** 🚨 Urgent alert
- **Level 3 (Critical):** 🔴 Emergency broadcast

### 2. **SMS Notifications** (via Twilio)
Sends concise 160-character emergency messages:
```
FLOOD ALERT: CRITICAL - Ayodhya.
EVACUATE IMMEDIATELY! Call 112.
```

### 3. **Email Alerts**
Sends detailed alerts with:
- Full risk assessment
- Recommended actions
- Emergency contacts
- Critical conditions

### 4. **Push Notifications** (Simulated)
Mobile app notifications with:
- Alert title
- Brief message
- Risk level data

### 5. **Multi-Channel Delivery**
Send to all channels simultaneously for redundancy

### 6. **Bulk Alerting**
Process multiple cities and send to registered contacts

---

## Demo Output

When you run `python run_phase9.py`, you'll see:

```
======================================================================
               🚀 PHASE 9: ALERT ENGINE
======================================================================

🔧 Initializing systems...
🎭 Alert Engine in DEMO MODE (simulates sending)
✅ Systems ready!

======================================================================
SCENARIO 1: Safe Weather Conditions
======================================================================

📍 Location: Bangalore
🌡️  Current conditions: Light rain, normal river levels

🎯 Prediction: Safe (Level 0)
📊 Confidence: 100.0%

✅ No alert needed - conditions are safe
   (Alert threshold: Level 1 - Warning or higher)

----------------------------------------------------------------------

======================================================================
SCENARIO 2: Warning Conditions - Moderate Risk
======================================================================

📍 Location: Patna
🌧️  Current conditions: Heavy rainfall, rising water levels

🎯 Prediction: Warning (Level 1)
📊 Confidence: 100.0%

⚠️  ALERT TRIGGERED! Sending notifications...

📱 SIMULATING SMS to 2 recipient(s)
Message: FLOOD ALERT: WARNING - Patna. Monitor updates...

📧 SIMULATING EMAIL to 2 recipient(s)
Subject: 🚨 ⚠️ Flood Watch for Patna
Body preview: FLOOD EARLY WARNING ALERT...

🔔 SIMULATING PUSH NOTIFICATION
Title: ⚠️ Flood Watch for Patna
Body: Moderate flood risk detected in Patna...

📊 Delivery Report:
   Timestamp: 2025-02-15T16:30:45.123456
   Location: Patna
   Risk Level: 1
   Channels: 3

   ✅ SMS: simulated
   ✅ EMAIL: simulated
   ✅ PUSH: simulated

----------------------------------------------------------------------

======================================================================
SCENARIO 3: CRITICAL EMERGENCY - Immediate Evacuation
======================================================================

📍 Location: Ayodhya
🚨 Current conditions: EXTREME rainfall, DANGER-level river

🎯 Prediction: Critical (Level 3)
📊 Confidence: 100.0%

⚠️  Critical Conditions Detected:
   🌧️ EXTREME rainfall detected: 340.0 mm in last 24 hours
   🌊 DANGER LEVEL: River at 13.2 meters (critical threshold)
   💧 Ground saturated: 96.0% moisture (high runoff risk)

🚨 CRITICAL ALERT! Broadcasting emergency notifications...

📱 SIMULATING SMS to 4 recipient(s)
Message: FLOOD ALERT: CRITICAL - Ayodhya. EVACUATE IMMEDIATELY! Call 112.

📧 SIMULATING EMAIL to 3 recipient(s)
Subject: 🚨 🔴 CRITICAL FLOOD ALERT - AYODHYA

🔔 SIMULATING PUSH NOTIFICATION
Title: 🔴 CRITICAL FLOOD ALERT - AYODHYA

📊 Emergency Broadcast Report:
   Timestamp: 2025-02-15T16:30:47.456789
   Location: Ayodhya
   Risk Level: CRITICAL (3)
   Priority: HIGHEST

   🚨 SMS: simulated
      Recipients: 4
   🚨 EMAIL: simulated
      Recipients: 3
   🚨 PUSH: simulated

----------------------------------------------------------------------

======================================================================
SCENARIO 4: Multi-City Monitoring & Bulk Alerts
======================================================================

📡 Monitoring 4 cities simultaneously...

✅ Lucknow        : Safe            (Confidence: 100.0%)
⚠️ Varanasi       : Warning         (Confidence: 100.0%)
🚨 Gorakhpur      : Critical        (Confidence: 100.0%)
🔴 Ayodhya        : Critical        (Confidence: 100.0%)

📞 Sending alerts to registered users in affected areas...

📱 SIMULATING SMS to 2 recipient(s)
📧 SIMULATING EMAIL to 1 recipient(s)
🔔 SIMULATING PUSH NOTIFICATION

[... continues for other cities ...]

✅ Bulk alert processing complete!
   Total assessments: 4
   Alerts sent: 3
   Cities safe (no alert): 1

======================================================================
                        📊 PHASE 9 SUMMARY
======================================================================

✅ Alert Engine Features Demonstrated:
   • Threshold-based alert triggering
   • SMS notifications (via Twilio)
   • Email alerts (SMTP)
   • Push notifications (simulated)
   • Multi-channel delivery
   • Bulk alerting for multiple locations
   • Alert logging and tracking
```

---

## Message Formats

### SMS Format (160 characters)
```
FLOOD ALERT: CRITICAL - Ayodhya.
EVACUATE IMMEDIATELY! Call 112.
```

**Optimized for:**
- Emergency brevity
- Clear action items
- Under 160 chars (single SMS)

### Email Format
```
Subject: 🚨 🔴 CRITICAL FLOOD ALERT - AYODHYA

FLOOD EARLY WARNING ALERT

Location: Ayodhya
Risk Level: Critical (Level 3)
Severity: Critical
Timestamp: 2025-02-15T16:30:47

CRITICAL FLOOD DANGER in Ayodhya! EVACUATE to higher ground immediately!

RECOMMENDED ACTIONS:
1. 🚨 EVACUATE IMMEDIATELY to designated shelter
2. 🚨 Do NOT wait for further instructions
3. Take ONLY essential items (ID, medications, phone)
...

EMERGENCY CONTACTS:
- National Emergency: 112
- Disaster Management: 1078
...

CRITICAL CONDITIONS DETECTED:
- 🌧️ EXTREME rainfall: 340mm
- 🌊 River at DANGER LEVEL: 13.2m
...
```

### Push Notification
```json
{
  "title": "🔴 CRITICAL FLOOD ALERT - AYODHYA",
  "body": "CRITICAL FLOOD DANGER in Ayodhya! Evacuate immediately!",
  "data": {
    "risk_level": 3,
    "location": "Ayodhya"
  }
}
```

---

## Production Setup (Optional)

### For Real SMS (Twilio)

#### Step 1: Get Twilio Account
1. Visit: **https://www.twilio.com/try-twilio**
2. Sign up (free trial includes $15 credit)
3. Get phone number
4. Copy credentials

#### Step 2: Install Twilio
```powershell
pip install twilio
```

#### Step 3: Add to .env
```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

#### Step 4: Run in Production Mode
```python
from alert_engine import AlertEngine

# Production mode (real SMS)
engine = AlertEngine(demo_mode=False)

# Send real SMS
result = engine.send_alert(
    alert_data,
    phone_numbers=['+919876543210'],
    channels=[AlertChannel.SMS]
)
```

---

### For Real Email (SMTP)

#### Step 1: Gmail Setup
1. Enable 2-Factor Authentication
2. Generate App Password
3. Copy password

#### Step 2: Add to .env
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your.email@gmail.com
EMAIL_PASSWORD=your_app_password_here
```

#### Step 3: Send Real Email
```python
engine = AlertEngine(demo_mode=False)

result = engine.send_alert(
    alert_data,
    email_addresses=['recipient@example.com'],
    channels=[AlertChannel.EMAIL]
)
```

---

## Alert Thresholds

### Default Threshold: Level 1 (Warning)

| Risk Level | Label | Alert Action |
|------------|-------|--------------|
| 0 | Safe | ❌ No alert sent |
| 1 | Warning | ✅ Alert sent |
| 2 | High Risk | ✅ Urgent alert |
| 3 | Critical | ✅ Emergency broadcast |

### Custom Threshold
```python
# Only send for high risk and above
engine.should_send_alert(risk_level, threshold=2)
```

---

## Integration with API

Add alert endpoints to your FastAPI:

```python
# In main.py
from alert_engine import AlertEngine, AlertChannel

# Initialize
alert_engine = AlertEngine(demo_mode=True)

@app.post("/send-alert")
async def send_alert(
    alert_data: dict,
    phone_numbers: List[str] = None,
    email_addresses: List[str] = None
):
    """Send alert via multiple channels"""
    
    result = alert_engine.send_alert(
        alert_data,
        phone_numbers=phone_numbers,
        email_addresses=email_addresses,
        channels=[AlertChannel.ALL]
    )
    
    return result
```

---

## Use Cases

### Use Case 1: Single City Alert
```python
from alert_engine import AlertEngine
from flood_assessment import FloodRiskAssessor

engine = AlertEngine(demo_mode=True)
assessor = FloodRiskAssessor()

# Get assessment
assessment = assessor.assess_flood_risk(features, "Mumbai")

# Send if needed
if engine.should_send_alert(assessment['risk_level']):
    engine.send_alert(
        assessment,
        phone_numbers=['+919876543210'],
        email_addresses=['admin@mumbai.gov.in']
    )
```

### Use Case 2: Scheduled Monitoring
```python
import schedule
import time

def check_all_cities():
    cities = ['Mumbai', 'Delhi', 'Kolkata', 'Chennai']
    
    for city in cities:
        # Fetch weather
        weather = weather_client.get_current_weather(city)
        features = weather_client.transform_to_features(weather, city)
        
        # Assess risk
        assessment = assessor.assess_flood_risk(features, city)
        
        # Send alert if needed
        if engine.should_send_alert(assessment['risk_level']):
            engine.send_alert(assessment, ...)

# Run every hour
schedule.every().hour.do(check_all_cities)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Use Case 3: User Subscription System
```python
# User database
users = {
    'user1': {
        'phone': '+919876543210',
        'email': 'user1@example.com',
        'locations': ['Mumbai', 'Pune']
    },
    'user2': {
        'phone': '+918765432109',
        'email': 'user2@example.com',
        'locations': ['Delhi']
    }
}

# Send alerts to subscribed users
for user_id, user_info in users.items():
    for location in user_info['locations']:
        assessment = get_assessment_for_location(location)
        
        if engine.should_send_alert(assessment['risk_level']):
            engine.send_alert(
                assessment,
                phone_numbers=[user_info['phone']],
                email_addresses=[user_info['email']]
            )
```

---

## For Your Hackathon Presentation

### Demo Script

**Step 1: Run the demo**
```powershell
python run_phase9.py
```

**Step 2: Explain the scenarios**
> "Watch as the system evaluates 4 different scenarios - from safe conditions to critical emergencies..."

**Step 3: Highlight the alerts**
> "For the critical scenario, notice how the system immediately broadcasts alerts via SMS, email, and push notifications..."

**Step 4: Show multi-city**
> "The system can monitor multiple cities simultaneously and send targeted alerts only to affected areas..."

### Key Talking Points

> **"Our alert engine uses intelligent thresholds - safe conditions don't spam users, but critical floods trigger immediate emergency broadcasts..."**

> **"We support multiple channels for redundancy - if one fails, others ensure the message gets through..."**

> **"SMS messages are optimized to 160 characters for instant delivery, while emails provide full details..."**

> **"The system integrates with Twilio for SMS and SMTP for email - production-ready with real credentials..."**

> **"Alert logging tracks every notification sent, providing audit trails for disaster response coordination..."**

---

## Verification Checklist

After running Phase 9:

- [ ] Ran `python run_phase9.py` successfully
- [ ] Saw 4 scenarios (Safe, Warning, Critical, Multi-city)
- [ ] Simulated SMS messages displayed
- [ ] Simulated emails displayed
- [ ] Push notifications displayed
- [ ] Bulk alerts processed correctly
- [ ] Alert log displayed

---

## What's Next?

After Phase 9 is complete, you have:
- ✅ Complete ML pipeline
- ✅ REST API backend
- ✅ Risk scoring system
- ✅ Live weather integration
- ✅ **Multi-channel alert delivery** 🆕

**Your system can now:**
1. Fetch live weather data
2. Predict flood risk
3. Generate actionable alerts
4. **Send SMS/Email/Push notifications** 🆕
5. Monitor multiple cities
6. All automatically!

**Next:** Phase 10 - Dashboard Frontend
- Visual interface for monitoring
- Interactive maps
- Real-time risk display
- Alert history
- Manual prediction input

---

## Quick Reference

### Run Demo
```powershell
python run_phase9.py
```

### Test Alert Engine Only
```powershell
python alert_engine.py
```

### Production Setup
```powershell
# Install Twilio
pip install twilio

# Add credentials to .env
notepad ..\..\. env
```

---

**Ready to see your alert system in action?** Run `python run_phase9.py` and watch notifications get delivered! 🚨📱📧