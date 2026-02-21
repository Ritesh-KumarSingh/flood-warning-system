"""
Risk Scoring Module
Converts model predictions into actionable risk assessments with alerts
"""

from typing import Dict, List, Optional
from datetime import datetime
try:
    from schema import (RISK_LEVELS, RISK_THRESHOLDS, CRITICAL_THRESHOLDS,
                       get_risk_level_from_probability, get_risk_info)
except ImportError:
    from .schema import (RISK_LEVELS, RISK_THRESHOLDS, CRITICAL_THRESHOLDS,
                        get_risk_level_from_probability, get_risk_info)


class RiskScorer:
    """Converts model predictions into comprehensive risk assessments"""
    
    def __init__(self):
        self.risk_levels = RISK_LEVELS
        self.thresholds = RISK_THRESHOLDS
        self.critical_thresholds = CRITICAL_THRESHOLDS
    
    def calculate_risk_score(self, probability: float) -> int:
        """
        Convert probability to risk level (0-3)
        
        Args:
            probability: Model's prediction probability (0-1)
            
        Returns:
            Risk level: 0 (Safe), 1 (Warning), 2 (High Risk), 3 (Critical)
        """
        return get_risk_level_from_probability(probability)
    
    def generate_alert_message(self, risk_level: int, location: str = "your area",
                              features: Optional[Dict] = None) -> Dict:
        """
        Generate detailed alert message for a risk level
        
        Args:
            risk_level: Risk level (0-3)
            location: Location name
            features: Optional feature values for context
            
        Returns:
            Dictionary with alert information
        """
        risk_info = get_risk_info(risk_level)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Base alert structure
        alert = {
            'timestamp': timestamp,
            'location': location,
            'risk_level': risk_level,
            'risk_label': risk_info['label'],
            'risk_color': risk_info['color'],
            'severity': self._get_severity_text(risk_level),
            'title': self._generate_title(risk_level, location),
            'message': self._generate_message(risk_level, location),
            'description': risk_info['description'],
            'recommended_actions': self._generate_actions(risk_level),
            'emergency_contacts': self._get_emergency_contacts(risk_level),
            'additional_info': []
        }
        
        # Add feature-specific warnings if available
        if features:
            alert['additional_info'] = self._analyze_critical_features(features)
            alert['detailed_conditions'] = self._format_conditions(features)
        
        return alert
    
    def _get_severity_text(self, risk_level: int) -> str:
        """Get severity description"""
        severity_map = {
            0: "Low",
            1: "Moderate",
            2: "High",
            3: "Critical"
        }
        return severity_map.get(risk_level, "Unknown")
    
    def _generate_title(self, risk_level: int, location: str) -> str:
        """Generate alert title"""
        titles = {
            0: f"✅ All Clear in {location}",
            1: f"⚠️ Flood Watch for {location}",
            2: f"🚨 Flood Warning for {location}",
            3: f"🔴 CRITICAL FLOOD ALERT - {location.upper()}"
        }
        return titles.get(risk_level, f"Flood Alert - {location}")
    
    def _generate_message(self, risk_level: int, location: str) -> str:
        """Generate main alert message"""
        messages = {
            0: f"Weather conditions in {location} are normal. No flood risk detected at this time. Continue with regular activities.",
            
            1: f"Moderate flood risk detected in {location}. Heavy rainfall and rising water levels are being monitored. "
               f"Stay informed about weather conditions and prepare emergency supplies.",
            
            2: f"High flood risk expected in {location} within the next 24-48 hours. Significant rainfall and elevated "
               f"river levels create dangerous conditions. Prepare to evacuate if advised by authorities.",
            
            3: f"CRITICAL FLOOD DANGER in {location}! Extreme weather conditions indicate imminent flooding. "
               f"EVACUATE IMMEDIATELY to higher ground. This is a life-threatening emergency."
        }
        return messages.get(risk_level, f"Flood alert for {location}")
    
    def _generate_actions(self, risk_level: int) -> List[str]:
        """Generate list of recommended actions"""
        actions = {
            0: [
                "Continue normal activities",
                "Stay updated on weather forecasts",
                "Review your emergency plan periodically"
            ],
            
            1: [
                "Monitor weather updates closely",
                "Prepare emergency kit (water, food, medications, flashlight)",
                "Identify evacuation routes from your area",
                "Move important documents to higher floors",
                "Charge electronic devices fully",
                "Fill bathtubs and containers with clean water",
                "Stay in contact with family members"
            ],
            
            2: [
                "PREPARE TO EVACUATE - Pack essential items now",
                "Move vehicles to higher ground immediately",
                "Turn off utilities (gas, electricity) if instructed",
                "Move valuables and electronics to upper floors",
                "Secure outdoor items that could float away",
                "Stay tuned to emergency radio/TV broadcasts",
                "Do NOT attempt to walk or drive through flooded areas",
                "Keep emergency kit ready by the door",
                "Inform neighbors, especially elderly or disabled"
            ],
            
            3: [
                "🚨 EVACUATE IMMEDIATELY to designated shelter or higher ground",
                "🚨 Do NOT wait for further instructions",
                "Take ONLY essential items (ID, medications, phone)",
                "Do NOT attempt to drive through floodwater",
                "If trapped, move to highest floor or rooftop",
                "Call emergency services: 112 / 101 (India)",
                "Signal for help if stranded",
                "Do NOT return home until authorities declare it safe",
                "Avoid contact with floodwater (contamination risk)"
            ]
        }
        return actions.get(risk_level, ["Follow official emergency instructions"])
    
    def _get_emergency_contacts(self, risk_level: int) -> Dict:
        """Get relevant emergency contacts"""
        contacts = {
            'national_emergency': '112',
            'disaster_management': '1078',
            'police': '100',
            'fire': '101',
            'ambulance': '102'
        }
        
        if risk_level >= 2:
            return contacts
        elif risk_level == 1:
            return {
                'national_emergency': '112',
                'disaster_management': '1078'
            }
        else:
            return {}
    
    def _analyze_critical_features(self, features: Dict) -> List[str]:
        """Analyze features and generate specific warnings"""
        warnings = []
        
        # Rainfall analysis
        rainfall = features.get('rainfall_mm', 0)
        if rainfall > 200:
            warnings.append(f"🌧️ EXTREME rainfall detected: {rainfall:.1f} mm in last 24 hours")
        elif rainfall > 100:
            warnings.append(f"🌧️ Heavy rainfall: {rainfall:.1f} mm in last 24 hours")
        
        # River level analysis
        river_level = features.get('river_level_m', 0)
        if river_level > 11:
            warnings.append(f"🌊 DANGER LEVEL: River at {river_level:.1f} meters (critical threshold)")
        elif river_level > 8:
            warnings.append(f"🌊 WARNING: River at {river_level:.1f} meters (above normal)")
        
        # Soil moisture analysis
        soil_moisture = features.get('soil_moisture_percent', 0)
        if soil_moisture > 85:
            warnings.append(f"💧 Ground saturated: {soil_moisture:.1f}% moisture (high runoff risk)")
        
        # Distance to river
        distance = features.get('distance_to_river_km', 999)
        if distance < 1:
            warnings.append(f"⚠️ Very close to river: {distance:.2f} km (immediate flood zone)")
        
        # River level change (rapid rise)
        level_change = features.get('river_level_change', 0)
        if level_change > 2:
            warnings.append(f"📈 Rapidly rising water: +{level_change:.1f} meters in 6 hours")
        
        # Elevation (low-lying area)
        elevation = features.get('elevation_m', 999)
        if elevation < 30:
            warnings.append(f"⬇️ Low elevation: {elevation:.1f} meters (flood-prone area)")
        
        return warnings
    
    def _format_conditions(self, features: Dict) -> Dict:
        """Format current conditions in readable format"""
        return {
            'rainfall_24h': f"{features.get('rainfall_mm', 0):.1f} mm",
            'rainfall_7day_avg': f"{features.get('rainfall_7day_avg', 0):.1f} mm",
            'rainfall_intensity': f"{features.get('rainfall_intensity', 0):.1f} mm/hr",
            'river_level': f"{features.get('river_level_m', 0):.1f} meters",
            'river_trend': f"{'+' if features.get('river_level_change', 0) > 0 else ''}{features.get('river_level_change', 0):.1f} m (6h)",
            'soil_moisture': f"{features.get('soil_moisture_percent', 0):.1f}%",
            'elevation': f"{features.get('elevation_m', 0):.1f} meters",
            'distance_to_river': f"{features.get('distance_to_river_km', 0):.2f} km",
            'temperature': f"{features.get('temperature_celsius', 0):.1f}°C",
            'humidity': f"{features.get('humidity_percent', 0):.1f}%"
        }
    
    def assess_full_risk(self, prediction_result: Dict, location: str = "your area",
                        features: Optional[Dict] = None) -> Dict:
        """
        Complete risk assessment from prediction result
        
        Args:
            prediction_result: Output from model prediction
            location: Location name
            features: Input feature values
            
        Returns:
            Comprehensive risk assessment
        """
        risk_level = prediction_result['risk_level']
        probability = prediction_result['probability']
        
        # Generate alert
        alert = self.generate_alert_message(risk_level, location, features)
        
        # Add prediction details
        alert['prediction'] = {
            'probability': probability,
            'confidence': prediction_result.get('probability', 0),
            'all_probabilities': prediction_result.get('probabilities', {})
        }
        
        # Add risk scoring details
        alert['risk_score'] = {
            'numeric_level': risk_level,
            'label': prediction_result['risk_label'],
            'threshold_min': RISK_LEVELS[risk_level]['probability_range'][0],
            'threshold_max': RISK_LEVELS[risk_level]['probability_range'][1]
        }
        
        return alert


