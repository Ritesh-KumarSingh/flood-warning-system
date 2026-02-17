"""
Data Validation Script
Checks the quality and consistency of the generated flood dataset
"""

import pandas as pd
import numpy as np
from schema import FEATURE_NAMES, TARGET_NAME, FEATURE_RANGES

def validate_dataset(filepath: str) -> bool:
    """
    Validate the flood dataset for quality and consistency
    
    Args:
        filepath: Path to the CSV dataset
        
    Returns:
        True if validation passes, False otherwise
    """
    print("\n" + "="*70)
    print(" "*20 + "🔍 DATA VALIDATION")
    print("="*70 + "\n")
    
    # Load dataset
    print("📂 Loading dataset...")
    try:
        df = pd.read_csv(filepath)
        print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
    except FileNotFoundError:
        print(f"❌ ERROR: File not found at {filepath}")
        return False
    except Exception as e:
        print(f"❌ ERROR loading file: {e}")
        return False
    
    all_passed = True
    
    # Test 1: Check column names
    print("\n1️⃣  Checking column names...")
    expected_columns = FEATURE_NAMES + [TARGET_NAME]
    if list(df.columns) == expected_columns:
        print("   ✅ All columns present and in correct order")
    else:
        print("   ❌ Column mismatch!")
        print(f"   Expected: {expected_columns}")
        print(f"   Found: {list(df.columns)}")
        all_passed = False
    
    # Test 2: Check for missing values
    print("\n2️⃣  Checking for missing values...")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("   ✅ No missing values found")
    else:
        print("   ❌ Missing values detected:")
        for col, count in missing[missing > 0].items():
            print(f"      {col}: {count} missing")
        all_passed = False
    
    # Test 3: Check value ranges
    print("\n3️⃣  Checking value ranges...")
    range_errors = []
    for feature, (min_val, max_val) in FEATURE_RANGES.items():
        if feature in df.columns:
            actual_min = df[feature].min()
            actual_max = df[feature].max()
            
            if actual_min < min_val or actual_max > max_val:
                range_errors.append(
                    f"      {feature}: [{actual_min:.2f}, {actual_max:.2f}] "
                    f"(expected [{min_val}, {max_val}])"
                )
    
    if not range_errors:
        print("   ✅ All features within expected ranges")
    else:
        print("   ⚠️  Some features outside expected ranges:")
        for error in range_errors:
            print(error)
        # This is a warning, not a failure
    
    # Test 4: Check target variable
    print("\n4️⃣  Checking target variable...")
    unique_targets = sorted(df[TARGET_NAME].unique())
    expected_targets = [0, 1, 2, 3]
    if unique_targets == expected_targets:
        print(f"   ✅ Target has correct classes: {unique_targets}")
    else:
        print(f"   ❌ Target classes incorrect!")
        print(f"   Expected: {expected_targets}")
        print(f"   Found: {unique_targets}")
        all_passed = False
    
    # Test 5: Check class distribution
    print("\n5️⃣  Checking class distribution...")
    class_dist = df[TARGET_NAME].value_counts(normalize=True).sort_index()
    print("   Class distribution:")
    risk_labels = {0: 'Safe', 1: 'Warning', 2: 'High Risk', 3: 'Critical'}
    for cls, pct in class_dist.items():
        print(f"      Level {cls} ({risk_labels[cls]:10s}): {pct*100:5.1f}%")
    
    # Check if any class is severely underrepresented
    if (class_dist < 0.05).any():
        print("   ⚠️  Warning: Some classes have <5% representation")
    else:
        print("   ✅ All classes reasonably represented")
    
    # Test 6: Check data types
    print("\n6️⃣  Checking data types...")
    type_errors = []
    for feature in FEATURE_NAMES:
        if feature == 'month':
            if df[feature].dtype not in [np.int64, np.int32]:
                type_errors.append(f"      {feature}: {df[feature].dtype} (expected int)")
        else:
            if df[feature].dtype not in [np.float64, np.int64, np.int32]:
                type_errors.append(f"      {feature}: {df[feature].dtype} (expected float)")
    
    if not type_errors:
        print("   ✅ All data types correct")
    else:
        print("   ❌ Data type errors:")
        for error in type_errors:
            print(error)
        all_passed = False
    
    # Test 7: Check for duplicates
    print("\n7️⃣  Checking for duplicate rows...")
    duplicates = df.duplicated().sum()
    if duplicates == 0:
        print("   ✅ No duplicate rows found")
    else:
        print(f"   ⚠️  Found {duplicates} duplicate rows")
    
    # Test 8: Logical consistency checks
    print("\n8️⃣  Checking logical consistency...")
    consistency_issues = []
    
    # High rainfall should correlate with high soil moisture
    high_rain = df[df['rainfall_mm'] > 150]
    if len(high_rain) > 0:
        low_moisture = high_rain[high_rain['soil_moisture_percent'] < 50]
        if len(low_moisture) > len(high_rain) * 0.1:  # More than 10% anomalies
            consistency_issues.append(
                f"      {len(low_moisture)} samples have high rainfall but low soil moisture"
            )
    
    # Critical risk should have high rainfall or river level
    critical = df[df['flood_risk'] == 3]
    if len(critical) > 0:
        low_indicators = critical[
            (critical['rainfall_mm'] < 100) & 
            (critical['river_level_m'] < 8)
        ]
        if len(low_indicators) > 0:
            consistency_issues.append(
                f"      {len(low_indicators)} critical samples lack high rainfall/river level"
            )
    
    if not consistency_issues:
        print("   ✅ Data appears logically consistent")
    else:
        print("   ⚠️  Potential consistency issues:")
        for issue in consistency_issues:
            print(issue)
    
    # Final summary
    print("\n" + "="*70)
    if all_passed:
        print("✅ VALIDATION PASSED - Dataset is ready for training!")
    else:
        print("⚠️  VALIDATION COMPLETED WITH WARNINGS - Review issues above")
    print("="*70 + "\n")
    
    return all_passed


if __name__ == "__main__":
    import os
    
    # Determine the correct path
    if os.path.exists('data'):
        filepath = "data/raw/flood_data.csv"
    else:
        filepath = "../../data/raw/flood_data.csv"
    
    validate_dataset(filepath)