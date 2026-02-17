# Phase 4: Data Preprocessing - Instructions

## Overview
Transform raw flood data into clean, normalized, ML-ready format for model training.

## Prerequisites
✅ Phase 3 must be complete (flood_data.csv must exist in data/raw/)

## Files Created
- `data_preprocessing.py` - Main preprocessing pipeline
- `data_loader.py` - Helper to load processed data
- `visualize_preprocessing.py` - Visualization of preprocessing effects
- `run_phase4.py` - Master script (runs everything)

---

## Quick Start (Recommended)

### Run Everything at Once
```powershell
# Navigate to src/ml directory
cd E:\disaster_management\disaster-warning-platform\src\ml

# Activate virtual environment (if not already active)
..\..\venv\Scripts\Activate.ps1

# Run the master script
python run_phase4.py
```

**Runtime:** ~10-15 seconds

---

## What Phase 4 Does

### 1. Data Validation
- ✅ Checks for missing values
- ✅ Validates feature ranges
- ✅ Clips outliers to valid ranges

### 2. Feature Normalization
- ✅ Applies StandardScaler (mean=0, std=1)
- ✅ Fits on training data only
- ✅ Transforms test data with same scaler

### 3. Train-Test Split
- ✅ 80% training, 20% testing
- ✅ Stratified split (maintains class distribution)
- ✅ Random seed=42 for reproducibility

### 4. Data Export
- ✅ Saves train.csv and test.csv
- ✅ Saves scaler.pkl for future predictions
- ✅ Saves preprocessing metadata (JSON)

### 5. Visualization
- ✅ Shows normalization effects
- ✅ Displays train/test split
- ✅ Compares before/after feature scales

---

## Expected Output Files

### Processed Data Files
```
data/
└── processed/
    ├── train.csv                    (~1,600 samples)
    ├── test.csv                     (~400 samples)
    ├── scaler.pkl                   (StandardScaler object)
    └── preprocessing_metadata.json  (Processing info)
```

### Visualization Files
```
outputs/
├── normalization_effect.png   (Before/after histograms)
├── train_test_split.png       (Class distribution)
└── feature_scaling.png        (Feature range comparison)
```

---

## Output Specifications

### train.csv
- **Rows:** ~1,600 (80% of 2,000)
- **Columns:** 13 (12 normalized features + 1 target)
- **Features:** All scaled to mean≈0, std≈1
- **Target:** Original values (0, 1, 2, 3)

### test.csv
- **Rows:** ~400 (20% of 2,000)
- **Columns:** 13 (same as train)
- **Features:** Normalized with training scaler
- **Target:** Original values (0, 1, 2, 3)

### scaler.pkl
- **Type:** sklearn.preprocessing.StandardScaler
- **Purpose:** Transform new data for predictions
- **Usage:** 
  ```python
  import joblib
  scaler = joblib.load('data/processed/scaler.pkl')
  new_data_scaled = scaler.transform(new_data)
  ```

---

## Step-by-Step Execution (Advanced)

### Step 1: Run Preprocessing Only
```powershell
cd src\ml
python data_preprocessing.py
```
**Output:** Creates train.csv, test.csv, scaler.pkl

### Step 2: Load and Verify Data
```powershell
python data_loader.py
```
**Output:** Displays data statistics

### Step 3: Create Visualizations
```powershell
python visualize_preprocessing.py
```
**Output:** Creates 3 PNG charts

---

## Understanding the Output

### Console Output Example
```
======================================================================
                   🔧 DATA PREPROCESSING PIPELINE
======================================================================

📂 Loading data from data/raw/flood_data.csv...
✅ Loaded 2000 samples with 13 columns

🔍 Checking for missing values...
✅ No missing values found

📏 Validating feature ranges...
✅ All values within expected ranges

✂️  Splitting features and target...
✅ Features shape: (2000, 12)
✅ Target shape: (2000,)

   Target distribution:
   Level 0 (Safe      ):  802 ( 40.1%)
   Level 1 (Warning   ):  597 ( 29.8%)
   Level 2 (High Risk ):  402 ( 20.1%)
   Level 3 (Critical  ):  199 ( 10.0%)

🔀 Splitting data (train: 80%, test: 20%)...
✅ Training set: 1600 samples
✅ Test set: 400 samples

🔧 Normalizing features...
✅ Training data normalized
   Mean: 0.0000
   Std:  1.0000
✅ Test data normalized with same scaler

💾 Saving processed data to data/processed...
✅ Saved training set: data/processed/train.csv
✅ Saved test set: data/processed/test.csv
✅ Saved scaler: data/processed/scaler.pkl
✅ Saved metadata: data/processed/preprocessing_metadata.json

======================================================================
✅ PREPROCESSING COMPLETE!
======================================================================
```

