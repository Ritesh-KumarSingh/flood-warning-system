"""
ML Schema Configuration for Flood Prediction System
This file defines the exact structure of input/output data
"""

# Feature names in order
FEATURE_NAMES = [
    'rainfall_mm',
    'rainfall_7day_avg',
    'rainfall_intensity',
    'river_level_m',
    'river_level_change',
    'soil_moisture_percent',
    'elevation_m',
    'temperature_celsius',
    'humidity_percent',
    'wind_speed_kmh',
    'distance_to_river_km',
    'month'
]

# Target variable
TARGET_NAME = 'flood_risk'

# Feature value ranges (for validation and normalization)
FEATURE_RANGES = {
    'rainfall_mm': (0, 500),
    'rainfall_7day_avg': (0, 300),
    'rainfall_intensity': (0, 50),
    'river_level_m': (0, 15),
    'river_level_change': (-2, 5),
    'soil_moisture_percent': (0, 100),
    'elevation_m': (0, 1000),
    'temperature_celsius': (-10, 45),
    'humidity_percent': (0, 100),
    'wind_speed_kmh': (0, 100),
    'distance_to_river_km': (0, 50),
    'month': (1, 12)
}

# Risk level definitions
RISK_LEVELS = {
    0: {
        'label': 'Safe',
        'color': 'green',
        'probability_range': (0.0, 0.3),
        'description': 'No flood risk detected. Weather conditions are normal.',
        'action': 'No action required. Continue normal activities.'
    },
    1: {
        'label': 'Warning',
        'color': 'yellow',
        'probability_range': (0.3, 0.6),
        'description': 'Moderate flood risk. Monitor weather updates.',
        'action': 'Prepare emergency kit. Stay informed about weather.'
    },
    2: {
        'label': 'High Risk',
        'color': 'orange',
        'probability_range': (0.6, 0.8),
        'description': 'High flood risk expected within 24-48 hours.',
        'action': 'Prepare to evacuate if advised. Move valuables to higher ground.'
    },
    3: {
        'label': 'Critical',
        'color': 'red',
        'probability_range': (0.8, 1.0),
        'description': 'CRITICAL: Immediate flood danger!',
        'action': 'EVACUATE to higher ground immediately. Follow emergency instructions.'
    }
}

# Risk threshold values
RISK_THRESHOLDS = {
    'safe': 0.3,
    'warning': 0.6,
    'high_risk': 0.8,
    'critical': 1.0
}

# Critical feature thresholds (domain knowledge)
CRITICAL_THRESHOLDS = {
    'rainfall_mm': 100,  # Heavy rainfall
    'river_level_m': 10,  # Danger level
    'soil_moisture_percent': 80,  # Saturated
    'distance_to_river_km': 1.0  # Very close to river
}

def get_risk_level_from_probability(probability: float) -> int:
    """Convert probability to risk level (0-3)"""
    if probability < RISK_THRESHOLDS['safe']:
        return 0
    elif probability < RISK_THRESHOLDS['warning']:
        return 1
    elif probability < RISK_THRESHOLDS['high_risk']:
        return 2
    else:
        return 3

def get_risk_info(risk_level: int) -> dict:
    """Get detailed information about a risk level"""
    return RISK_LEVELS.get(risk_level, RISK_LEVELS[0])

def validate_features(features: dict) -> bool:
    """Validate that all features are within expected ranges"""
    for feature, value in features.items():
        if feature in FEATURE_RANGES:
            min_val, max_val = FEATURE_RANGES[feature]
            if not (min_val <= value <= max_val):
                return False
    return True

# Example usage:
if __name__ == "__main__":
    print("Feature Schema:")
    print(f"Number of features: {len(FEATURE_NAMES)}")
    print(f"Features: {FEATURE_NAMES}")
    print(f"\nTarget: {TARGET_NAME}")
    print(f"Risk levels: {list(RISK_LEVELS.keys())}")
    
    # Test probability to risk conversion
    test_probabilities = [0.1, 0.4, 0.7, 0.95]
    print("\nProbability to Risk Level Mapping:")
    for prob in test_probabilities:
        risk = get_risk_level_from_probability(prob)
        info = get_risk_info(risk)
        print(f"Probability {prob:.2f} → Risk Level {risk} ({info['label']})")