"""
Unit Tests for ML Components
Tests model, preprocessing, and prediction functions
"""

import unittest
import sys
import os
import numpy as np
import pandas as pd

# Add paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
ml_path = os.path.join(project_root, 'src', 'ml')
backend_path = os.path.join(project_root, 'src', 'backend')

sys.path.insert(0, ml_path)
sys.path.insert(0, backend_path)

try:
    from schema import FEATURE_NAMES, RISK_LEVELS, validate_features
    from data_preprocessing import FloodDataPreprocessor
    from train_model import FloodPredictor
    from predict import FloodRiskPredictor
    IMPORTS_OK = True
except ImportError as e:
    print(f"⚠️  Import Error: {e}")
    print(f"   ML Path: {ml_path}")
    print(f"   Backend Path: {backend_path}")
    IMPORTS_OK = False


class TestSchema(unittest.TestCase):
    """Test schema definitions and validation"""
    
    def setUp(self):
        """Check if imports are available"""
        if not IMPORTS_OK:
            self.skipTest("Required modules not imported")
    
    def test_feature_count(self):
        """Test correct number of features"""
        self.assertEqual(len(FEATURE_NAMES), 12, "Should have exactly 12 features")
    
    def test_risk_levels(self):
        """Test risk level definitions"""
        self.assertEqual(len(RISK_LEVELS), 4, "Should have 4 risk levels")
        self.assertIn(0, RISK_LEVELS, "Should have level 0 (Safe)")
        self.assertIn(3, RISK_LEVELS, "Should have level 3 (Critical)")
    
    def test_feature_validation(self):
        """Test feature validation function"""
        # Valid features
        valid_features = {
            'rainfall_mm': 100.0,
            'rainfall_7day_avg': 80.0,
            'rainfall_intensity': 10.0,
            'river_level_m': 5.0,
            'river_level_change': 0.5,
            'soil_moisture_percent': 60.0,
            'elevation_m': 100.0,
            'temperature_celsius': 25.0,
            'humidity_percent': 70.0,
            'wind_speed_kmh': 15.0,
            'distance_to_river_km': 3.0,
            'month': 7
        }
        self.assertTrue(validate_features(valid_features))
        
        # Invalid features (out of range)
        invalid_features = valid_features.copy()
        invalid_features['rainfall_mm'] = -10.0  # Negative rainfall
        self.assertFalse(validate_features(invalid_features))


class TestPreprocessing(unittest.TestCase):
    """Test data preprocessing functions"""
    
    def setUp(self):
        """Set up test data"""
        self.test_data = pd.DataFrame({
            'rainfall_mm': [50.0, 100.0, 200.0],
            'rainfall_7day_avg': [40.0, 80.0, 150.0],
            'rainfall_intensity': [5.0, 10.0, 20.0],
            'river_level_m': [3.0, 6.0, 11.0],
            'river_level_change': [0.1, 0.5, 2.0],
            'soil_moisture_percent': [50.0, 70.0, 90.0],
            'elevation_m': [100.0, 80.0, 30.0],
            'temperature_celsius': [28.0, 26.0, 24.0],
            'humidity_percent': [65.0, 80.0, 95.0],
            'wind_speed_kmh': [12.0, 18.0, 25.0],
            'distance_to_river_km': [5.0, 2.0, 0.5],
            'month': [3, 7, 8],
            'flood_risk': [0, 1, 3]
        })
    
    def test_preprocessor_initialization(self):
        """Test preprocessor can be initialized"""
        preprocessor = FloodDataPreprocessor()
        self.assertIsNotNone(preprocessor)
    
    def test_normalization(self):
        """Test that normalization produces valid output"""
        preprocessor = FloodDataPreprocessor()
        X = self.test_data[FEATURE_NAMES]
        y = self.test_data['flood_risk']
        
        X_normalized = preprocessor.scaler.fit_transform(X)
        
        # Check shape preserved
        self.assertEqual(X_normalized.shape, X.shape)
        
        # Check values are standardized (mean ~0, std ~1)
        # Note: With only 3 samples, this is approximate
        self.assertTrue(np.abs(X_normalized.mean()) < 1.0)