def format_alert_for_display(alert: Dict) -> str:
    """
    Format alert as human-readable text
    
    Args:
        alert: Alert dictionary
        
    Returns:
        Formatted text string
    """
    output = []
    output.append("=" * 70)
    output.append(alert['title'].center(70))
    output.append("=" * 70)
    output.append(f"\n📍 Location: {alert['location']}")
    output.append(f"🕐 Time: {alert['timestamp']}")
    output.append(f"⚠️  Severity: {alert['severity']}")
    output.append(f"\n{alert['message']}")
    
    if alert.get('additional_info'):
        output.append(f"\n🔍 CRITICAL CONDITIONS:")
        for info in alert['additional_info']:
            output.append(f"   {info}")
    
    output.append(f"\n📋 RECOMMENDED ACTIONS:")
    for idx, action in enumerate(alert['recommended_actions'], 1):
        output.append(f"   {idx}. {action}")
    
    if alert.get('emergency_contacts'):
        output.append(f"\n📞 EMERGENCY CONTACTS:")
        for service, number in alert['emergency_contacts'].items():
            output.append(f"   {service.replace('_', ' ').title()}: {number}")
    
    if alert.get('detailed_conditions'):
        output.append(f"\n🌡️  CURRENT CONDITIONS:")
        conditions = alert['detailed_conditions']
        output.append(f"   Rainfall (24h): {conditions['rainfall_24h']}")
        output.append(f"   River Level: {conditions['river_level']}")
        output.append(f"   Soil Moisture: {conditions['soil_moisture']}")
    
    output.append("\n" + "=" * 70)
    
    return "\n".join(output)


if __name__ == "__main__":
    # Example usage
    print("\n" + "="*70)
    print(" "*20 + "RISK SCORING EXAMPLES")
    print("="*70 + "\n")
    
    scorer = RiskScorer()
    
    # Example 1: Safe scenario
    print("1️⃣  Safe Scenario")
    print("-"*70)
    alert = scorer.generate_alert_message(0, "Lucknow", {
        'rainfall_mm': 15.0,
        'river_level_m': 3.5,
        'soil_moisture_percent': 45.0,
        'elevation_m': 200.0,
        'distance_to_river_km': 5.0
    })
    print(format_alert_for_display(alert))
    
    # Example 2: Critical scenario
    print("\n2️⃣  Critical Scenario")
    print("-"*70)
    alert = scorer.generate_alert_message(3, "Ayodhya", {
        'rainfall_mm': 320.0,
        'river_level_m': 12.5,
        'river_level_change': 3.5,
        'soil_moisture_percent': 92.0,
        'elevation_m': 15.0,
        'distance_to_river_km': 0.3
    })
    print(format_alert_for_display(alert))