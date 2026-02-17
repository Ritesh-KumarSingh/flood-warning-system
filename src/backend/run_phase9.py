"""
Phase 9 - Alert Engine Demonstration
Shows SMS, Email, and Push Notification delivery
"""

import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from alert_engine import AlertEngine, AlertChannel
from flood_assessment import FloodRiskAssessor
from weather_api import WeatherAPIClient
from datetime import datetime


def run_phase_9():
    """Execute Phase 9 - Alert Engine Demo"""
    
    print("\n" + "="*70)
    print(" "*15 + "🚀 PHASE 9: ALERT ENGINE")
    print("="*70 + "\n")
    
    print("This phase demonstrates:")
    print("  1. Alert triggering based on risk thresholds")
    print("  2. SMS notifications (via Twilio)")
    print("  3. Email alerts")
    print("  4. Push notifications (simulated)")
    print("  5. Multi-channel alert delivery")
    print("  6. Bulk alerting for multiple locations")
    print("\n" + "-"*70 + "\n")
    
    # Initialize systems
    print("🔧 Initializing systems...")
    alert_engine = AlertEngine(demo_mode=True)
    assessor = FloodRiskAssessor()
    weather_client = WeatherAPIClient()
    print("✅ Systems ready!\n")
    
    # Scenario 1: Safe condition (no alert)
    print("="*70)
    print("SCENARIO 1: Safe Weather Conditions")
    print("="*70 + "\n")
    
    print("📍 Location: Bangalore")
    print("🌡️  Current conditions: Light rain, normal river levels\n")
    
    safe_features = {
        'rainfall_mm': 15.0,
        'rainfall_7day_avg': 20.0,
        'rainfall_intensity': 2.0,
        'river_level_m': 3.5,
        'river_level_change': 0.1,
        'soil_moisture_percent': 45.0,
        'elevation_m': 920.0,
        'temperature_celsius': 24.0,
        'humidity_percent': 65.0,
        'wind_speed_kmh': 12.0,
        'distance_to_river_km': 5.0,
        'month': 3
    }
    
    assessment_safe = assessor.assess_flood_risk(safe_features, "Bangalore")
    
    print(f"🎯 Prediction: {assessment_safe['risk_label']} (Level {assessment_safe['risk_level']})")
    print(f"📊 Confidence: {assessment_safe['prediction']['confidence']*100:.1f}%\n")
    
    if alert_engine.should_send_alert(assessment_safe['risk_level']):
        print("⚠️  Alert would be sent")
    else:
        print("✅ No alert needed - conditions are safe")
        print("   (Alert threshold: Level 1 - Warning or higher)")
    
    print("\n" + "-"*70 + "\n")
    
    # Scenario 2: Warning condition (send alerts)
    print("="*70)
    print("SCENARIO 2: Warning Conditions - Moderate Risk")
    print("="*70 + "\n")
    
    print("📍 Location: Patna")
    print("🌧️  Current conditions: Heavy rainfall, rising water levels\n")
    
    warning_features = {
        'rainfall_mm': 95.0,
        'rainfall_7day_avg': 65.0,
        'rainfall_intensity': 10.0,
        'river_level_m': 7.2,
        'river_level_change': 0.8,
        'soil_moisture_percent': 72.0,
        'elevation_m': 53.0,
        'temperature_celsius': 26.0,
        'humidity_percent': 82.0,
        'wind_speed_kmh': 18.0,
        'distance_to_river_km': 2.3,
        'month': 7
    }
    
    assessment_warning = assessor.assess_flood_risk(warning_features, "Patna")
    
    print(f"🎯 Prediction: {assessment_warning['risk_label']} (Level {assessment_warning['risk_level']})")
    print(f"📊 Confidence: {assessment_warning['prediction']['confidence']*100:.1f}%\n")
    
    if alert_engine.should_send_alert(assessment_warning['risk_level']):
        print("⚠️  ALERT TRIGGERED! Sending notifications...\n")
        
        result = alert_engine.send_alert(
            assessment_warning,
            phone_numbers=['+91-9876543210', '+91-8765432109'],
            email_addresses=['patna.admin@example.com', 'emergency@example.com'],
            channels=[AlertChannel.ALL]
        )
        
        print(f"\n📊 Delivery Report:")
        print(f"   Timestamp: {result['timestamp']}")
        print(f"   Location: {result['location']}")
        print(f"   Risk Level: {result['risk_level']}")
        print(f"   Channels: {len(result['deliveries'])}")
        
        for delivery in result['deliveries']:
            print(f"\n   ✅ {delivery['channel']}: {delivery['status']}")
    
    print("\n" + "-"*70 + "\n")
    
    # Scenario 3: Critical emergency (urgent alerts)
    print("="*70)
    print("SCENARIO 3: CRITICAL EMERGENCY - Immediate Evacuation")
    print("="*70 + "\n")
    
    print("📍 Location: Ayodhya")
    print("🚨 Current conditions: EXTREME rainfall, DANGER-level river\n")
    
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
    
    assessment_critical = assessor.assess_flood_risk(critical_features, "Ayodhya")
    
    print(f"🎯 Prediction: {assessment_critical['risk_label']} (Level {assessment_critical['risk_level']})")
    print(f"📊 Confidence: {assessment_critical['prediction']['confidence']*100:.1f}%\n")
    
    if assessment_critical.get('additional_info'):
        print("⚠️  Critical Conditions Detected:")
        for info in assessment_critical['additional_info'][:3]:
            print(f"   {info}")
        print()
    
    if alert_engine.should_send_alert(assessment_critical['risk_level']):
        print("🚨 CRITICAL ALERT! Broadcasting emergency notifications...\n")
        
        result = alert_engine.send_alert(
            assessment_critical,
            phone_numbers=[
                '+91-1234567890',  # District admin
                '+91-2345678901',  # Emergency services
                '+91-3456789012',  # Local authority
                '+91-4567890123'   # Relief coordinator
            ],
            email_addresses=[
                'ayodhya.district@gov.in',
                'emergency.response@gov.in',
                'ndrf@gov.in'
            ],
            channels=[AlertChannel.ALL]
        )
        
        print(f"\n📊 Emergency Broadcast Report:")
        print(f"   Timestamp: {result['timestamp']}")
        print(f"   Location: {result['location']}")
        print(f"   Risk Level: CRITICAL ({result['risk_level']})")
        print(f"   Priority: HIGHEST")
        
        for delivery in result['deliveries']:
            print(f"\n   🚨 {delivery['channel']}: {delivery['status']}")
            if 'recipients' in delivery:
                print(f"      Recipients: {delivery['recipients']}")
    
    print("\n" + "-"*70 + "\n")
    
    # Scenario 4: Multi-city bulk alerting
    print("="*70)
    print("SCENARIO 4: Multi-City Monitoring & Bulk Alerts")
    print("="*70 + "\n")
    
    print("📡 Monitoring 4 cities simultaneously...\n")
    
    cities = [
        ("Lucknow", safe_features),
        ("Varanasi", warning_features),
        ("Gorakhpur", critical_features),
        ("Ayodhya", critical_features)
    ]
    
    assessments = []
    for city, features in cities:
        assessment = assessor.assess_flood_risk(features, city)
        assessments.append(assessment)
        
        emoji = ["✅", "⚠️", "🚨", "🔴"][assessment['risk_level']]
        print(f"{emoji} {city:15s}: {assessment['risk_label']:15s} "
              f"(Confidence: {assessment['prediction']['confidence']*100:.1f}%)")
    
    print("\n📞 Sending alerts to registered users in affected areas...\n")
    
    # Contact database (in production, this would be from a database)
    contact_database = {
        'Lucknow': {
            'phones': ['+91-1111111111'],
            'emails': ['lucknow@alert.system']
        },
        'Varanasi': {
            'phones': ['+91-2222222222', '+91-3333333333'],
            'emails': ['varanasi@alert.system']
        },
        'Gorakhpur': {
            'phones': ['+91-4444444444', '+91-5555555555', '+91-6666666666'],
            'emails': ['gorakhpur@alert.system', 'emergency.gorakhpur@gov.in']
        },
        'Ayodhya': {
            'phones': ['+91-7777777777', '+91-8888888888'],
            'emails': ['ayodhya@alert.system']
        }
    }
    
    bulk_results = alert_engine.send_bulk_alerts(assessments, contact_database)
    
    print(f"✅ Bulk alert processing complete!")
    print(f"   Total assessments: {len(assessments)}")
    print(f"   Alerts sent: {len(bulk_results)}")
    print(f"   Cities safe (no alert): {len(assessments) - len(bulk_results)}")
    
    # Summary
    print("\n" + "="*70)
    print(" "*20 + "📊 PHASE 9 SUMMARY")
    print("="*70 + "\n")
    
    print("✅ Alert Engine Features Demonstrated:")
    print("   • Threshold-based alert triggering")
    print("   • SMS notifications (via Twilio)")
    print("   • Email alerts (SMTP)")
    print("   • Push notifications (simulated)")
    print("   • Multi-channel delivery")
    print("   • Bulk alerting for multiple locations")
    print("   • Alert logging and tracking")
    
    print("\n📱 Supported Channels:")
    print("   • SMS: Concise 160-char emergency messages")
    print("   • Email: Detailed alerts with full recommendations")
    print("   • Push: Real-time mobile notifications")
    
    print("\n🎯 Alert Thresholds:")
    print("   • Level 0 (Safe): No alert")
    print("   • Level 1 (Warning): Alert sent")
    print("   • Level 2 (High Risk): Urgent alert sent")
    print("   • Level 3 (Critical): Emergency broadcast")
    
    print("\n💡 Production Features:")
    print("   • Twilio SMS integration (requires API key)")
    print("   • SMTP email delivery (requires credentials)")
    print("   • Firebase/APNS push notifications")
    print("   • Alert deduplication")
    print("   • Delivery status tracking")
    print("   • Retry logic for failed deliveries")
    
    print("\n🚀 Next Step: Phase 10 - Dashboard Frontend")
    print("   Create interactive Streamlit dashboard for visualization")
    print("="*70 + "\n")


if __name__ == "__main__":
    run_phase_9()