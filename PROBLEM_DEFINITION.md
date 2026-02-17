# PHASE 2: Problem Definition - Complete Specification

## 1. MACHINE LEARNING PROBLEM

### Problem Type
**Supervised Multi-Class Classification**

### Formal Problem Statement
```
Given: X = {x1, x2, ..., x12} (12 environmental features)
Predict: y ∈ {0, 1, 2, 3} (4 flood risk levels)

Where:
- y = 0: Safe (no flood risk)
- y = 1: Warning (moderate risk)
- y = 2: High Risk (significant danger)
- y = 3: Critical (immediate danger)
```

### Business Objective
Predict flood risk 24-48 hours in advance to enable:
- Early evacuation
- Emergency resource allocation
- Public safety alerts
- Damage mitigation

---

## 2. INPUT FEATURES (12 Features)

### Feature Categories

**A. Rainfall Features (3)**
1. `rainfall_mm` - Recent rainfall amount
2. `rainfall_7day_avg` - Sustained rainfall pattern
3. `rainfall_intensity` - Current rainfall rate

**B. Hydrological Features (2)**
4. `river_level_m` - Current water level
5. `river_level_change` - Water level trend

**C. Soil & Terrain (2)**
6. `soil_moisture_percent` - Ground saturation
7. `elevation_m` - Location height

**D. Weather Conditions (3)**
8. `temperature_celsius` - Atmospheric temperature
9. `humidity_percent` - Air moisture
10. `wind_speed_kmh` - Wind conditions

**E. Geographic & Temporal (2)**
11. `distance_to_river_km` - Proximity to water
12. `month` - Seasonal context

---

## 3. OUTPUT SPECIFICATION

### Target Variable: `flood_risk`

| Level | Label      | Probability Range | Action Required                    |
|-------|------------|-------------------|-------------------------------------|
| 0     | Safe       | 0.0 - 0.3         | Normal activities                  |
| 1     | Warning    | 0.3 - 0.6         | Monitor & prepare                  |
| 2     | High Risk  | 0.6 - 0.8         | Prepare evacuation                 |
| 3     | Critical   | 0.8 - 1.0         | Immediate evacuation               |

### Model Output Format
```python
{
    "risk_level": 2,  # Integer 0-3
    "risk_label": "High Risk",  # String label
    "probability": 0.73,  # Float 0-1
    "confidence": 0.89,  # Model confidence
    "alert_message": "High flood risk expected...",
    "recommended_action": "Prepare to evacuate..."
}
```

---

## 4. DATA REQUIREMENTS

### Minimum Dataset Size
- Training: 1,500+ samples
- Testing: 500+ samples
- **Total: 2,000+ samples recommended**

### Class Distribution (Target Balance)
- Safe (0): ~40% (800 samples)
- Warning (1): ~30% (600 samples)
- High Risk (2): ~20% (400 samples)
- Critical (3): ~10% (200 samples)

### Data Quality Criteria
✅ No missing values in critical features
✅ Values within specified ranges
✅ Temporal consistency (month = 1-12)
✅ Logical correlations (e.g., high rain → high soil moisture)

---

## 5. SUCCESS METRICS

### Primary Metrics
1. **Accuracy**: Overall prediction correctness (target: >85%)
2. **Precision**: Avoid false alarms (target: >80%)
3. **Recall**: Catch real disasters (target: >90% for Critical class)
4. **F1-Score**: Balance precision/recall (target: >85%)

### Critical Metric: Recall for Critical Class
- **Missing a critical flood = catastrophic**
- Better to have false positives than false negatives
- Recall for Critical (class 3) must be >90%

### Confusion Matrix Goals
```
Priority: Minimize False Negatives in Critical class
Acceptable: Some False Positives in Safe→Warning
```

---

## 6. MODEL CONSTRAINTS

### Real-Time Requirements
- Prediction latency: <100ms
- Model size: <50MB (for mobile deployment)
- Memory usage: <500MB RAM

### Deployment Environment
- Backend server (FastAPI)
- Mobile app (potential future)
- Edge devices (Raspberry Pi compatible)

---

## 7. DOMAIN KNOWLEDGE RULES

### Critical Thresholds (Immediate Red Flags)
```python
IF rainfall_mm > 200 mm → HIGH RISK
IF river_level_m > 11 m → CRITICAL
IF soil_moisture > 90% AND rainfall_intensity > 15 → CRITICAL
IF distance_to_river < 0.5 km AND river_level > 10 → CRITICAL
```

### Feature Correlations (Expected)
- High rainfall → High soil moisture
- Rising river level → Increasing flood risk
- Monsoon months (Jun-Sep) → Higher baseline risk
- Low elevation + proximity to river → Higher vulnerability

---

## 8. DATA SCHEMA (CSV Format)

### Column Order
```
rainfall_mm,rainfall_7day_avg,rainfall_intensity,river_level_m,
river_level_change,soil_moisture_percent,elevation_m,
temperature_celsius,humidity_percent,wind_speed_kmh,
distance_to_river_km,month,flood_risk
```

### Example Row (High Risk)
```csv
145.5,95.2,15.3,9.2,1.5,85.3,50.2,25.1,88.4,8.2,1.2,8,2
```

---

## 9. VALIDATION STRATEGY

### Train-Test Split
- Training: 80% (1,600 samples)
- Testing: 20% (400 samples)
- Stratified split (maintain class distribution)

### Cross-Validation
- 5-fold stratified CV during training
- Ensures robust performance across data splits

---

## 10. NEXT STEPS (Phase 3)

1. ✅ Generate or collect dataset (2,000+ samples)
2. ✅ Validate data quality
3. ✅ Save to `data/raw/flood_data.csv`
4. → Proceed to Phase 3: Data Preprocessing

---

## 11. HACKATHON QUICK REFERENCE

### What We're Building
"AI system that predicts flood risk 24-48 hours ahead using weather and environmental data"

### Key Innovation
"Real-time multi-factor risk assessment with actionable alerts"

### Impact Statement
"Early warnings can reduce flood casualties by 80% and damage by 30%"

### Demo Flow
```
Input: Current weather data
↓
ML Model: Random Forest classification
↓
Output: Risk level + probability + alert message
↓
Dashboard: Visual risk map + recommendations
```