---

## Normalization Explained

### Before Normalization (Raw Data)
```
rainfall_mm:        0 - 450    (wide range)
river_level_m:      1 - 14     (different scale)
soil_moisture_%:    20 - 98    (another scale)
elevation_m:        5 - 500    (very wide range)
```

### After Normalization (StandardScaler)
```
All features transformed to:
Mean ≈ 0
Std  ≈ 1
Range: typically -3 to +3
```

**Why normalize?**
- ✅ Prevents features with large ranges from dominating
- ✅ Improves model convergence speed
- ✅ Makes features comparable
- ✅ Required for many ML algorithms

---

## Verification Checklist

After running Phase 4:

✅ Check `data/processed/train.csv` exists (should be ~100 KB)  
✅ Check `data/processed/test.csv` exists (should be ~25 KB)  
✅ Check `data/processed/scaler.pkl` exists  
✅ Open train.csv - verify all feature values are small (-3 to +3)  
✅ Open test.csv - verify target column has values 0, 1, 2, 3  
✅ Check outputs folder has 3 new PNG files  

---

## Quick Test

Verify preprocessing worked correctly:
```powershell
python data_loader.py
```

**Expected output:**
```
📂 Loading preprocessed data from data/processed...
✅ Loaded training data: (1600, 13)
✅ Loaded test data: (400, 13)
✅ Loaded scaler

📊 Data Summary:
   Features: 12
   Training samples: 1600
   Test samples: 400
   Target classes: [0, 1, 2, 3]
```

---

## Troubleshooting

### Problem: "FileNotFoundError: flood_data.csv not found"
**Solution:** Run Phase 3 first to generate the dataset
```powershell
cd src\ml
python run_phase3.py
```

### Problem: "All features have same value after normalization"
**Solution:** This shouldn't happen. Check if your raw data has variance:
```powershell
python -c "import pandas as pd; print(pd.read_csv('../../data/raw/flood_data.csv').describe())"
```

### Problem: Visualization errors
**Solution:** Visualizations are optional. Your data is still processed correctly even if charts fail to generate.

---

## Data Science Notes

### Why 80/20 Split?
- **80% train:** Enough data for model to learn patterns
- **20% test:** Sufficient for reliable evaluation
- **Stratified:** Maintains class balance in both sets

### Why Stratified Split?
Without stratification:
```
Train: 90% Safe, 10% Critical  ❌ Imbalanced
Test:  50% Safe, 50% Critical  ❌ Different distribution
```

With stratification:
```
Train: 40% Safe, 30% Warning, 20% High, 10% Critical ✅
Test:  40% Safe, 30% Warning, 20% High, 10% Critical ✅
```

### Why Save the Scaler?
When making predictions on new data (Phase 8+), you MUST use the same scaler:
```python
# ❌ WRONG: Create new scaler
scaler = StandardScaler()
new_data_scaled = scaler.fit_transform(new_data)  # Different scaling!

# ✅ CORRECT: Use saved scaler
scaler = joblib.load('scaler.pkl')
new_data_scaled = scaler.transform(new_data)  # Same scaling as training!
```

---

## What's Next?

After Phase 4 is complete, you'll have:
- ✅ Clean, normalized training data (1,600 samples)
- ✅ Clean, normalized test data (400 samples)
- ✅ Saved scaler for future predictions
- ✅ Visualizations showing preprocessing effects

**Next:** Phase 5 - Model Training
- Train Random Forest classifier
- Evaluate performance metrics
- Save trained model
- Generate predictions

---

## Key Takeaways

🎯 **Preprocessing is critical** - Bad data = Bad model  
🎯 **Normalization matters** - Helps model learn better  
🎯 **Save the scaler** - Needed for production predictions  
🎯 **Stratified split** - Maintains class balance  
🎯 **Test set = Future proxy** - Never train on it!  

---

## For Your Hackathon Presentation

Show these visualizations and say:

> "We preprocessed our data using industry-standard techniques:"
> - ✅ StandardScaler normalization
> - ✅ Stratified train-test split
> - ✅ Comprehensive data validation
> - ✅ Preserved class distribution

> "As you can see in this chart, normalization brought all features to the same scale, preventing any single feature from dominating the model..."