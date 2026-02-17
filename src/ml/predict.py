"""
Prediction Module
Helper functions for making predictions with trained model
"""

import pandas as pd
import numpy as np
import joblib
import os
from schema import FEATURE_NAMES, get_risk_info, get_risk_level_from_probability

class FloodRiskPredictor:
    """Helper class for making flood predictions"""
    
    def __init__(self, model_path='../../data/models/flood_model.pkl',
                 scaler_path='../../data/processed/scaler.pkl'):
        """
        Initialize predictor with trained model and scaler
        
        Args:
            model_path: Path to trained model
            scaler_path: Path to fitted scaler
        """
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        print(f"✅ Model loaded from {model_path}")
        print(f"✅ Scaler loaded from {scaler_path}")
    
    def predict_single(self, features_dict):
        """
        Make prediction for a single data point
        
        Args:
            features_dict: Dictionary with feature values
            
        Returns:
            Dictionary with prediction results
        """
        # Convert dict to DataFrame
        features_df = pd.DataFrame([features_dict])
        
        # Ensure correct column order
        features_df = features_df[FEATURE_NAMES]
        
        # Scale features - keep as DataFrame to preserve feature names
        features_scaled = self.scaler.transform(features_df)
        features_scaled_df = pd.DataFrame(features_scaled, columns=FEATURE_NAMES)
        
        # Make prediction with DataFrame (avoids feature name warning)
        risk_level = self.model.predict(features_scaled_df)[0]
        probabilities = self.model.predict_proba(features_scaled_df)[0]
        
        # Get risk info
        risk_info = get_risk_info(risk_level)
        max_probability = probabilities[risk_level]
        
        result = {
            'risk_level': int(risk_level),
            'risk_label': risk_info['label'],
            'risk_color': risk_info['color'],
            'probability': float(max_probability),
            'probabilities': {
                'safe': float(probabilities[0]),
                'warning': float(probabilities[1]),
                'high_risk': float(probabilities[2]),
                'critical': float(probabilities[3])
            },
            'description': risk_info['description'],
            'recommended_action': risk_info['action']
        }
        
        return result
    
    def predict_batch(self, features_df):
        """
        Make predictions for multiple data points
        
        Args:
            features_df: DataFrame with features
            
        Returns:
            DataFrame with predictions
        """
        # Ensure correct column order
        features_df = features_df[FEATURE_NAMES]
        
        # Scale features - keep as DataFrame to preserve feature names
        features_scaled = self.scaler.transform(features_df)
        features_scaled_df = pd.DataFrame(features_scaled, columns=FEATURE_NAMES, index=features_df.index)
        
        # Make predictions with DataFrame (avoids feature name warning)
        risk_levels = self.model.predict(features_scaled_df)
        probabilities = self.model.predict_proba(features_scaled_df)
        
        # Create results DataFrame
        results = features_df.copy()
        results['predicted_risk_level'] = risk_levels
        results['prediction_probability'] = [prob[level] for prob, level in zip(probabilities, risk_levels)]
        
        # Add risk labels
        results['risk_label'] = results['predicted_risk_level'].map({
            0: 'Safe', 1: 'Warning', 2: 'High Risk', 3: 'Critical'
        })
        
        return results
    
    def predict_with_explanation(self, features_dict):
        """
        Make prediction with detailed explanation
        
        Args:
            features_dict: Dictionary with feature values
            
        Returns:
            Dictionary with prediction and explanation
        """
        result = self.predict_single(features_dict)
        
        # Add feature analysis
        critical_features = []
        
        # Check critical thresholds
        if features_dict['rainfall_mm'] > 200:
            critical_features.append(f"⚠️  Very heavy rainfall: {features_dict['rainfall_mm']:.1f} mm")
        
        if features_dict['river_level_m'] > 10:
            critical_features.append(f"⚠️  River at danger level: {features_dict['river_level_m']:.1f} m")
        
        if features_dict['soil_moisture_percent'] > 85:
            critical_features.append(f"⚠️  Soil saturated: {features_dict['soil_moisture_percent']:.1f}%")
        
        if features_dict['distance_to_river_km'] < 1:
            critical_features.append(f"⚠️  Very close to river: {features_dict['distance_to_river_km']:.2f} km")
        
        result['critical_features'] = critical_features
        result['input_features'] = features_dict
        
        return result


def example_predictions():
    """Run example predictions"""
    
    print("\n" + "="*70)
    print(" "*15 + "🔮 FLOOD PREDICTION EXAMPLES")
    print("="*70 + "\n")
    
    # Initialize predictor
    predictor = FloodRiskPredictor()
    
    # Example 1: Safe conditions
    print("1️⃣  Example: Safe Conditions")
    print("-"*70)
    
    safe_scenario = {
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
    
    result = predictor.predict_with_explanation(safe_scenario)
    print_prediction_result(result)
    
    # Example 2: Warning conditions
    print("\n2️⃣  Example: Warning Conditions")
    print("-"*70)
    
    warning_scenario = {
        'rainfall_mm': 85.0,
        'rainfall_7day_avg': 60.0,
        'rainfall_intensity': 9.0,
        'river_level_m': 6.5,
        'river_level_change': 0.7,
        'soil_moisture_percent': 70.0,
        'elevation_m': 100.0,
        'temperature_celsius': 26.0,
        'humidity_percent': 80.0,
        'wind_speed_kmh': 15.0,
        'distance_to_river_km': 2.5,
        'month': 7
    }
    
    result = predictor.predict_with_explanation(warning_scenario)
    print_prediction_result(result)
    
    # Example 3: Critical conditions
    print("\n3️⃣  Example: Critical Conditions")
    print("-"*70)
    
    critical_scenario = {
        'rainfall_mm': 320.0,
        'rainfall_7day_avg': 200.0,
        'rainfall_intensity': 28.0,
        'river_level_m': 12.5,
        'river_level_change': 3.5,
        'soil_moisture_percent': 92.0,
        'elevation_m': 15.0,
        'temperature_celsius': 24.0,
        'humidity_percent': 95.0,
        'wind_speed_kmh': 8.0,
        'distance_to_river_km': 0.3,
        'month': 8
    }
    
    result = predictor.predict_with_explanation(critical_scenario)
    print_prediction_result(result)
    
    print("\n" + "="*70)
    print("✅ Example predictions complete!")
    print("="*70 + "\n")


def print_prediction_result(result):
    """Pretty print prediction result"""
    
    # Color coding
    color_emoji = {
        'green': '🟢',
        'yellow': '🟡',
        'orange': '🟠',
        'red': '🔴'
    }
    
    emoji = color_emoji.get(result['risk_color'], '⚪')
    
    print(f"\n{emoji} PREDICTION: {result['risk_label']} (Level {result['risk_level']})")
    print(f"   Confidence: {result['probability']*100:.1f}%")
    print()
    print(f"📊 Probability Distribution:")
    print(f"   Safe:      {result['probabilities']['safe']*100:5.1f}%")
    print(f"   Warning:   {result['probabilities']['warning']*100:5.1f}%")
    print(f"   High Risk: {result['probabilities']['high_risk']*100:5.1f}%")
    print(f"   Critical:  {result['probabilities']['critical']*100:5.1f}%")
    print()
    print(f"📝 Description:")
    print(f"   {result['description']}")
    print()
    print(f"🎯 Recommended Action:")
    print(f"   {result['recommended_action']}")
    
    if result.get('critical_features'):
        print()
        print(f"⚠️  Critical Factors:")
        for feature in result['critical_features']:
            print(f"   {feature}")


if __name__ == "__main__":
    example_predictions()