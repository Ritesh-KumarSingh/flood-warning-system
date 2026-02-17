# Data Schema for Flood Prediction Dataset

## CSV Column Structure

| Column Name             | Data Type | Range/Values      | Description                           |
|------------------------|-----------|-------------------|---------------------------------------|
| rainfall_mm            | float     | 0-500             | Rainfall in last 24h (mm)            |
| rainfall_7day_avg      | float     | 0-300             | 7-day average rainfall (mm)          |
| rainfall_intensity     | float     | 0-50              | Current rainfall rate (mm/h)         |
| river_level_m          | float     | 0-15              | Current river level (meters)         |
| river_level_change     | float     | -2 to +5          | Level change in 6h (meters)          |
| soil_moisture_percent  | float     | 0-100             | Soil saturation (%)                  |
| elevation_m            | float     | 0-1000            | Elevation above sea level (m)        |
| temperature_celsius    | float     | -10 to 45         | Current temperature (°C)             |
| humidity_percent       | float     | 0-100             | Relative humidity (%)                |
| wind_speed_kmh         | float     | 0-100             | Wind speed (km/h)                    |
| distance_to_river_km   | float     | 0-50              | Distance to river (km)               |
| month                  | int       | 1-12              | Month of year                        |
| flood_risk             | int       | 0, 1, 2, 3        | TARGET: Risk level                   |

## Target Variable Mapping

```python
RISK_LEVELS = {
    0: "Safe",
    1: "Warning", 
    2: "High Risk",
    3: "Critical"
}
```

## Sample Data Rows

### Example 1: Safe Condition
```
rainfall_mm,rainfall_7day_avg,rainfall_intensity,river_level_m,river_level_change,soil_moisture_percent,elevation_m,temperature_celsius,humidity_percent,wind_speed_kmh,distance_to_river_km,month,flood_risk
10.5,15.2,2.0,3.5,0.1,45.0,150.0,28.0,65.0,12.0,5.0,3,0
```

### Example 2: Warning Condition
```
65.0,45.0,8.0,6.5,0.8,68.0,80.0,26.0,78.0,15.0,2.0,7,1
```

### Example 3: High Risk Condition
```
145.0,95.0,15.0,9.2,1.5,85.0,50.0,25.0,88.0,8.0,1.0,8,2
```

### Example 4: Critical Condition
```
280.0,180.0,25.0,11.5,3.2,95.0,20.0,24.0,92.0,5.0,0.5,7,3
```

## Data Quality Requirements

1. **No missing values** in critical columns (rainfall, river_level, flood_risk)
2. **Range validation**: All values within specified ranges
3. **Temporal consistency**: month should reflect when data was collected
4. **Logical consistency**: High soil moisture should correlate with recent rainfall
5. **Minimum dataset size**: 1000+ rows for reliable training

## File Naming Convention

- Raw data: `data/raw/flood_data_raw.csv`
- Cleaned data: `data/processed/flood_data_clean.csv`
- Train set: `data/processed/train.csv`
- Test set: `data/processed/test.csv`