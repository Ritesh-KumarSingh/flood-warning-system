# Phase 3: Data Collection - Instructions

## Overview
Generate a complete synthetic flood prediction dataset with 2,000 realistic samples.

## Files Created
- `schema.py` - Feature definitions and risk level mappings
- `generate_data.py` - Synthetic data generator
- `validate_data.py` - Data quality validation
- `visualize_data.py` - Create charts and plots
- `run_phase3.py` - Master script (runs everything)

## Quick Start (Recommended)

### Option 1: Run Everything at Once
```powershell
# Navigate to src/ml directory
cd E:\disaster_management\disaster-warning-platform\src\ml

# Activate virtual environment (if not already active)
..\..\venv\Scripts\Activate.ps1

# Run the master script
python run_phase3.py
```

This will:
1. Generate 2,000 flood scenarios
2. Validate data quality
3. Create 6 visualization charts
4. Save everything to appropriate folders

---

## Option 2: Run Step by Step

### Step 1: Generate Data
```powershell
cd src\ml
python generate_data.py
```
**Output:** `data/raw/flood_data.csv` (2,000 samples)

### Step 2: Validate Data
```powershell
python validate_data.py
```
**Output:** Validation report in terminal

### Step 3: Create Visualizations
```powershell
python visualize_data.py
```
**Output:** 6 PNG charts in `outputs/` folder

---

## Expected Output Files

### Data Files
```
data/
└── raw/
    └── flood_data.csv        (2,000 samples, ~120 KB)
```

### Visualization Files
```
outputs/
├── risk_distribution.png     (Bar chart of risk levels)
├── feature_distributions.png (Histograms by risk)
├── correlation_heatmap.png   (Feature correlations)
├── box_plots.png             (Box plots by risk)
├── rainfall_vs_river.png     (Scatter plot)
└── monthly_distribution.png  (Seasonal patterns)
```

---

## Dataset Specifications

### Size
- **Total samples:** 2,000
- **Features:** 12
- **Target classes:** 4 (Safe, Warning, High Risk, Critical)

### Class Distribution
- Safe (0): ~40% (800 samples)
- Warning (1): ~30% (600 samples)
- High Risk (2): ~20% (400 samples)
- Critical (3): ~10% (200 samples)

### Features
1. rainfall_mm - Rainfall in last 24 hours
2. rainfall_7day_avg - 7-day average rainfall
3. rainfall_intensity - Current rainfall rate
4. river_level_m - Current river water level
5. river_level_change - Change in river level (6h)
6. soil_moisture_percent - Soil saturation level
7. elevation_m - Location elevation
8. temperature_celsius - Current temperature
9. humidity_percent - Relative humidity
10. wind_speed_kmh - Wind speed
11. distance_to_river_km - Distance to water body
12. month - Month of year (1-12)

**Target:** flood_risk (0=Safe, 1=Warning, 2=High Risk, 3=Critical)

---

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'matplotlib'"
**Solution:** Install missing packages
```powershell
pip install matplotlib seaborn
```

### Problem: "FileNotFoundError: data/raw/"
**Solution:** Run from correct directory
```powershell
# Make sure you're in src/ml/
cd E:\disaster_management\disaster-warning-platform\src\ml
```

### Problem: Matplotlib display errors
**Solution:** Visualizations save to files anyway, so you can ignore display warnings

---

## Verification Checklist

✅ Check that `data/raw/flood_data.csv` exists  
✅ Open CSV and verify 2,000 rows + 13 columns  
✅ Check that `outputs/` folder has 6 PNG files  
✅ Open one visualization to confirm it looks good  

---

## What's Next?

After Phase 3 is complete, you'll have:
- ✅ Complete training dataset (2,000 samples)
- ✅ Validated data quality
- ✅ Visual analysis charts

**Next:** Phase 4 - Data Preprocessing
- Load and clean data
- Normalize features
- Split train/test sets
- Prepare for model training

---

## Quick Test

Run this to test if everything works:
```powershell
python schema.py
```

You should see feature names and risk level mappings.