class TestModel(unittest.TestCase):
    """Test ML model predictions"""
    
    @classmethod
    def setUpClass(cls):
        """Load trained model once for all tests"""
        try:
            model_path = "../../data/models/flood_model.pkl"
            scaler_path = "../../data/processed/scaler.pkl"
            
            if not os.path.exists(model_path):
                model_path = "../data/models/flood_model.pkl"
                scaler_path = "../data/processed/scaler.pkl"
            
            cls.predictor = FloodRiskPredictor(model_path, scaler_path)
            cls.model_loaded = True
        except:
            cls.model_loaded = False
    
    def test_model_loaded(self):
        """Test that model can be loaded"""
        self.assertTrue(self.model_loaded, "Model should be loaded successfully")
    
    def test_safe_prediction(self):
        """Test prediction for safe conditions"""
        if not self.model_loaded:
            self.skipTest("Model not loaded")
        
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
        
        result = self.predictor.predict_single(safe_features)
        
        # Should predict Safe (level 0) or Warning (level 1)
        self.assertIn(result['risk_level'], [0, 1], "Safe conditions should predict low risk")
        self.assertIn(result['risk_label'], ['Safe', 'Warning'])
    
    def test_critical_prediction(self):
        """Test prediction for critical conditions"""
        if not self.model_loaded:
            self.skipTest("Model not loaded")
        
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
        
        result = self.predictor.predict_single(critical_features)
        
        # Should predict High Risk or Critical
        self.assertIn(result['risk_level'], [2, 3], "Critical conditions should predict high risk")
        self.assertIn(result['risk_label'], ['High Risk', 'Critical'])
    
    def test_prediction_structure(self):
        """Test that prediction returns correct structure"""
        if not self.model_loaded:
            self.skipTest("Model not loaded")
        
        features = {
            'rainfall_mm': 100.0,
            'rainfall_7day_avg': 80.0,
            'rainfall_intensity': 10.0,
            'river_level_m': 6.0,
            'river_level_change': 0.5,
            'soil_moisture_percent': 70.0,
            'elevation_m': 100.0,
            'temperature_celsius': 26.0,
            'humidity_percent': 80.0,
            'wind_speed_kmh': 15.0,
            'distance_to_river_km': 2.0,
            'month': 7
        }
        
        result = self.predictor.predict_single(features)
        
        # Check required fields
        self.assertIn('risk_level', result)
        self.assertIn('risk_label', result)
        self.assertIn('probability', result)
        self.assertIn('probabilities', result)
        self.assertIn('description', result)
        self.assertIn('recommended_action', result)
        
        # Check types
        self.assertIsInstance(result['risk_level'], int)
        self.assertIsInstance(result['risk_label'], str)
        self.assertIsInstance(result['probability'], float)
        
        # Check ranges
        self.assertIn(result['risk_level'], [0, 1, 2, 3])
        self.assertGreaterEqual(result['probability'], 0.0)
        self.assertLessEqual(result['probability'], 1.0)
    
    def test_probability_sum(self):
        """Test that probabilities sum to 1"""
        if not self.model_loaded:
            self.skipTest("Model not loaded")
        
        features = {
            'rainfall_mm': 100.0,
            'rainfall_7day_avg': 80.0,
            'rainfall_intensity': 10.0,
            'river_level_m': 6.0,
            'river_level_change': 0.5,
            'soil_moisture_percent': 70.0,
            'elevation_m': 100.0,
            'temperature_celsius': 26.0,
            'humidity_percent': 80.0,
            'wind_speed_kmh': 15.0,
            'distance_to_river_km': 2.0,
            'month': 7
        }
        
        result = self.predictor.predict_single(features)
        probs = result['probabilities']
        
        total = probs['safe'] + probs['warning'] + probs['high_risk'] + probs['critical']
        
        self.assertAlmostEqual(total, 1.0, places=5, msg="Probabilities should sum to 1")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""
    
    @classmethod
    def setUpClass(cls):
        """Load model for edge case testing"""
        try:
            model_path = "../../data/models/flood_model.pkl"
            scaler_path = "../../data/processed/scaler.pkl"
            
            if not os.path.exists(model_path):
                model_path = "../data/models/flood_model.pkl"
                scaler_path = "../data/processed/scaler.pkl"
            
            cls.predictor = FloodRiskPredictor(model_path, scaler_path)
            cls.model_loaded = True
        except:
            cls.model_loaded = False
    
    def test_zero_rainfall(self):
        """Test with zero rainfall"""
        if not self.model_loaded:
            self.skipTest("Model not loaded")
        
        features = {
            'rainfall_mm': 0.0,
            'rainfall_7day_avg': 0.0,
            'rainfall_intensity': 0.0,
            'river_level_m': 2.0,
            'river_level_change': 0.0,
            'soil_moisture_percent': 30.0,
            'elevation_m': 200.0,
            'temperature_celsius': 28.0,
            'humidity_percent': 50.0,
            'wind_speed_kmh': 10.0,
            'distance_to_river_km': 10.0,
            'month': 3
        }
        
        result = self.predictor.predict_single(features)
        
        # Zero rainfall should predict safe
        self.assertEqual(result['risk_level'], 0, "Zero rainfall should predict safe")
    
    def test_max_values(self):
        """Test with maximum values"""
        if not self.model_loaded:
            self.skipTest("Model not loaded")
        
        features = {
            'rainfall_mm': 500.0,  # Max
            'rainfall_7day_avg': 300.0,  # Max
            'rainfall_intensity': 50.0,  # Max
            'river_level_m': 15.0,  # Max
            'river_level_change': 5.0,  # Max
            'soil_moisture_percent': 100.0,  # Max
            'elevation_m': 0.0,  # Min (sea level)
            'temperature_celsius': 45.0,  # Max
            'humidity_percent': 100.0,  # Max
            'wind_speed_kmh': 100.0,  # Max
            'distance_to_river_km': 0.0,  # Min
            'month': 8  # Monsoon
        }
        
        result = self.predictor.predict_single(features)
        
        # Extreme values should predict critical
        self.assertEqual(result['risk_level'], 3, "Extreme conditions should predict critical")
    
    def test_different_months(self):
        """Test predictions across different months"""
        if not self.model_loaded:
            self.skipTest("Model not loaded")
        
        base_features = {
            'rainfall_mm': 100.0,
            'rainfall_7day_avg': 80.0,
            'rainfall_intensity': 10.0,
            'river_level_m': 6.0,
            'river_level_change': 0.5,
            'soil_moisture_percent': 70.0,
            'elevation_m': 100.0,
            'temperature_celsius': 26.0,
            'humidity_percent': 80.0,
            'wind_speed_kmh': 15.0,
            'distance_to_river_km': 2.0,
            'month': 1
        }
        
        # Test all months
        for month in range(1, 13):
            features = base_features.copy()
            features['month'] = month
            
            result = self.predictor.predict_single(features)
            
            # Should return valid risk level for all months
            self.assertIn(result['risk_level'], [0, 1, 2, 3], 
                         f"Month {month} should return valid risk level")


def run_ml_tests():
    """Run all ML tests"""
    
    print("\n" + "="*70)
    print(" "*20 + "🧪 ML COMPONENT TESTS")
    print("="*70 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestSchema))
    suite.addTests(loader.loadTestsFromTestCase(TestPreprocessing))
    suite.addTests(loader.loadTestsFromTestCase(TestModel))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failed: {len(result.failures)}")
    print(f"⚠️  Errors: {len(result.errors)}")
    print(f"⏭️  Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print("\n⚠️  SOME TESTS FAILED")
    
    print("="*70 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_ml_tests()
    sys.exit(0 if success else 1)