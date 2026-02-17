"""
Synthetic Flood Data Generator
Generates realistic flood prediction training data based on domain knowledge
"""

import numpy as np
import pandas as pd
import os
from pathlib import Path

# Set random seed for reproducibility
np.random.seed(42)

def generate_flood_data(n_samples: int = 2000) -> pd.DataFrame:
    """
    Generate synthetic flood prediction dataset with realistic correlations
    
    Args:
        n_samples: Number of data samples to generate
        
    Returns:
        DataFrame with features and target variable
    """
    
    print(f"🌊 Generating {n_samples} synthetic flood scenarios...")
    data = []
    
    for i in range(n_samples):
        # Show progress
        if (i + 1) % 500 == 0:
            print(f"   Generated {i + 1}/{n_samples} samples...")
        
        # Randomly select a risk scenario
        scenario = np.random.choice(['safe', 'warning', 'high_risk', 'critical'], 
                                   p=[0.4, 0.3, 0.2, 0.1])  # More safe cases than critical
        
        if scenario == 'safe':
            # Safe conditions: low rainfall, normal river levels
            rainfall_mm = np.random.uniform(0, 50)
            rainfall_7day_avg = np.random.uniform(0, 40)
            rainfall_intensity = np.random.uniform(0, 5)
            river_level_m = np.random.uniform(1, 5)
            river_level_change = np.random.uniform(-0.5, 0.3)
            soil_moisture = np.random.uniform(20, 60)
            elevation = np.random.uniform(100, 500)
            distance_to_river = np.random.uniform(3, 20)
            flood_risk = 0
            
        elif scenario == 'warning':
            # Warning: moderate rainfall, rising water
            rainfall_mm = np.random.uniform(50, 120)
            rainfall_7day_avg = np.random.uniform(40, 80)
            rainfall_intensity = np.random.uniform(5, 12)
            river_level_m = np.random.uniform(5, 8)
            river_level_change = np.random.uniform(0.3, 1.0)
            soil_moisture = np.random.uniform(60, 75)
            elevation = np.random.uniform(50, 150)
            distance_to_river = np.random.uniform(1.5, 5)
            flood_risk = 1
            
        elif scenario == 'high_risk':
            # High risk: heavy rainfall, high river levels
            rainfall_mm = np.random.uniform(120, 200)
            rainfall_7day_avg = np.random.uniform(80, 140)
            rainfall_intensity = np.random.uniform(12, 20)
            river_level_m = np.random.uniform(8, 11)
            river_level_change = np.random.uniform(1.0, 2.5)
            soil_moisture = np.random.uniform(75, 90)
            elevation = np.random.uniform(20, 80)
            distance_to_river = np.random.uniform(0.5, 2.5)
            flood_risk = 2
            
        else:  # critical
            # Critical: extreme rainfall, flooding imminent
            rainfall_mm = np.random.uniform(200, 450)
            rainfall_7day_avg = np.random.uniform(140, 250)
            rainfall_intensity = np.random.uniform(20, 45)
            river_level_m = np.random.uniform(11, 14)
            river_level_change = np.random.uniform(2.5, 4.5)
            soil_moisture = np.random.uniform(85, 98)
            elevation = np.random.uniform(5, 40)
            distance_to_river = np.random.uniform(0.1, 1.5)
            flood_risk = 3
        
        # Weather conditions (less directly correlated with flood)
        temperature = np.random.uniform(18, 35)
        humidity = np.random.uniform(60, 95)
        wind_speed = np.random.uniform(5, 40)
        
        # Month (monsoon season June-Sept has higher risk)
        if scenario in ['high_risk', 'critical']:
            month = np.random.choice([6, 7, 8, 9], p=[0.3, 0.3, 0.25, 0.15])
        else:
            month = np.random.randint(1, 13)
        
        # Create data row
        data.append({
            'rainfall_mm': round(rainfall_mm, 2),
            'rainfall_7day_avg': round(rainfall_7day_avg, 2),
            'rainfall_intensity': round(rainfall_intensity, 2),
            'river_level_m': round(river_level_m, 2),
            'river_level_change': round(river_level_change, 2),
            'soil_moisture_percent': round(soil_moisture, 2),
            'elevation_m': round(elevation, 2),
            'temperature_celsius': round(temperature, 2),
            'humidity_percent': round(humidity, 2),
            'wind_speed_kmh': round(wind_speed, 2),
            'distance_to_river_km': round(distance_to_river, 2),
            'month': int(month),
            'flood_risk': int(flood_risk)
        })
    
    df = pd.DataFrame(data)
    
    # Shuffle the dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    print(f"✅ Generated {len(df)} samples successfully!")
    return df


def save_dataset(df: pd.DataFrame, filepath: str):
    """Save dataset to CSV"""
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    df.to_csv(filepath, index=False)
    print(f"\n✅ Dataset saved to: {filepath}")
    print(f"   Shape: {df.shape}")
    print(f"   Size: {os.path.getsize(filepath) / 1024:.2f} KB")


def display_dataset_stats(df: pd.DataFrame):
    """Display statistics about the generated dataset"""
    print("\n" + "="*70)
    print(" "*20 + "DATASET STATISTICS")
    print("="*70)
    
    print(f"\n📊 Total samples: {len(df)}")
    
    print("\n🎯 Risk Level Distribution:")
    risk_counts = df['flood_risk'].value_counts().sort_index()
    risk_labels = {0: 'Safe', 1: 'Warning', 2: 'High Risk', 3: 'Critical'}
    for risk_level, count in risk_counts.items():
        percentage = (count / len(df)) * 100
        bar = "█" * int(percentage / 2)
        print(f"  Level {risk_level} ({risk_labels[risk_level]:10s}): {count:4d} samples ({percentage:5.1f}%) {bar}")
    
    print("\n📏 Feature Ranges:")
    feature_display = [
        'rainfall_mm', 'river_level_m', 'soil_moisture_percent', 
        'elevation_m', 'distance_to_river_km'
    ]
    for col in feature_display:
        print(f"  {col:25s}: {df[col].min():7.2f} - {df[col].max():7.2f}")
    
    print("\n🔍 Sample Data (first 3 rows):")
    print(df.head(3).to_string(index=False))
    
    print("\n" + "="*70)


if __name__ == "__main__":
    print("\n" + "="*70)
    print(" "*15 + "🌊 FLOOD DATA GENERATOR 🌊")
    print("="*70 + "\n")
    
    # Determine the correct path (works from src/ml or project root)
    if os.path.exists('data'):
        output_path = "data/raw/flood_data.csv"
    else:
        output_path = "../../data/raw/flood_data.csv"
    
    # Generate dataset
    df = generate_flood_data(n_samples=2000)
    
    # Display statistics
    display_dataset_stats(df)
    
    # Save to file
    save_dataset(df, output_path)
    
    print("\n✅ Data generation complete!")
    print("📁 File location: " + output_path)
    print("🚀 Ready for Phase 4 (Data Preprocessing)")
    print("\n" + "="*70 + "\n")