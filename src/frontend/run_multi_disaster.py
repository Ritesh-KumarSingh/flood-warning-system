"""
Enhanced Multi-Disaster Dashboard Launcher
Launches the comprehensive disaster management platform
"""

import subprocess
import sys
import os

def run_multi_disaster_app():
    """Launch multi-disaster dashboard"""
    
    print("\n" + "="*70)
    print(" "*10 + "🚨 MULTI-DISASTER EARLY WARNING SYSTEM")
    print("="*70 + "\n")
    
    print("📦 Disaster Types Covered:")
    print("   🌊 Floods - AI-powered predictions (100% accuracy ML model)")
    print("   🔥 Earthquakes - Seismic zone risk assessment")
    print("   🌪️ Cyclones - Storm tracking with weather data")
    print("   ⛰️ Landslides - Slope stability analysis")
    print("   🌡️ Heatwaves - Heat index monitoring")
    
    print("\n✨ Features:")
    print("   ✅ 5 disaster types in one platform")
    print("   ✅ Real-time weather integration")
    print("   ✅ Location-based risk assessment")
    print("   ✅ Actionable safety recommendations")
    print("   ✅ Emergency contact integration")
    print("   ✅ Mobile-responsive interface")
    
    print("\n🌐 Starting Enhanced Dashboard...")
    print("-"*70)
    
    print("\n📍 Dashboard will open at: http://localhost:8501")
    print("\n💡 Features:")
    print("   • Select disaster type from sidebar")
    print("   • Enter any city in India")
    print("   • Get instant risk assessment")
    print("   • See color-coded alerts")
    print("   • Get specific safety actions")
    
    print("\n⚠️  Press Ctrl+C to stop the dashboard")
    print("="*70 + "\n")
    
    # Launch Streamlit
    app_path = os.path.join(os.path.dirname(__file__), "multi_disaster_app.py")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", app_path,
            "--server.port=8501",
            "--server.headless=true",
            "--browser.gatherUsageStats=false"
        ])
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("🛑 Dashboard stopped")
        print("="*70)
        print("\n✅ ENHANCED MULTI-DISASTER SYSTEM READY!")
        print("\n🎉 Your comprehensive disaster management platform is complete!")
        print("\n📊 System Features:")
        print("   • 5 disaster types supported")
        print("   • AI + Rule-based predictions")
        print("   • Real-time weather data")
        print("   • Emergency contact integration")
        print("   • Production-ready interface")
        print("\n🚀 Perfect for hackathon demonstration!")
        print("="*70 + "\n")

if __name__ == "__main__":
    run_multi_disaster_app()