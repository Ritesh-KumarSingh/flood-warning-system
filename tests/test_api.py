"""
API Endpoint Tests
Tests FastAPI endpoints and integration
"""

import unittest
import requests
import time
import sys
import os

BASE_URL = "http://localhost:8000"


class TestAPIEndpoints(unittest.TestCase):
    """Test API endpoint functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Check if API server is running"""
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            cls.server_running = response.status_code == 200
        except:
            cls.server_running = False
            print("\n⚠️  Warning: API server not running. Start with: python src/backend/main.py")
    
    def test_root_endpoint(self):
        """Test root endpoint returns API info"""
        if not self.server_running:
            self.skipTest("API server not running")
        
        response = requests.get(f"{BASE_URL}/")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('message', data)
        self.assertIn('version', data)
        self.assertIn('endpoints', data)
    
    def test_health_check(self):
        """Test health check endpoint"""
        if not self.server_running:
            self.skipTest("API server not running")
        
        response = requests.get(f"{BASE_URL}/health")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'healthy')
        self.assertTrue(data['model_loaded'])
    
    def test_predict_endpoint(self):
        """Test prediction endpoint with valid data"""
        if not self.server_running:
            self.skipTest("API server not running")
        
        payload = {
            "features": {
                "rainfall_mm": 100.0,
                "rainfall_7day_avg": 80.0,
                "rainfall_intensity": 10.0,
                "river_level_m": 6.0,
                "river_level_change": 0.5,
                "soil_moisture_percent": 70.0,
                "elevation_m": 100.0,
                "temperature_celsius": 26.0,
                "humidity_percent": 80.0,
                "wind_speed_kmh": 15.0,
                "distance_to_river_km": 2.0,
                "month": 7
            },
            "location": "Test City"
        }
        
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check response structure
        self.assertTrue(data['success'])
        self.assertIn('alert', data)
        self.assertIn('prediction', data)
        self.assertIn('risk_score', data)
        self.assertIn('processing_time_ms', data)
        
        # Check alert structure
        alert = data['alert']
        self.assertIn('risk_level', alert)
        self.assertIn('risk_label', alert)
        self.assertIn('title', alert)
        self.assertIn('message', alert)
        self.assertIn('recommended_actions', alert)
        
        # Validate risk level
        self.assertIn(alert['risk_level'], [0, 1, 2, 3])
    
    def test_predict_invalid_data(self):
        """Test prediction with invalid data"""
        if not self.server_running:
            self.skipTest("API server not running")
        
        # Missing required field
        payload = {
            "features": {
                "rainfall_mm": 100.0,
                # Missing other required fields
            },
            "location": "Test City"
        }
        
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        
        # Should return validation error
        self.assertEqual(response.status_code, 422)
    
    def test_predict_out_of_range(self):
        """Test prediction with out-of-range values"""
        if not self.server_running:
            self.skipTest("API server not running")
        
        payload = {
            "features": {
                "rainfall_mm": -10.0,  # Negative (invalid)
                "rainfall_7day_avg": 80.0,
                "rainfall_intensity": 10.0,
                "river_level_m": 6.0,
                "river_level_change": 0.5,
                "soil_moisture_percent": 70.0,
                "elevation_m": 100.0,
                "temperature_celsius": 26.0,
                "humidity_percent": 80.0,
                "wind_speed_kmh": 15.0,
                "distance_to_river_km": 2.0,
                "month": 7
            },
            "location": "Test City"
        }
        
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        
        # Should return validation error
        self.assertEqual(response.status_code, 422)
    
    def test_quick_check_endpoint(self):
        """Test quick check endpoint"""
        if not self.server_running:
            self.skipTest("API server not running")
        
        payload = {
            "features": {
                "rainfall_mm": 100.0,
                "rainfall_7day_avg": 80.0,
                "rainfall_intensity": 10.0,
                "river_level_m": 6.0,
                "river_level_change": 0.5,
                "soil_moisture_percent": 70.0,
                "elevation_m": 100.0,
                "temperature_celsius": 26.0,
                "humidity_percent": 80.0,
                "wind_speed_kmh": 15.0,
                "distance_to_river_km": 2.0,
                "month": 7
            }
        }
        
        response = requests.post(f"{BASE_URL}/quick-check", json=payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check simplified response
        self.assertTrue(data['success'])
        self.assertIn('risk_level', data)
        self.assertIn('risk_label', data)
        self.assertIn('confidence', data)
        self.assertIn('action', data)
    
    def test_risk_levels_info(self):
        """Test risk levels information endpoint"""
        if not self.server_running:
            self.skipTest("API server not running")
        
        response = requests.get(f"{BASE_URL}/risk-levels")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn('risk_levels', data)
        risk_levels = data['risk_levels']
        
        # Should have all 4 levels
        self.assertEqual(len(risk_levels), 4)
        self.assertIn('0', risk_levels)
        self.assertIn('3', risk_levels)
    
    def test_features_info(self):
        """Test features information endpoint"""
        if not self.server_running:
            self.skipTest("API server not running")
        
        response = requests.get(f"{BASE_URL}/features")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn('features', data)
        self.assertIn('total_features', data)
        self.assertEqual(data['total_features'], 12)


class TestAPIPerformance(unittest.TestCase):
    """Test API performance benchmarks"""
    
    @classmethod
    def setUpClass(cls):
        """Check if API server is running"""
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            cls.server_running = response.status_code == 200
        except:
            cls.server_running = False
    
    def test_prediction_response_time(self):
        """Test prediction response time is acceptable"""
        if not self.server_running:
            self.skipTest("API server not running")
        
        payload = {
            "features": {
                "rainfall_mm": 100.0,
                "rainfall_7day_avg": 80.0,
                "rainfall_intensity": 10.0,
                "river_level_m": 6.0,
                "river_level_change": 0.5,
                "soil_moisture_percent": 70.0,
                "elevation_m": 100.0,
                "temperature_celsius": 26.0,
                "humidity_percent": 80.0,
                "wind_speed_kmh": 15.0,
                "distance_to_river_km": 2.0,
                "month": 7
            },
            "location": "Test City"
        }
        
        # Warm-up request (first request loads model, so it's slower)
        requests.post(f"{BASE_URL}/predict", json=payload)
        
        # Now test actual response time
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        response_time = (time.time() - start_time) * 1000  # ms
        
        self.assertEqual(response.status_code, 200)
        
        # Response should be under 2 seconds (generous for warm request)
        self.assertLess(response_time, 2000, 
                       f"Response time {response_time:.0f}ms exceeds 2000ms")
        
        # Check processing time reported by API
        data = response.json()
        processing_time = data.get('processing_time_ms', 0)
        
        # Processing time should be reasonable
        self.assertLess(processing_time, 1000,
                       f"Processing time {processing_time:.0f}ms exceeds 1000ms")
    
    def test_concurrent_requests(self):
        """Test handling multiple concurrent requests"""
        if not self.server_running:
            self.skipTest("API server not running")
        
        import concurrent.futures
        
        payload = {
            "features": {
                "rainfall_mm": 100.0,
                "rainfall_7day_avg": 80.0,
                "rainfall_intensity": 10.0,
                "river_level_m": 6.0,
                "river_level_change": 0.5,
                "soil_moisture_percent": 70.0,
                "elevation_m": 100.0,
                "temperature_celsius": 26.0,
                "humidity_percent": 80.0,
                "wind_speed_kmh": 15.0,
                "distance_to_river_km": 2.0,
                "month": 7
            },
            "location": "Test City"
        }
        
        def make_request():
            response = requests.post(f"{BASE_URL}/predict", json=payload)
            return response.status_code == 200
        
        # Send 5 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(5)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # All should succeed
        self.assertEqual(sum(results), 5, "All concurrent requests should succeed")


def run_api_tests():
    """Run all API tests"""
    
    print("\n" + "="*70)
    print(" "*20 + "🌐 API ENDPOINT TESTS")
    print("="*70 + "\n")
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code != 200:
            print("⚠️  API server not responding properly")
            print("   Start server: python src/backend/main.py")
            return False
    except:
        print("❌ API server not running!")
        print("   Start server first: python src/backend/main.py")
        print("   Then run tests again")
        return False
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestAPIEndpoints))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIPerformance))
    
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
    
    if result.wasSuccessful():
        print("\n🎉 ALL API TESTS PASSED!")
    else:
        print("\n⚠️  SOME API TESTS FAILED")
    
    print("="*70 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_api_tests()
    sys.exit(0 if success else 1)