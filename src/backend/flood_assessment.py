"""
Integrated Flood Risk Assessment Module
Combines ML prediction with risk scoring for complete assessment
"""

import sys
import os

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml'))

from predict import FloodRiskPredictor
from risk_scoring import RiskScorer, format_alert_for_display
from typing import Dict, Optional


class FloodRiskAssessor:
    """
    Complete flood risk assessment system
    Combines ML prediction with risk scoring and alert generation
    """
    
    def __init__(self, 
                 model_path='../../data/models/flood_model.pkl',
                 scaler_path='../../data/processed/scaler.pkl'):
        """
        Initialize assessor with model and scaler
        
        Args:
            model_path: Path to trained model
            scaler_path: Path to fitted scaler
        """
        print("🚀 Initializing Flood Risk Assessment System...")
        self.predictor = FloodRiskPredictor(model_path, scaler_path)
        self.scorer = RiskScorer()
        print("✅ System ready!\n")
    
    def assess_flood_risk(self, 
                         features: Dict,
                         location: str = "your area",
                         include_detailed_conditions: bool = True) -> Dict:
        """
        Complete flood risk assessment
        
        Args:
            features: Dictionary with environmental features
            location: Location name for alerts
            include_detailed_conditions: Include feature analysis
            
        Returns:
            Comprehensive risk assessment
        """
        # Step 1: Get ML prediction
        prediction = self.predictor.predict_with_explanation(features)
        
        # Step 2: Generate risk score and alert
        features_for_analysis = features if include_detailed_conditions else None
        assessment = self.scorer.assess_full_risk(
            prediction, 
            location, 
            features_for_analysis
        )
        
        # Step 3: Add input features to result
        assessment['input_features'] = features
        
        return assessment
    
    def get_formatted_alert(self, features: Dict, location: str = "your area") -> str:
        """
        Get human-readable alert text
        
        Args:
            features: Environmental features
            location: Location name
            
        Returns:
            Formatted alert string
        """
        assessment = self.assess_flood_risk(features, location)
        return format_alert_for_display(assessment)
    
    def quick_check(self, features: Dict) -> Dict:
        """
        Quick risk check - returns only essential info
        
        Args:
            features: Environmental features
            
        Returns:
            Simplified risk info
        """
        prediction = self.predictor.predict_single(features)
        
        return {
            'risk_level': prediction['risk_level'],
            'risk_label': prediction['risk_label'],
            'confidence': prediction['probability'],
            'action': prediction['recommended_action']
        }
    
    def batch_assess(self, features_list: list, locations: list = None) -> list:
        """
        Assess multiple locations at once
        
        Args:
            features_list: List of feature dictionaries
            locations: List of location names (optional)
            
        Returns:
            List of assessments
        """
        if locations is None:
            locations = [f"Location {i+1}" for i in range(len(features_list))]
        
        assessments = []
        for features, location in zip(features_list, locations):
            assessment = self.assess_flood_risk(features, location)
            assessments.append(assessment)
        
        return assessments


def run_examples():
    """Run comprehensive examples"""
    
    print("\n" + "="*70)
    print(" "*15 + "🌊 FLOOD RISK ASSESSMENT SYSTEM")
    print("="*70 + "\n")
    
    # Initialize assessor
    assessor = FloodRiskAssessor()
    
    # Example 1: Safe conditions
    print("EXAMPLE 1: Normal Weather Conditions")
    print("="*70)
    
    safe_features = {
        'rainfall_mm': 15.0,
        'rainfall_7day_avg': 20.0,
        'rainfall_intensity': 2.0,
        'river_level_m': 3.5,
        'river_level_change': 0.1,
        'soil_moisture_percent': 45.0,
        'elevation_m': 200.0,
        'temperature_celsius': 28.0,
        'humidity_percent': 65.0,
        'wind_speed_kmh': 12.0,
        'distance_to_river_km': 5.0,
        'month': 3
    }
    
    alert_text = assessor.get_formatted_alert(safe_features, "Lucknow")
    print(alert_text)
    print()
    
    # Example 2: Warning conditions
    print("\nEXAMPLE 2: Developing Flood Risk")
    print("="*70)
    
    warning_features = {
        'rainfall_mm': 95.0,
        'rainfall_7day_avg': 65.0,
        'rainfall_intensity': 10.0,
        'river_level_m': 7.2,
        'river_level_change': 0.8,
        'soil_moisture_percent': 72.0,
        'elevation_m': 85.0,
        'temperature_celsius': 26.0,
        'humidity_percent': 82.0,
        'wind_speed_kmh': 18.0,
        'distance_to_river_km': 2.3,
        'month': 7
    }
    
    alert_text = assessor.get_formatted_alert(warning_features, "Varanasi")
    print(alert_text)
    print()
    
    # Example 3: High risk
    print("\nEXAMPLE 3: High Flood Risk")
    print("="*70)
    
    high_risk_features = {
        'rainfall_mm': 165.0,
        'rainfall_7day_avg': 120.0,
        'rainfall_intensity': 18.0,
        'river_level_m': 9.8,
        'river_level_change': 2.1,
        'soil_moisture_percent': 88.0,
        'elevation_m': 42.0,
        'temperature_celsius': 24.0,
        'humidity_percent': 89.0,
        'wind_speed_kmh': 22.0,
        'distance_to_river_km': 1.1,
        'month': 8
    }
    
    alert_text = assessor.get_formatted_alert(high_risk_features, "Gorakhpur")
    print(alert_text)
    print()
    
    # Example 4: Critical emergency
    print("\nEXAMPLE 4: Critical Flood Emergency")
    print("="*70)
    
    critical_features = {
        'rainfall_mm': 340.0,
        'rainfall_7day_avg': 215.0,
        'rainfall_intensity': 32.0,
        'river_level_m': 13.2,
        'river_level_change': 4.1,
        'soil_moisture_percent': 96.0,
        'elevation_m': 18.0,
        'temperature_celsius': 23.0,
        'humidity_percent': 95.0,
        'wind_speed_kmh': 28.0,
        'distance_to_river_km': 0.4,
        'month': 8
    }
    
    alert_text = assessor.get_formatted_alert(critical_features, "Ayodhya")
    print(alert_text)
    print()
    
    # Example 5: Quick check demo
    print("\nEXAMPLE 5: Quick Risk Check (Simplified Output)")
    print("="*70)
    
    quick_result = assessor.quick_check(warning_features)
    print(f"Risk Level: {quick_result['risk_label']}")
    print(f"Confidence: {quick_result['confidence']*100:.1f}%")
    print(f"Action: {quick_result['action']}")
    print()
    
    print("="*70)
    print("✅ All examples complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    run_examples()