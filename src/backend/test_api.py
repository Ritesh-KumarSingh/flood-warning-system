"""
API Testing Script
Tests all FastAPI endpoints with sample requests
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"


def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70 + "\n")


def test_root():
    """Test root endpoint"""
    print_section("1️⃣  Testing Root Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_health():
    """Test health check endpoint"""
    print_section("2️⃣  Testing Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Status: {data['status']}")
        print(f"Model Loaded: {data['model_loaded']}")
        print(f"Timestamp: {data['timestamp']}")
        return response.status_code == 200 and data['model_loaded']
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_prediction_safe():
    """Test prediction with safe conditions"""
    print_section("3️⃣  Testing Prediction - Safe Conditions")
    
    payload = {
        "features": {
            "rainfall_mm": 15.0,
            "rainfall_7day_avg": 20.0,
            "rainfall_intensity": 2.0,
            "river_level_m": 3.5,
            "river_level_change": 0.1,
            "soil_moisture_percent": 45.0,
            "elevation_m": 200.0,
            "temperature_celsius": 28.0,
            "humidity_percent": 65.0,
            "wind_speed_kmh": 12.0,
            "distance_to_river_km": 5.0,
            "month": 3
        },
        "location": "Mumbai",
        "include_detailed_analysis": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            alert = data['alert']
            print(f"\n📊 Prediction Result:")
            print(f"   Location: {alert['location']}")
            print(f"   Risk Level: {alert['risk_level']} ({alert['risk_label']})")
            print(f"   Severity: {alert['severity']}")
            print(f"   Confidence: {data['prediction']['confidence']*100:.1f}%")
            print(f"   Processing Time: {data['processing_time_ms']:.2f} ms")
            print(f"\n   Title: {alert['title']}")
            print(f"   Actions: {len(alert['recommended_actions'])} recommended")
            return True
        else:
            print(f"❌ Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_prediction_critical():
    """Test prediction with critical conditions"""
    print_section("4️⃣  Testing Prediction - Critical Conditions")
    
    payload = {
        "features": {
            "rainfall_mm": 340.0,
            "rainfall_7day_avg": 215.0,
            "rainfall_intensity": 32.0,
            "river_level_m": 13.2,
            "river_level_change": 4.1,
            "soil_moisture_percent": 96.0,
            "elevation_m": 18.0,
            "temperature_celsius": 23.0,
            "humidity_percent": 95.0,
            "wind_speed_kmh": 28.0,
            "distance_to_river_km": 0.4,
            "month": 8
        },
        "location": "Ayodhya",
        "include_detailed_analysis": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            alert = data['alert']
            print(f"\n📊 Prediction Result:")
            print(f"   Location: {alert['location']}")
            print(f"   Risk Level: {alert['risk_level']} ({alert['risk_label']})")
            print(f"   Severity: {alert['severity']}")
            print(f"   Confidence: {data['prediction']['confidence']*100:.1f}%")
            print(f"   Processing Time: {data['processing_time_ms']:.2f} ms")
            print(f"\n   Title: {alert['title']}")
            
            if alert['additional_info']:
                print(f"\n   🚨 Critical Warnings:")
                for warning in alert['additional_info'][:3]:
                    print(f"      {warning}")
            
            print(f"\n   Emergency Contacts: {len(alert['emergency_contacts'])}")
            return True
        else:
            print(f"❌ Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_quick_check():
    """Test quick check endpoint"""
    print_section("5️⃣  Testing Quick Check")
    
    payload = {
        "features": {
            "rainfall_mm": 95.0,
            "rainfall_7day_avg": 65.0,
            "rainfall_intensity": 10.0,
            "river_level_m": 7.2,
            "river_level_change": 0.8,
            "soil_moisture_percent": 72.0,
            "elevation_m": 85.0,
            "temperature_celsius": 26.0,
            "humidity_percent": 82.0,
            "wind_speed_kmh": 18.0,
            "distance_to_river_km": 2.3,
            "month": 7
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/quick-check", json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📊 Quick Check Result:")
            print(f"   Risk Level: {data['risk_level']} ({data['risk_label']})")
            print(f"   Confidence: {data['confidence']*100:.1f}%")
            print(f"   Action: {data['action']}")
            return True
        else:
            print(f"❌ Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_risk_levels():
    """Test risk levels info endpoint"""
    print_section("6️⃣  Testing Risk Levels Info")
    
    try:
        response = requests.get(f"{BASE_URL}/risk-levels")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nRisk Levels:")
            for level, info in data['risk_levels'].items():
                print(f"   Level {level}: {info['label']} ({info['color']}) - {info['threshold']}")
            return True
        else:
            print(f"❌ Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_features_info():
    """Test features info endpoint"""
    print_section("7️⃣  Testing Features Info")
    
    try:
        response = requests.get(f"{BASE_URL}/features")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nTotal Features: {data['total_features']}")
            print(f"\nSample Features:")
            for i, (key, info) in enumerate(list(data['features'].items())[:3]):
                print(f"   {info['name']}: {info['range']} {info['unit']}")
            print(f"   ... and {data['total_features'] - 3} more")
            return True
        else:
            print(f"❌ Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def run_all_tests():
    """Run all API tests"""
    print("\n" + "="*70)
    print(" "*15 + "🧪 FLOOD WARNING API TESTS")
    print("="*70)
    
    print("\n⚠️  Make sure the API server is running!")
    print("   Run: python main.py")
    print("\n   Waiting 3 seconds for you to start the server...")
    time.sleep(3)
    
    results = []
    
    # Run tests
    results.append(("Root Endpoint", test_root()))
    results.append(("Health Check", test_health()))
    results.append(("Prediction - Safe", test_prediction_safe()))
    results.append(("Prediction - Critical", test_prediction_critical()))
    results.append(("Quick Check", test_quick_check()))
    results.append(("Risk Levels Info", test_risk_levels()))
    results.append(("Features Info", test_features_info()))
    
    # Summary
    print_section("📊 TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{'='*70}")
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("🎉 All tests passed! API is working perfectly!")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    run_all_tests()