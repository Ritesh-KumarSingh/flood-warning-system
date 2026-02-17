"""
Multi-Disaster Prediction System
Supports: Floods, Earthquakes, Cyclones, Landslides, Heatwaves
"""

import sys
import os

# ── deployment-safe path bootstrap ──────────────────────────────────────────
_BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
_SRC_DIR     = os.path.dirname(_BACKEND_DIR)
_ML_DIR      = os.path.join(_SRC_DIR, "ml")
_UTILS_DIR   = os.path.join(_SRC_DIR, "utils")
for _p in (_BACKEND_DIR, _ML_DIR, _UTILS_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from flood_assessment import FloodRiskAssessor
from datetime import datetime

class MultiDisasterPredictor:
    """Unified predictor for multiple disaster types"""
    
    def __init__(self):
        # Load flood model (already trained)
        self.flood_assessor = FloodRiskAssessor()
        
    def predict_disaster(self, disaster_type, weather_data, location):
        """
        Predict risk for any disaster type
        
        Args:
            disaster_type: 'flood', 'earthquake', 'cyclone', 'landslide', 'heatwave'
            weather_data: Current weather conditions
            location: Location name
            
        Returns:
            Risk assessment with alerts
        """
        if disaster_type == 'flood':
            return self._predict_flood(weather_data, location)
        elif disaster_type == 'earthquake':
            return self._predict_earthquake(weather_data, location)
        elif disaster_type == 'cyclone':
            return self._predict_cyclone(weather_data, location)
        elif disaster_type == 'landslide':
            return self._predict_landslide(weather_data, location)
        elif disaster_type == 'heatwave':
            return self._predict_heatwave(weather_data, location)
        else:
            raise ValueError(f"Unknown disaster type: {disaster_type}")
    
    def _predict_flood(self, weather_data, location):
        """Use trained ML model for floods"""
        return self.flood_assessor.assess_flood_risk(weather_data, location)
    
    def _predict_earthquake(self, weather_data, location):
        """Rule-based earthquake risk assessment"""
        # Note: Earthquakes aren't weather-dependent, but we can assess general risk
        # In production, integrate with seismic monitoring APIs
        
        # High-risk earthquake zones in India
        high_risk_zones = ['delhi', 'uttarakhand', 'himachal', 'kashmir', 'assam', 
                          'sikkim', 'gujarat', 'maharashtra']
        medium_risk_zones = ['kerala', 'karnataka', 'rajasthan', 'bihar']
        
        location_lower = location.lower()
        
        # Determine base risk
        if any(zone in location_lower for zone in high_risk_zones):
            base_risk = 2  # High risk
            probability = 0.65
        elif any(zone in location_lower for zone in medium_risk_zones):
            base_risk = 1  # Medium risk
            probability = 0.45
        else:
            base_risk = 0  # Low risk
            probability = 0.15
        
        # Create assessment
        risk_levels = ['Safe', 'Warning', 'High Risk', 'Critical']
        
        return {
            'timestamp': datetime.now().isoformat(),
            'location': location,
            'disaster_type': 'Earthquake',
            'risk_level': base_risk,
            'risk_label': risk_levels[base_risk],
            'risk_color': ['green', 'yellow', 'orange', 'red'][base_risk],
            'severity': ['Low', 'Moderate', 'High', 'Critical'][base_risk],
            'title': f"{'⚠️' if base_risk >= 1 else '✅'} Earthquake Risk: {risk_levels[base_risk]} - {location}",
            'message': self._get_earthquake_message(base_risk, location),
            'recommended_actions': self._get_earthquake_actions(base_risk),
            'emergency_contacts': self._get_emergency_contacts(base_risk),
            'prediction': {
                'probability': probability,
                'confidence': 0.7,
                'all_probabilities': {
                    'safe': 1 - probability if base_risk == 0 else 0.2,
                    'warning': probability if base_risk == 1 else 0.3,
                    'high_risk': probability if base_risk == 2 else 0.4,
                    'critical': 0.1
                }
            },
            'risk_score': {
                'numeric_level': base_risk,
                'label': risk_levels[base_risk],
                'threshold_min': 0.3 * base_risk,
                'threshold_max': 0.3 * (base_risk + 1)
            },
            'additional_info': self._get_earthquake_warnings(base_risk, location)
        }
    
    def _predict_cyclone(self, weather_data, location):
        """Rule-based cyclone risk assessment"""
        wind_speed = weather_data.get('wind_speed_kmh', 0)
        pressure = weather_data.get('pressure', 1013)
        humidity = weather_data.get('humidity_percent', 70)
        temperature = weather_data.get('temperature_celsius', 25)
        month = weather_data.get('month', 1)
        
        # Coastal areas
        coastal_cities = ['mumbai', 'chennai', 'kolkata', 'visakhapatnam', 
                         'bhubaneswar', 'goa', 'thiruvananthapuram']
        is_coastal = any(city in location.lower() for city in coastal_cities)
        
        # Cyclone season (May-June, October-November)
        cyclone_season = month in [5, 6, 10, 11]
        
        # Risk calculation
        risk_score = 0
        
        if is_coastal:
            risk_score += 2
        if cyclone_season:
            risk_score += 2
        if wind_speed > 60:
            risk_score += 3
        if pressure < 990:
            risk_score += 3
        if humidity > 85:
            risk_score += 1
        
        # Determine risk level
        if risk_score >= 8:
            risk_level = 3  # Critical
            probability = 0.85
        elif risk_score >= 5:
            risk_level = 2  # High
            probability = 0.65
        elif risk_score >= 3:
            risk_level = 1  # Warning
            probability = 0.40
        else:
            risk_level = 0  # Safe
            probability = 0.15
        
        risk_levels = ['Safe', 'Warning', 'High Risk', 'Critical']
        
        return {
            'timestamp': datetime.now().isoformat(),
            'location': location,
            'disaster_type': 'Cyclone',
            'risk_level': risk_level,
            'risk_label': risk_levels[risk_level],
            'risk_color': ['green', 'yellow', 'orange', 'red'][risk_level],
            'severity': ['Low', 'Moderate', 'High', 'Critical'][risk_level],
            'title': f"{'🌪️' if risk_level >= 2 else '✅'} Cyclone Risk: {risk_levels[risk_level]} - {location}",
            'message': self._get_cyclone_message(risk_level, location, wind_speed),
            'recommended_actions': self._get_cyclone_actions(risk_level),
            'emergency_contacts': self._get_emergency_contacts(risk_level),
            'prediction': {
                'probability': probability,
                'confidence': 0.75,
                'all_probabilities': {
                    'safe': 1 - probability if risk_level == 0 else 0.1,
                    'warning': probability if risk_level == 1 else 0.2,
                    'high_risk': probability if risk_level == 2 else 0.4,
                    'critical': probability if risk_level == 3 else 0.3
                }
            },
            'risk_score': {
                'numeric_level': risk_level,
                'label': risk_levels[risk_level],
                'threshold_min': 0.3 * risk_level,
                'threshold_max': 0.3 * (risk_level + 1)
            },
            'additional_info': self._get_cyclone_warnings(risk_level, wind_speed, pressure)
        }
    
    def _predict_landslide(self, weather_data, location):
        """Rule-based landslide risk assessment"""
        rainfall = weather_data.get('rainfall_mm', 0)
        rainfall_7day = weather_data.get('rainfall_7day_avg', 0)
        soil_moisture = weather_data.get('soil_moisture_percent', 50)
        elevation = weather_data.get('elevation_m', 100)
        
        # Hilly/mountainous regions
        hilly_regions = ['uttarakhand', 'himachal', 'kashmir', 'sikkim', 
                        'darjeeling', 'ooty', 'munnar', 'shimla', 'manali']
        is_hilly = any(region in location.lower() for region in hilly_regions)
        
        # Risk calculation
        risk_score = 0
        
        if is_hilly or elevation > 500:
            risk_score += 3
        if rainfall > 100:
            risk_score += 2
        if rainfall_7day > 200:
            risk_score += 3
        if soil_moisture > 80:
            risk_score += 2
        
        # Determine risk level
        if risk_score >= 8:
            risk_level = 3
            probability = 0.80
        elif risk_score >= 5:
            risk_level = 2
            probability = 0.60
        elif risk_score >= 3:
            risk_level = 1
            probability = 0.35
        else:
            risk_level = 0
            probability = 0.10
        
        risk_levels = ['Safe', 'Warning', 'High Risk', 'Critical']
        
        return {
            'timestamp': datetime.now().isoformat(),
            'location': location,
            'disaster_type': 'Landslide',
            'risk_level': risk_level,
            'risk_label': risk_levels[risk_level],
            'risk_color': ['green', 'yellow', 'orange', 'red'][risk_level],
            'severity': ['Low', 'Moderate', 'High', 'Critical'][risk_level],
            'title': f"{'⛰️' if risk_level >= 2 else '✅'} Landslide Risk: {risk_levels[risk_level]} - {location}",
            'message': self._get_landslide_message(risk_level, location),
            'recommended_actions': self._get_landslide_actions(risk_level),
            'emergency_contacts': self._get_emergency_contacts(risk_level),
            'prediction': {
                'probability': probability,
                'confidence': 0.70,
                'all_probabilities': {
                    'safe': 1 - probability if risk_level == 0 else 0.15,
                    'warning': probability if risk_level == 1 else 0.25,
                    'high_risk': probability if risk_level == 2 else 0.35,
                    'critical': probability if risk_level == 3 else 0.25
                }
            },
            'risk_score': {
                'numeric_level': risk_level,
                'label': risk_levels[risk_level],
                'threshold_min': 0.3 * risk_level,
                'threshold_max': 0.3 * (risk_level + 1)
            },
            'additional_info': self._get_landslide_warnings(risk_level, rainfall, soil_moisture)
        }
    
    def _predict_heatwave(self, weather_data, location):
        """Rule-based heatwave risk assessment"""
        temperature = weather_data.get('temperature_celsius', 25)
        humidity = weather_data.get('humidity_percent', 70)
        month = weather_data.get('month', 1)
        
        # Calculate heat index (feels like temperature)
        heat_index = temperature + (0.5 * humidity / 100 * (temperature - 14))
        
        # Summer months
        is_summer = month in [4, 5, 6, 7]
        
        # Risk calculation
        if heat_index >= 45:
            risk_level = 3  # Critical
            probability = 0.90
        elif heat_index >= 40:
            risk_level = 2  # High
            probability = 0.70
        elif heat_index >= 35:
            risk_level = 1  # Warning
            probability = 0.45
        else:
            risk_level = 0  # Safe
            probability = 0.15
        
        # Summer bonus
        if is_summer and risk_level < 3:
            if heat_index >= 38:
                risk_level += 1
                probability += 0.15
        
        risk_levels = ['Safe', 'Warning', 'High Risk', 'Critical']
        
        return {
            'timestamp': datetime.now().isoformat(),
            'location': location,
            'disaster_type': 'Heatwave',
            'risk_level': min(risk_level, 3),
            'risk_label': risk_levels[min(risk_level, 3)],
            'risk_color': ['green', 'yellow', 'orange', 'red'][min(risk_level, 3)],
            'severity': ['Low', 'Moderate', 'High', 'Critical'][min(risk_level, 3)],
            'title': f"{'🌡️' if risk_level >= 2 else '✅'} Heatwave Risk: {risk_levels[min(risk_level, 3)]} - {location}",
            'message': self._get_heatwave_message(min(risk_level, 3), temperature, heat_index),
            'recommended_actions': self._get_heatwave_actions(min(risk_level, 3)),
            'emergency_contacts': self._get_emergency_contacts(min(risk_level, 3)) if risk_level >= 2 else {},
            'prediction': {
                'probability': min(probability, 0.95),
                'confidence': 0.85,
                'all_probabilities': {
                    'safe': 1 - probability if risk_level == 0 else 0.05,
                    'warning': probability if risk_level == 1 else 0.20,
                    'high_risk': probability if risk_level == 2 else 0.40,
                    'critical': probability if risk_level >= 3 else 0.35
                }
            },
            'risk_score': {
                'numeric_level': min(risk_level, 3),
                'label': risk_levels[min(risk_level, 3)],
                'threshold_min': 0.3 * min(risk_level, 3),
                'threshold_max': 0.3 * (min(risk_level, 3) + 1)
            },
            'additional_info': self._get_heatwave_warnings(min(risk_level, 3), temperature, heat_index)
        }
    
    # Helper methods for messages and actions
    
    def _get_earthquake_message(self, risk_level, location):
        messages = [
            f"No immediate earthquake threat in {location}. Continue normal activities.",
            f"Moderate seismic activity possible in {location}. Stay prepared.",
            f"High earthquake risk zone. Be prepared for potential seismic activity.",
            f"CRITICAL: Very high earthquake risk. Ensure emergency preparedness!"
        ]
        return messages[risk_level]
    
    def _get_earthquake_actions(self, risk_level):
        actions = {
            0: ["Stay informed about seismic activity", "Review earthquake safety plan"],
            1: ["Secure heavy furniture", "Identify safe spots (doorways, tables)", "Prepare emergency kit"],
            2: ["DROP, COVER, HOLD ON practice", "Secure water heaters and appliances", 
                "Identify evacuation routes", "Stock emergency supplies"],
            3: ["Ensure emergency kit is ready", "Identify safe zones in each room",
                "Plan family meeting points", "Stay away from buildings if outdoors"]
        }
        return actions[risk_level]
    
    def _get_earthquake_warnings(self, risk_level, location):
        if risk_level >= 2:
            return [
                f"⚠️ {location} is in a seismically active zone",
                "🏢 Secure tall furniture and heavy objects",
                "📱 Keep emergency contacts handy"
            ]
        return []
    
    def _get_cyclone_message(self, risk_level, location, wind_speed):
        messages = [
            f"No cyclone threat in {location}. Weather conditions normal.",
            f"Cyclone watch for {location}. Wind speed: {wind_speed:.1f} km/h. Monitor updates.",
            f"Cyclone warning! High winds expected in {location}. Prepare to evacuate.",
            f"CRITICAL CYCLONE ALERT! Severe storm conditions in {location}. Evacuate NOW!"
        ]
        return messages[risk_level]
    
    def _get_cyclone_actions(self, risk_level):
        actions = {
            0: ["Monitor weather updates", "Review cyclone safety plan"],
            1: ["Secure outdoor items", "Stock emergency supplies", "Charge devices",
                "Fill water containers"],
            2: ["Board up windows", "Move to sturdy shelter", "Stay indoors",
                "Avoid coastal areas", "Prepare for power outage"],
            3: ["EVACUATE to designated shelter", "Stay away from windows",
                "Do NOT go outside", "Listen to emergency broadcasts"]
        }
        return actions[risk_level]
    
    def _get_cyclone_warnings(self, risk_level, wind_speed, pressure):
        warnings = []
        if wind_speed > 60:
            warnings.append(f"💨 High winds: {wind_speed:.1f} km/h")
        if pressure < 990:
            warnings.append(f"🌀 Low pressure system: {pressure} hPa")
        if risk_level >= 2:
            warnings.append("⚠️ Storm surge possible in coastal areas")
        return warnings
    
    def _get_landslide_message(self, risk_level, location):
        messages = [
            f"No landslide risk in {location}. Conditions stable.",
            f"Landslide watch for {location}. Heavy rain may destabilize slopes.",
            f"HIGH landslide risk in {location}! Avoid hilly areas.",
            f"CRITICAL: Imminent landslide danger in {location}! Evacuate slopes immediately!"
        ]
        return messages[risk_level]
    
    def _get_landslide_actions(self, risk_level):
        actions = {
            0: ["Stay informed about weather", "Avoid steep slopes during heavy rain"],
            1: ["Monitor slope stability", "Avoid hillside driving", "Prepare evacuation route"],
            2: ["EVACUATE from slope areas", "Stay away from valleys", 
                "Watch for debris flows", "Listen for unusual sounds"],
            3: ["EVACUATE IMMEDIATELY from hilly areas", "Move to high, stable ground",
                "Do NOT attempt to cross slopes", "Call emergency services"]
        }
        return actions[risk_level]
    
    def _get_landslide_warnings(self, risk_level, rainfall, soil_moisture):
        warnings = []
        if rainfall > 100:
            warnings.append(f"🌧️ Heavy rainfall: {rainfall:.1f} mm")
        if soil_moisture > 80:
            warnings.append(f"💧 Saturated soil: {soil_moisture:.1f}%")
        if risk_level >= 2:
            warnings.append("⛰️ Unstable slopes detected")
        return warnings
    
    def _get_heatwave_message(self, risk_level, temp, heat_index):
        messages = [
            f"Pleasant weather. Temperature: {temp:.1f}°C. No heat risk.",
            f"Hot weather alert! Temperature: {temp:.1f}°C, Feels like: {heat_index:.1f}°C. Stay hydrated.",
            f"HEATWAVE WARNING! Extreme heat: {temp:.1f}°C, Feels like: {heat_index:.1f}°C. Avoid outdoor activities.",
            f"CRITICAL HEATWAVE! Dangerous heat: {temp:.1f}°C, Feels like: {heat_index:.1f}°C. Stay indoors!"
        ]
        return messages[risk_level]
    
    def _get_heatwave_actions(self, risk_level):
        actions = {
            0: ["Enjoy the weather safely", "Stay hydrated"],
            1: ["Drink plenty of water", "Avoid peak sun hours (11AM-3PM)", 
                "Wear light clothing", "Use sunscreen"],
            2: ["Stay indoors during peak heat", "Use AC or fans", 
                "Check on elderly/vulnerable", "Avoid strenuous activities",
                "Drink water every 15-20 minutes"],
            3: ["STAY INDOORS with AC", "Close curtains/blinds",
                "Do NOT go outside unless absolutely necessary",
                "Seek cooling centers if no AC", "Call for medical help if dizzy/nauseous"]
        }
        return actions[risk_level]
    
    def _get_heatwave_warnings(self, risk_level, temp, heat_index):
        warnings = []
        if temp >= 40:
            warnings.append(f"🌡️ Extreme temperature: {temp:.1f}°C")
        if heat_index >= 45:
            warnings.append(f"🔥 Dangerous heat index: {heat_index:.1f}°C")
        if risk_level >= 2:
            warnings.append("⚠️ Heat stroke risk - stay hydrated!")
        return warnings
    
    def _get_emergency_contacts(self, risk_level):
        if risk_level >= 1:
            return {
                'national_emergency': '112',
                'disaster_management': '1078',
                'police': '100',
                'fire': '101',
                'ambulance': '102'
            }
        return {}