"""
Multi-Disaster Dataset Generator
Generates realistic training data for all 5 disaster types:
- Floods
- Earthquakes  
- Cyclones
- Landslides
- Heatwaves
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

def generate_flood_data(n_samples=2000):
    """Generate flood dataset (existing - already accurate)"""
    data = []
    
    for _ in range(n_samples):
        # Generate base conditions
        month = np.random.randint(1, 13)
        is_monsoon = month in [6, 7, 8, 9]
        
        # Rainfall
        if is_monsoon:
            rainfall = np.random.exponential(80) + np.random.uniform(0, 150)
        else:
            rainfall = np.random.exponential(20) + np.random.uniform(0, 50)
        
        rainfall_7day = rainfall * np.random.uniform(0.7, 1.5)
        rainfall_intensity = rainfall / 24 if rainfall > 0 else 0
        
        # River levels
        base_river = np.random.uniform(2, 8)
        river_level = base_river + (rainfall / 50) + np.random.normal(0, 1)
        river_change = (river_level - base_river) / 24
        
        # Soil moisture
        soil_moisture = min(95, 40 + (rainfall / 3) + np.random.uniform(0, 20))
        
        # Geography
        elevation = np.random.exponential(100) + np.random.uniform(10, 200)
        distance_river = np.random.exponential(3) + np.random.uniform(0.5, 10)
        
        # Weather
        temperature = 20 + np.random.normal(8, 4)
        humidity = min(95, 50 + (rainfall / 5) + np.random.uniform(0, 30))
        wind_speed = np.random.exponential(8) + np.random.uniform(5, 25)
        
        # Risk level determination
        risk_score = 0
        if rainfall > 200: risk_score += 3
        elif rainfall > 100: risk_score += 2
        elif rainfall > 50: risk_score += 1
        
        if river_level > 10: risk_score += 3
        elif river_level > 7: risk_score += 2
        elif river_level > 5: risk_score += 1
        
        if soil_moisture > 85: risk_score += 2
        elif soil_moisture > 70: risk_score += 1
        
        if elevation < 30: risk_score += 2
        elif elevation < 60: risk_score += 1
        
        if distance_river < 1: risk_score += 2
        elif distance_river < 3: risk_score += 1
        
        # Map to risk level
        if risk_score >= 10: risk_level = 3  # Critical
        elif risk_score >= 6: risk_level = 2  # High
        elif risk_score >= 3: risk_level = 1  # Warning
        else: risk_level = 0  # Safe
        
        data.append({
            'rainfall_mm': round(rainfall, 2),
            'rainfall_7day_avg': round(rainfall_7day, 2),
            'rainfall_intensity': round(rainfall_intensity, 2),
            'river_level_m': round(river_level, 2),
            'river_level_change': round(river_change, 3),
            'soil_moisture_percent': round(soil_moisture, 1),
            'elevation_m': round(elevation, 1),
            'temperature_celsius': round(temperature, 1),
            'humidity_percent': round(humidity, 1),
            'wind_speed_kmh': round(wind_speed, 1),
            'distance_to_river_km': round(distance_river, 2),
            'month': month,
            'risk_level': risk_level
        })
    
    return pd.DataFrame(data)


def generate_earthquake_data(n_samples=2000):
    """Generate earthquake dataset based on real seismic patterns"""
    data = []
    
    # Define seismic zones in India (1-5, where 5 is highest risk)
    seismic_zones = {
        'zone_5': ['delhi', 'uttarakhand', 'himachal', 'kashmir', 'sikkim', 'assam', 'gujarat'],
        'zone_4': ['punjab', 'haryana', 'bihar', 'west bengal', 'maharashtra', 'meghalaya'],
        'zone_3': ['rajasthan', 'madhya pradesh', 'karnataka', 'goa'],
        'zone_2': ['andhra', 'telangana', 'tamil nadu', 'kerala', 'odisha']
    }
    
    for _ in range(n_samples):
        # Random seismic zone
        zone_choice = np.random.choice([5, 4, 3, 2], p=[0.15, 0.25, 0.35, 0.25])
        seismic_zone = zone_choice
        
        # Seismic features
        ground_acceleration = np.random.exponential(0.1) * seismic_zone  # g-force
        p_wave_velocity = 5.0 + np.random.normal(0, 0.5)  # km/s
        s_wave_velocity = 3.0 + np.random.normal(0, 0.3)  # km/s
        
        # Recent seismic activity (last 30 days)
        recent_quakes = np.random.poisson(seismic_zone * 2)
        max_recent_magnitude = np.random.uniform(2.0, min(seismic_zone + 2, 7.0))
        
        # Geological features
        fault_distance = np.random.exponential(50) + np.random.uniform(5, 100)  # km
        soil_type = np.random.choice([1, 2, 3, 4])  # 1=rock, 4=soft soil
        building_age = np.random.randint(0, 100)  # years
        
        # Depth to bedrock
        bedrock_depth = np.random.exponential(20) + np.random.uniform(5, 50)  # meters
        
        # Historical earthquake count (5 years)
        historical_count = np.random.poisson(seismic_zone * 5)
        
        # Population density (affects risk even with same seismic activity)
        population_density = np.random.exponential(500) + np.random.uniform(100, 5000)
        
        # Time of day (affects casualties)
        hour = np.random.randint(0, 24)
        
        # Month
        month = np.random.randint(1, 13)
        
        # Calculate risk level
        risk_score = 0
        
        # Seismic zone contribution
        if seismic_zone == 5: risk_score += 4
        elif seismic_zone == 4: risk_score += 3
        elif seismic_zone == 3: risk_score += 2
        
        # Recent activity
        if recent_quakes > 10: risk_score += 3
        elif recent_quakes > 5: risk_score += 2
        elif recent_quakes > 2: risk_score += 1
        
        # Fault distance
        if fault_distance < 20: risk_score += 3
        elif fault_distance < 50: risk_score += 2
        elif fault_distance < 100: risk_score += 1
        
        # Soil type (softer = more risk)
        if soil_type == 4: risk_score += 2
        elif soil_type == 3: risk_score += 1
        
        # Ground acceleration
        if ground_acceleration > 0.5: risk_score += 2
        elif ground_acceleration > 0.3: risk_score += 1
        
        # Map to risk level
        if risk_score >= 10: risk_level = 3
        elif risk_score >= 6: risk_level = 2
        elif risk_score >= 3: risk_level = 1
        else: risk_level = 0
        
        data.append({
            'seismic_zone': seismic_zone,
            'ground_acceleration_g': round(ground_acceleration, 3),
            'p_wave_velocity_kms': round(p_wave_velocity, 2),
            's_wave_velocity_kms': round(s_wave_velocity, 2),
            'recent_quakes_30d': recent_quakes,
            'max_recent_magnitude': round(max_recent_magnitude, 1),
            'fault_distance_km': round(fault_distance, 1),
            'soil_type': soil_type,
            'building_age_years': building_age,
            'bedrock_depth_m': round(bedrock_depth, 1),
            'historical_count_5y': historical_count,
            'population_density': round(population_density, 0),
            'hour_of_day': hour,
            'month': month,
            'risk_level': risk_level
        })
    
    return pd.DataFrame(data)


def generate_cyclone_data(n_samples=2000):
    """Generate cyclone dataset based on meteorological patterns"""
    data = []
    
    for _ in range(n_samples):
        # Season (May-June, Oct-Nov are peak)
        month = np.random.randint(1, 13)
        is_cyclone_season = month in [5, 6, 10, 11]
        
        # Sea surface temperature (crucial for cyclone formation)
        if is_cyclone_season:
            sst = np.random.uniform(26, 32)  # Celsius
        else:
            sst = np.random.uniform(20, 28)
        
        # Atmospheric pressure
        if is_cyclone_season:
            pressure = np.random.normal(990, 15)
        else:
            pressure = np.random.normal(1010, 8)
        
        # Wind speed
        base_wind = 20 if is_cyclone_season else 10
        wind_speed = np.random.exponential(base_wind) + np.random.uniform(10, 60)
        
        # Wind shear (vertical wind speed change)
        wind_shear = np.random.exponential(10) + np.random.uniform(0, 30)
        
        # Humidity
        humidity = 60 + np.random.uniform(0, 35)
        
        # Coastal distance
        coastal_distance = np.random.exponential(100) + np.random.uniform(0, 500)
        
        # Latitude (cyclones rare beyond certain latitudes)
        latitude = np.random.uniform(8, 25)  # India range
        
        # Coriolis parameter (latitude effect)
        coriolis = 2 * 7.2921e-5 * np.sin(np.radians(latitude))
        
        # Cloud top temperature
        cloud_temp = -40 + np.random.uniform(-20, 20)
        
        # Vorticity
        vorticity = np.random.exponential(5) * (1 if is_cyclone_season else 0.3)
        
        # Previous cyclone in region (last 30 days)
        previous_cyclone = 1 if np.random.random() < (0.3 if is_cyclone_season else 0.05) else 0
        
        # Calculate risk
        risk_score = 0
        
        # SST
        if sst > 28: risk_score += 3
        elif sst > 26: risk_score += 2
        
        # Pressure
        if pressure < 980: risk_score += 4
        elif pressure < 995: risk_score += 3
        elif pressure < 1005: risk_score += 2
        
        # Wind
        if wind_speed > 120: risk_score += 4
        elif wind_speed > 80: risk_score += 3
        elif wind_speed > 50: risk_score += 2
        elif wind_speed > 30: risk_score += 1
        
        # Season
        if is_cyclone_season: risk_score += 2
        
        # Coastal proximity
        if coastal_distance < 50: risk_score += 3
        elif coastal_distance < 150: risk_score += 2
        elif coastal_distance < 300: risk_score += 1
        
        # Map to risk level
        if risk_score >= 12: risk_level = 3
        elif risk_score >= 7: risk_level = 2
        elif risk_score >= 4: risk_level = 1
        else: risk_level = 0
        
        data.append({
            'sea_surface_temp_c': round(sst, 1),
            'atmospheric_pressure_hpa': round(pressure, 1),
            'wind_speed_kmh': round(wind_speed, 1),
            'wind_shear_kms': round(wind_shear, 1),
            'humidity_percent': round(humidity, 1),
            'coastal_distance_km': round(coastal_distance, 1),
            'latitude': round(latitude, 2),
            'coriolis_parameter': round(coriolis * 1e5, 4),
            'cloud_top_temp_c': round(cloud_temp, 1),
            'vorticity': round(vorticity, 2),
            'previous_cyclone_30d': previous_cyclone,
            'month': month,
            'risk_level': risk_level
        })
    
    return pd.DataFrame(data)


def generate_landslide_data(n_samples=2000):
    """Generate landslide dataset based on terrain and weather"""
    data = []
    
    for _ in range(n_samples):
        # Slope angle (degrees)
        slope_angle = np.random.exponential(15) + np.random.uniform(5, 60)
        
        # Rainfall
        month = np.random.randint(1, 13)
        is_monsoon = month in [6, 7, 8, 9]
        
        if is_monsoon:
            rainfall_24h = np.random.exponential(80) + np.random.uniform(0, 200)
            rainfall_7d = rainfall_24h * np.random.uniform(2, 5)
        else:
            rainfall_24h = np.random.exponential(15) + np.random.uniform(0, 50)
            rainfall_7d = rainfall_24h * np.random.uniform(1, 3)
        
        # Soil properties
        soil_moisture = min(95, 30 + (rainfall_24h / 2) + np.random.uniform(0, 30))
        soil_cohesion = np.random.uniform(5, 50)  # kPa
        soil_friction_angle = np.random.uniform(15, 45)  # degrees
        
        # Vegetation cover (0-100%)
        vegetation = np.random.uniform(0, 100)
        
        # Elevation
        elevation = np.random.uniform(100, 3000)
        
        # Previous landslides in area
        historical_landslides = np.random.poisson(2)
        
        # Soil type (1=rock, 5=loose soil)
        soil_type = np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.2, 0.3, 0.25, 0.15])
        
        # Deforestation indicator
        deforestation = 1 if vegetation < 30 else 0
        
        # Ground water level
        groundwater_depth = np.random.exponential(5) + np.random.uniform(1, 20)
        
        # Seismic activity (can trigger landslides)
        seismic_activity = np.random.choice([0, 1], p=[0.85, 0.15])
        
        # Calculate risk
        risk_score = 0
        
        # Slope
        if slope_angle > 45: risk_score += 4
        elif slope_angle > 35: risk_score += 3
        elif slope_angle > 25: risk_score += 2
        elif slope_angle > 15: risk_score += 1
        
        # Rainfall
        if rainfall_24h > 150: risk_score += 3
        elif rainfall_24h > 100: risk_score += 2
        elif rainfall_24h > 50: risk_score += 1
        
        if rainfall_7d > 300: risk_score += 2
        elif rainfall_7d > 150: risk_score += 1
        
        # Soil moisture
        if soil_moisture > 85: risk_score += 3
        elif soil_moisture > 70: risk_score += 2
        elif soil_moisture > 55: risk_score += 1
        
        # Vegetation
        if vegetation < 20: risk_score += 2
        elif vegetation < 40: risk_score += 1
        
        # Soil type
        if soil_type >= 4: risk_score += 2
        elif soil_type == 3: risk_score += 1
        
        # Seismic
        if seismic_activity: risk_score += 2
        
        # Map to risk level
        if risk_score >= 12: risk_level = 3
        elif risk_score >= 7: risk_level = 2
        elif risk_score >= 4: risk_level = 1
        else: risk_level = 0
        
        data.append({
            'slope_angle_deg': round(slope_angle, 1),
            'rainfall_24h_mm': round(rainfall_24h, 1),
            'rainfall_7d_mm': round(rainfall_7d, 1),
            'soil_moisture_percent': round(soil_moisture, 1),
            'soil_cohesion_kpa': round(soil_cohesion, 1),
            'soil_friction_angle': round(soil_friction_angle, 1),
            'vegetation_cover_pct': round(vegetation, 1),
            'elevation_m': round(elevation, 1),
            'historical_landslides': historical_landslides,
            'soil_type': soil_type,
            'deforestation': deforestation,
            'groundwater_depth_m': round(groundwater_depth, 1),
            'seismic_activity': seismic_activity,
            'month': month,
            'risk_level': risk_level
        })
    
    return pd.DataFrame(data)


def generate_heatwave_data(n_samples=2000):
    """Generate heatwave dataset based on temperature patterns"""
    data = []
    
    for _ in range(n_samples):
        # Month (April-July are peak summer)
        month = np.random.randint(1, 13)
        is_summer = month in [4, 5, 6, 7]
        
        # Temperature
        if is_summer:
            temp = np.random.normal(38, 6)
        else:
            temp = np.random.normal(25, 8)
        
        temp = max(15, min(50, temp))  # Realistic bounds
        
        # Maximum temperature (day peak)
        temp_max = temp + np.random.uniform(2, 8)
        
        # Minimum temperature (night)
        temp_min = temp - np.random.uniform(3, 10)
        
        # Temperature trend (last 7 days)
        temp_trend = np.random.choice([-1, 0, 1], p=[0.2, 0.3, 0.5])  # -1=cooling, 1=heating
        
        # Humidity
        humidity = 100 - (temp - 15) * 1.5 + np.random.uniform(-10, 10)
        humidity = max(10, min(95, humidity))
        
        # Heat index calculation
        if temp >= 27 and humidity >= 40:
            heat_index = temp + 0.5 * (humidity / 100) * (temp - 14)
        else:
            heat_index = temp
        
        # Wind speed (affects perceived temperature)
        wind_speed = np.random.exponential(10) + np.random.uniform(5, 25)
        
        # UV index
        uv_index = max(0, min(11, (temp - 15) / 4 + np.random.uniform(-1, 2)))
        
        # Consecutive hot days
        consecutive_days = np.random.poisson(3 if is_summer else 1)
        
        # Urban heat island effect
        urban_area = np.random.choice([0, 1], p=[0.4, 0.6])
        if urban_area:
            temp += np.random.uniform(1, 4)
            heat_index += np.random.uniform(1, 3)
        
        # Soil moisture (drought indicator)
        soil_moisture = max(10, 80 - temp + np.random.uniform(-10, 10))
        
        # Cloud cover (0-100%)
        cloud_cover = np.random.uniform(0, 100)
        
        # Previous heatwave (last 30 days)
        previous_heatwave = 1 if np.random.random() < (0.4 if is_summer else 0.1) else 0
        
        # Calculate risk
        risk_score = 0
        
        # Temperature
        if temp > 45: risk_score += 4
        elif temp > 42: risk_score += 3
        elif temp > 38: risk_score += 2
        elif temp > 35: risk_score += 1
        
        # Heat index
        if heat_index > 50: risk_score += 3
        elif heat_index > 45: risk_score += 2
        elif heat_index > 40: risk_score += 1
        
        # Consecutive days
        if consecutive_days > 5: risk_score += 3
        elif consecutive_days > 3: risk_score += 2
        elif consecutive_days > 1: risk_score += 1
        
        # Humidity (high humidity makes heat worse)
        if humidity < 30 or humidity > 80: risk_score += 1
        
        # UV index
        if uv_index > 8: risk_score += 2
        elif uv_index > 6: risk_score += 1
        
        # Map to risk level
        if risk_score >= 10: risk_level = 3
        elif risk_score >= 6: risk_level = 2
        elif risk_score >= 3: risk_level = 1
        else: risk_level = 0
        
        data.append({
            'temperature_c': round(temp, 1),
            'temp_max_c': round(temp_max, 1),
            'temp_min_c': round(temp_min, 1),
            'temp_trend': temp_trend,
            'humidity_percent': round(humidity, 1),
            'heat_index': round(heat_index, 1),
            'wind_speed_kmh': round(wind_speed, 1),
            'uv_index': round(uv_index, 1),
            'consecutive_hot_days': consecutive_days,
            'urban_area': urban_area,
            'soil_moisture_percent': round(soil_moisture, 1),
            'cloud_cover_percent': round(cloud_cover, 1),
            'previous_heatwave_30d': previous_heatwave,
            'month': month,
            'risk_level': risk_level
        })
    
    return pd.DataFrame(data)


def main():
    """Generate all disaster datasets"""
    
    print("\n" + "="*70)
    print(" "*15 + "MULTI-DISASTER DATASET GENERATOR")
    print("="*70 + "\n")
    
    # Create output directory
    output_dir = "../../data/raw_multi_disaster"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate datasets
    print("Generating datasets...")
    print("-"*70)
    
    print("\n1. Flood Dataset...")
    flood_df = generate_flood_data(2000)
    flood_df.to_csv(f"{output_dir}/flood_data.csv", index=False)
    print(f"   ✓ Generated {len(flood_df)} samples")
    print(f"   ✓ Features: {len(flood_df.columns)-1}")
    print(f"   ✓ Risk distribution: {flood_df['risk_level'].value_counts().to_dict()}")
    
    print("\n2. Earthquake Dataset...")
    earthquake_df = generate_earthquake_data(2000)
    earthquake_df.to_csv(f"{output_dir}/earthquake_data.csv", index=False)
    print(f"   ✓ Generated {len(earthquake_df)} samples")
    print(f"   ✓ Features: {len(earthquake_df.columns)-1}")
    print(f"   ✓ Risk distribution: {earthquake_df['risk_level'].value_counts().to_dict()}")
    
    print("\n3. Cyclone Dataset...")
    cyclone_df = generate_cyclone_data(2000)
    cyclone_df.to_csv(f"{output_dir}/cyclone_data.csv", index=False)
    print(f"   ✓ Generated {len(cyclone_df)} samples")
    print(f"   ✓ Features: {len(cyclone_df.columns)-1}")
    print(f"   ✓ Risk distribution: {cyclone_df['risk_level'].value_counts().to_dict()}")
    
    print("\n4. Landslide Dataset...")
    landslide_df = generate_landslide_data(2000)
    landslide_df.to_csv(f"{output_dir}/landslide_data.csv", index=False)
    print(f"   ✓ Generated {len(landslide_df)} samples")
    print(f"   ✓ Features: {len(landslide_df.columns)-1}")
    print(f"   ✓ Risk distribution: {landslide_df['risk_level'].value_counts().to_dict()}")
    
    print("\n5. Heatwave Dataset...")
    heatwave_df = generate_heatwave_data(2000)
    heatwave_df.to_csv(f"{output_dir}/heatwave_data.csv", index=False)
    print(f"   ✓ Generated {len(heatwave_df)} samples")
    print(f"   ✓ Features: {len(heatwave_df.columns)-1}")
    print(f"   ✓ Risk distribution: {heatwave_df['risk_level'].value_counts().to_dict()}")
    
    print("\n" + "="*70)
    print("✅ ALL DATASETS GENERATED SUCCESSFULLY!")
    print("="*70)
    print(f"\nDatasets saved to: {output_dir}/")
    print("\nNext step: Train ML models for each disaster type")
    print("Run: python train_all_models.py")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()