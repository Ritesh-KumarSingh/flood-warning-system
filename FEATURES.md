# Flood Prediction - Feature Definitions

## Input Features (12 features total)

### 1. Rainfall Data (3 features)
- **rainfall_mm**: Rainfall in last 24 hours (mm)
  - Range: 0-500 mm
  - Critical threshold: >100 mm = high risk
  
- **rainfall_7day_avg**: Average rainfall over past 7 days (mm)
  - Range: 0-300 mm
  - Captures sustained wet periods
  
- **rainfall_intensity**: Current rainfall rate (mm/hour)
  - Range: 0-50 mm/hour
  - >10 mm/hour = heavy rain

### 2. River/Water Level (2 features)
- **river_level_m**: Current river water level (meters)
  - Range: 0-15 meters
  - >10m = danger level (location-dependent)
  
- **river_level_change**: Change in level over last 6 hours (meters)
  - Range: -2 to +5 meters
  - Rapid rise = high risk

### 3. Soil & Terrain (2 features)
- **soil_moisture_percent**: Soil saturation level (%)
  - Range: 0-100%
  - >80% = saturated, high runoff risk
  
- **elevation_m**: Location elevation above sea level (meters)
  - Range: 0-1000+ meters
  - Low elevation = higher flood risk

### 4. Weather Conditions (3 features)
- **temperature_celsius**: Current temperature (°C)
  - Range: -10 to 45°C
  - Affects evaporation rate
  
- **humidity_percent**: Relative humidity (%)
  - Range: 0-100%
  - High humidity = less evaporation
  
- **wind_speed_kmh**: Wind speed (km/h)
  - Range: 0-100 km/h
  - Affects evaporation and storm intensity

### 5. Geographic/Seasonal (2 features)
- **distance_to_river_km**: Distance from major water body (km)
  - Range: 0-50 km
  - <1 km = very high risk
  
- **month**: Month of year (1-12)
  - Captures monsoon/seasonal patterns
  - June-September = monsoon in India

## Output (Target Variable)

**flood_risk** - Categorical variable with 4 levels:
- 0 = Safe (probability < 0.3)
- 1 = Warning (probability 0.3-0.6)
- 2 = High Risk (probability 0.6-0.8)
- 3 = Critical (probability > 0.8)

## Why These Features?

1. **Rainfall**: Primary cause of floods
2. **River level**: Direct indicator of flood danger
3. **Soil moisture**: Determines absorption vs runoff
4. **Elevation**: Low areas flood first
5. **Weather**: Affects water accumulation/evaporation
6. **Geography**: Distance to water body matters
7. **Season**: Monsoons have higher risk

## Data Collection Sources

- **Rainfall**: Weather APIs (OpenWeatherMap), Rain gauges
- **River level**: Hydrological sensors, Government databases
- **Soil moisture**: IoT sensors, Satellite data
- **Weather**: Weather APIs
- **Geographic**: OpenStreetMap, Google Maps API
- **Historical**: Government disaster databases, Kaggle datasets