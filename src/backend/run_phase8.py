"""
Phase 8 - Live Weather Integration Demo
Demonstrates real-time weather data integration with flood prediction
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from weather_api import WeatherAPIClient
from flood_assessment import FloodRiskAssessor
from risk_scoring import format_alert_for_display
import time


def demo_weather_integration():
    """Demonstrate live weather integration"""
    
    print("\n" + "="*70)
    print(" "*15 + "🌦️  PHASE 8: LIVE WEATHER INTEGRATION")
    print("="*70 + "\n")
    
    print("This demo shows:")
    print("  1. Fetching real-time weather from OpenWeatherMap")
    print("  2. Transforming weather data to model features")
    print("  3. Making flood predictions with live data")
    print("  4. Generating location-specific alerts")
    print("\n" + "-"*70 + "\n")
    
    # Initialize clients
    print("🔧 Initializing systems...")
    weather_client = WeatherAPIClient()
    assessor = FloodRiskAssessor()
    print("✅ Systems ready!\n")
    
    # Test cities
    cities = [
        ("Lucknow", "Uttar Pradesh"),
        ("Mumbai", "Maharashtra"),
        ("Patna", "Bihar"),
        ("Kolkata", "West Bengal")
    ]
    
    for city, state in cities:
        print("\n" + "="*70)
        print(f"📍 ANALYZING: {city}, {state}")
        print("="*70)
        
        try:
            # Step 1: Fetch weather data
            print(f"\n1️⃣  Fetching live weather data...")
            start_time = time.time()
            weather_data = weather_client.get_current_weather(city)
            fetch_time = (time.time() - start_time) * 1000
            
            # Display weather
            if 'main' in weather_data:
                print(f"\n   Current Weather in {city}:")
                print(f"   🌡️  Temperature: {weather_data['main']['temp']:.1f}°C")
                print(f"   💧 Humidity: {weather_data['main']['humidity']}%")
                
                if 'wind' in weather_data:
                    wind_speed_kmh = weather_data['wind']['speed'] * 3.6
                    print(f"   💨 Wind: {wind_speed_kmh:.1f} km/h")
                
                if 'rain' in weather_data and '1h' in weather_data['rain']:
                    print(f"   🌧️  Rain (1h): {weather_data['rain']['1h']} mm")
                else:
                    print(f"   ☀️  No rain detected")
                
                if 'weather' in weather_data and len(weather_data['weather']) > 0:
                    desc = weather_data['weather'][0]['description']
                    print(f"   ☁️  Conditions: {desc.title()}")
            
            print(f"\n   ⏱️  Fetch time: {fetch_time:.2f} ms")
            
            # Step 2: Transform to features
            print(f"\n2️⃣  Transforming to model features...")
            start_time = time.time()
            features = weather_client.transform_to_features(weather_data, city)
            transform_time = (time.time() - start_time) * 1000
            print(f"   ⏱️  Transform time: {transform_time:.2f} ms")
            
            # Step 3: Make prediction
            print(f"\n3️⃣  Running flood risk prediction...")
            start_time = time.time()
            assessment = assessor.assess_flood_risk(
                features,
                location=f"{city}, {state}",
                include_detailed_conditions=True
            )
            predict_time = (time.time() - start_time) * 1000
            
            # Display prediction
            alert = assessment
            print(f"\n   🎯 PREDICTION RESULT:")
            print(f"   Risk Level: {alert['risk_level']} - {alert['risk_label']}")
            print(f"   Confidence: {assessment['prediction']['confidence']*100:.1f}%")
            print(f"   Severity: {alert['severity']}")
            print(f"   ⏱️  Prediction time: {predict_time:.2f} ms")
            
            # Show alert title and key actions
            print(f"\n   📢 ALERT:")
            print(f"   {alert['title']}")
            
            if alert.get('additional_info'):
                print(f"\n   ⚠️  Critical Factors:")
                for info in alert['additional_info'][:3]:
                    print(f"      {info}")
            
            print(f"\n   📋 Top Recommended Actions:")
            for i, action in enumerate(alert['recommended_actions'][:3], 1):
                print(f"      {i}. {action}")
            
            if len(alert['recommended_actions']) > 3:
                print(f"      ... and {len(alert['recommended_actions']) - 3} more")
            
            # Total time
            total_time = fetch_time + transform_time + predict_time
            print(f"\n   ⏱️  Total processing time: {total_time:.2f} ms")
            
            # Pause between cities
            if city != cities[-1][0]:
                print("\n" + "-"*70)
                time.sleep(1)
            
        except Exception as e:
            print(f"\n   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print("\n" + "="*70)
    print(" "*20 + "✅ DEMO COMPLETE!")
    print("="*70)
    
    print("\n📊 System Performance:")
    print("   • Weather fetch: ~50-200 ms (depends on API response)")
    print("   • Feature transform: ~5-10 ms")
    print("   • Flood prediction: ~100-150 ms")
    print("   • Total end-to-end: ~200-400 ms")
    
    print("\n🎯 Key Features Demonstrated:")
    print("   ✅ Real-time weather data fetching")
    print("   ✅ Automatic feature transformation")
    print("   ✅ Location-specific predictions")
    print("   ✅ Multi-city monitoring")
    print("   ✅ Fast processing (<400ms)")
    
    print("\n💡 Production Enhancements:")
    print("   • Add river gauge data integration")
    print("   • Use historical rainfall databases")
    print("   • Implement geospatial elevation API")
    print("   • Add soil moisture sensor networks")
    print("   • Enable weather forecast predictions")
    
    print("\n🚀 Next Step: Phase 10 - Dashboard Frontend")
    print("="*70 + "\n")


def test_single_city():
    """Quick test with a single city"""
    
    print("\n" + "="*70)
    print(" "*15 + "🧪 QUICK WEATHER TEST")
    print("="*70 + "\n")
    
    city = input("Enter city name (default: Lucknow): ").strip() or "Lucknow"
    
    weather_client = WeatherAPIClient()
    assessor = FloodRiskAssessor()
    
    print(f"\n🌐 Fetching weather for {city}...")
    weather = weather_client.get_current_weather(city)
    
    print(f"🔄 Transforming data...")
    features = weather_client.transform_to_features(weather, city)
    
    print(f"🎯 Making prediction...")
    assessment = assessor.assess_flood_risk(features, city)
    
    print(f"\n" + "="*70)
    print(format_alert_for_display(assessment))


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        test_single_city()
    else:
        demo_weather_integration()