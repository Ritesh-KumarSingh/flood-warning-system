"""
Example: Working with Preprocessed Data
Demonstrates how to load and use the processed datasets
"""

import pandas as pd
import numpy as np
from data_loader import load_preprocessed_data
from schema import FEATURE_NAMES, TARGET_NAME, get_risk_info

def example_data_exploration():
    """Example of exploring preprocessed data"""
    
    print("\n" + "="*70)
    print(" "*15 + "📚 PREPROCESSED DATA EXAMPLES")
    print("="*70 + "\n")
    
    # Load preprocessed data
    data = load_preprocessed_data()
    
    X_train = data['X_train']
    y_train = data['y_train']
    X_test = data['X_test']
    y_test = data['y_test']
    scaler = data['scaler']
    
    # Example 1: View sample rows
    print("1️⃣  Sample Training Data (first 3 rows):")
    print("-" * 70)
    sample_df = pd.concat([X_train.head(3), y_train.head(3)], axis=1)
    print(sample_df.to_string())
    print()
    
    # Example 2: Feature statistics
    print("2️⃣  Feature Statistics (Training Set):")
    print("-" * 70)
    stats = X_train.describe().loc[['mean', 'std', 'min', 'max']]
    print(stats.to_string())
    print()
    
    # Example 3: Class distribution
    print("3️⃣  Target Class Distribution:")
    print("-" * 70)
    risk_labels = {0: 'Safe', 1: 'Warning', 2: 'High Risk', 3: 'Critical'}
    
    print("\nTraining Set:")
    for level in [0, 1, 2, 3]:
        count = (y_train == level).sum()
        percentage = count / len(y_train) * 100
        info = get_risk_info(level)
        print(f"   {info['label']:12s} (Level {level}): {count:4d} samples ({percentage:5.1f}%)")
    
    print("\nTest Set:")
    for level in [0, 1, 2, 3]:
        count = (y_test == level).sum()
        percentage = count / len(y_test) * 100
        info = get_risk_info(level)
        print(f"   {info['label']:12s} (Level {level}): {count:4d} samples ({percentage:5.1f}%)")
    
    # Example 4: Correlation analysis
    print("\n4️⃣  Top Feature Correlations with Target:")
    print("-" * 70)
    
    # Combine features and target for correlation
    full_train = X_train.copy()
    full_train[TARGET_NAME] = y_train
    
    correlations = full_train.corr()[TARGET_NAME].drop(TARGET_NAME)
    top_correlations = correlations.abs().sort_values(ascending=False).head(5)
    
    print("\nMost correlated features with flood risk:")
    for feature, corr in top_correlations.items():
        direction = "↑" if correlations[feature] > 0 else "↓"
        print(f"   {feature:25s}: {correlations[feature]:+.3f} {direction}")
    
    # Example 5: Using the scaler on new data
    print("\n5️⃣  Example: Transforming New Data with Scaler:")
    print("-" * 70)
    
    # Create a fake "new" data point
    new_data_raw = {
        'rainfall_mm': 150.0,
        'rainfall_7day_avg': 95.0,
        'rainfall_intensity': 15.0,
        'river_level_m': 9.5,
        'river_level_change': 1.8,
        'soil_moisture_percent': 85.0,
        'elevation_m': 45.0,
        'temperature_celsius': 26.0,
        'humidity_percent': 88.0,
        'wind_speed_kmh': 12.0,
        'distance_to_river_km': 1.2,
        'month': 7
    }
    
    print("\nRaw input values:")
    for feature, value in new_data_raw.items():
        print(f"   {feature:25s}: {value:8.2f}")
    
    # Transform using saved scaler
    new_data_df = pd.DataFrame([new_data_raw])
    new_data_scaled = scaler.transform(new_data_df)
    new_data_scaled_df = pd.DataFrame(new_data_scaled, columns=FEATURE_NAMES)
    
    print("\nNormalized values (ready for model):")
    for idx, feature in enumerate(FEATURE_NAMES):
        print(f"   {feature:25s}: {new_data_scaled[0][idx]:8.4f}")
    
    # Example 6: Data shapes summary
    print("\n6️⃣  Data Shapes Summary:")
    print("-" * 70)
    print(f"\n   Training features (X_train): {X_train.shape}")
    print(f"   Training target (y_train):   {y_train.shape}")
    print(f"   Test features (X_test):      {X_test.shape}")
    print(f"   Test target (y_test):        {y_test.shape}")
    print(f"\n   Total features: {X_train.shape[1]}")
    print(f"   Total training samples: {X_train.shape[0]}")
    print(f"   Total test samples: {X_test.shape[0]}")
    
    print("\n" + "="*70)
    print("✅ Example exploration complete!")
    print("\n💡 This data is now ready for model training (Phase 5)")
    print("="*70 + "\n")


if __name__ == "__main__":
    example_data_exploration()