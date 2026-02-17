"""
Enhanced Flood Warning Dashboard with Automated User Flow
Complete end-to-end user journey implementation
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
import time
from datetime import datetime
import requests

# ── deployment-safe path bootstrap ──────────────────────────────────────────
_FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))
_SRC_DIR      = os.path.dirname(_FRONTEND_DIR)
_BACKEND_DIR  = os.path.join(_SRC_DIR, "backend")
_ML_DIR       = os.path.join(_SRC_DIR, "ml")
_UTILS_DIR    = os.path.join(_SRC_DIR, "utils")
for _p in (_BACKEND_DIR, _ML_DIR, _UTILS_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from weather_api import WeatherAPIClient
from flood_assessment import FloodRiskAssessor

# Page configuration
st.set_page_config(
    page_title="Flood Alert - Your Safety First",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: bold;
    }
    .tagline {
        text-align: center;
        color: #6c757d;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .step-indicator {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.5rem 0;
        font-weight: bold;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .alert-box {
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        margin: 1.5rem 0;
        animation: fadeIn 0.5s;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .action-item {
        background-color: #f8f9fa;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 4px solid #007bff;
    }
    .big-button {
        font-size: 1.5rem !important;
        padding: 1rem 2rem !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'weather_client' not in st.session_state:
    st.session_state.weather_client = WeatherAPIClient()
if 'assessor' not in st.session_state:
    st.session_state.assessor = FloodRiskAssessor()
if 'user_city' not in st.session_state:
    st.session_state.user_city = None
if 'assessment' not in st.session_state:
    st.session_state.assessment = None
if 'flow_complete' not in st.session_state:
    st.session_state.flow_complete = False

def get_location_from_ip():
    """Get approximate location from IP address"""
    try:
        response = requests.get('https://ipapi.co/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('city', None), data.get('country_name', None)
    except:
        pass
    return None, None

def main():
    """Main application with automated user flow"""
    
    # Header
    st.markdown('<h1 class="main-header">🚨 Flood Alert System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">Your Safety First - Real-Time Flood Risk Assessment</p>', unsafe_allow_html=True)
    
    # Check if flow is complete
    if not st.session_state.flow_complete:
        show_automated_flow()
    else:
        show_results()
    
    # Reset button at bottom
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Check Another Location", use_container_width=True):
            reset_flow()

def show_automated_flow():
    """Show automated user flow"""
    
    st.markdown("## 🚀 Welcome! Let's Check Your Flood Risk")
    st.info("💡 **How it works:** Enter your city → We fetch weather → AI predicts risk → Get safety alerts")
    
    # Step 1: Location Input
    st.markdown('<div class="step-indicator">📍 STEP 1: Your Location</div>', unsafe_allow_html=True)
    
    # Try to detect location
    if st.session_state.user_city is None:
        detected_city, detected_country = get_location_from_ip()
        if detected_city:
            st.success(f"✅ Detected your location: **{detected_city}, {detected_country}**")
            use_detected = st.checkbox("Use detected location", value=True)
            if use_detected:
                st.session_state.user_city = detected_city
    
    # Manual input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        city_input = st.text_input(
            "Enter your city name:",
            value=st.session_state.user_city if st.session_state.user_city else "",
            placeholder="e.g., Lucknow, Mumbai, Delhi",
            help="Enter the city you want to check"
        )
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        check_btn = st.button(
            "🔍 Check My Risk",
            type="primary",
            use_container_width=True,
            disabled=not city_input
        )
    
    if check_btn and city_input:
        run_automated_flow(city_input)

def run_automated_flow(city):
    """Run the complete automated flow"""
    
    st.markdown("---")
    st.markdown("## 🔄 Processing Your Request")
    
    progress_text = st.empty()
    progress_bar = st.progress(0)
    status_container = st.container()
    
    try:
        # Step 1: Location confirmed
        with status_container:
            st.markdown('<div class="step-indicator">📍 STEP 1: Location Confirmed</div>', unsafe_allow_html=True)
            st.success(f"✅ Checking flood risk for: **{city}**")
        progress_text.text("Step 1/4: Location confirmed...")
        progress_bar.progress(25)
        time.sleep(0.5)
        
        # Step 2: Fetch weather
        with status_container:
            st.markdown('<div class="step-indicator">🌤️ STEP 2: Fetching Weather Data</div>', unsafe_allow_html=True)
            with st.spinner("Connecting to weather services..."):
                weather_data = st.session_state.weather_client.get_current_weather(city)
                st.success("✅ Weather data retrieved!")
                
                # Show weather preview
                if 'main' in weather_data:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("🌡️ Temperature", f"{weather_data['main']['temp']:.1f}°C")
                    with col2:
                        st.metric("💧 Humidity", f"{weather_data['main']['humidity']}%")
                    with col3:
                        rain = weather_data.get('rain', {}).get('1h', 0)
                        st.metric("🌧️ Rainfall", f"{rain} mm")
        
        progress_text.text("Step 2/4: Weather data collected...")
        progress_bar.progress(50)
        time.sleep(0.5)
        
        # Step 3: AI Analysis
        with status_container:
            st.markdown('<div class="step-indicator">🤖 STEP 3: AI Risk Analysis</div>', unsafe_allow_html=True)
            with st.spinner("Running AI prediction model..."):
                features = st.session_state.weather_client.transform_to_features(weather_data, city)
                st.success("✅ Features extracted from weather data")
                
                assessment = st.session_state.assessor.assess_flood_risk(features, city)
                st.success(f"✅ AI Analysis complete: **{assessment['risk_label']}** risk detected")
        
        progress_text.text("Step 3/4: AI analysis complete...")
        progress_bar.progress(75)
        time.sleep(0.5)
        
        # Step 4: Generate Alert
        with status_container:
            st.markdown('<div class="step-indicator">📢 STEP 4: Generating Safety Alert</div>', unsafe_allow_html=True)
            with st.spinner("Preparing personalized safety recommendations..."):
                time.sleep(0.3)  # Brief pause for effect
                st.success("✅ Safety alert ready!")
        
        progress_text.text("Step 4/4: Alert generated!")
        progress_bar.progress(100)
        time.sleep(0.5)
        
        # Store results
        st.session_state.user_city = city
        st.session_state.assessment = assessment
        st.session_state.weather_data = weather_data
        st.session_state.features = features
        st.session_state.flow_complete = True
        
        # Success message
        st.balloons()
        st.success("🎉 **Analysis Complete!** Scroll down to see your personalized flood risk assessment.")
        
        # Rerun to show results
        time.sleep(1)
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("💡 Tip: Make sure the city name is spelled correctly and try again.")

def show_results():
    """Display complete results"""
    
    assessment = st.session_state.assessment
    city = st.session_state.user_city
    weather_data = st.session_state.weather_data
    
    risk_level = assessment['risk_level']
    risk_colors = {0: '#28a745', 1: '#ffc107', 2: '#fd7e14', 3: '#dc3545'}
    risk_emojis = {0: '✅', 1: '⚠️', 2: '🚨', 3: '🔴'}
    
    # Big alert box
    st.markdown("---")
    st.markdown(f"""
    <div class="alert-box" style="background: linear-gradient(135deg, {risk_colors[risk_level]}20 0%, {risk_colors[risk_level]}40 100%); border-left: 8px solid {risk_colors[risk_level]};">
        <h1 style="margin:0; color: {risk_colors[risk_level]};">{risk_emojis[risk_level]} {assessment['title']}</h1>
        <p style="font-size: 1.3rem; margin-top: 1rem; color: #333;">{assessment['message']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    st.markdown("### 📊 Risk Assessment Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📍 Location", city)
    with col2:
        st.metric("🎯 Risk Level", assessment['risk_label'], 
                 delta=f"Level {risk_level}", 
                 delta_color="inverse" if risk_level <= 1 else "normal")
    with col3:
        confidence = assessment['prediction']['confidence'] * 100
        st.metric("✅ Confidence", f"{confidence:.0f}%")
    with col4:
        st.metric("⚠️ Severity", assessment['severity'])
    
    # Critical warnings (if any)
    if assessment.get('additional_info'):
        st.markdown("### ⚠️ Critical Conditions Detected")
        for info in assessment['additional_info']:
            st.warning(info)
    
    # Safety Actions - Prioritized
    st.markdown("### 🎯 What You Should Do RIGHT NOW")
    st.info("👇 **Follow these steps in order for your safety:**")
    
    for i, action in enumerate(assessment['recommended_actions'], 1):
        priority = "🔴 URGENT" if risk_level >= 3 and i <= 3 else "🟡 IMPORTANT" if risk_level >= 2 else "🟢 ADVISED"
        st.markdown(f"""
        <div class="action-item">
            <strong>{priority} - Action {i}:</strong><br>
            {action}
        </div>
        """, unsafe_allow_html=True)
    
    # Emergency contacts
    if assessment.get('emergency_contacts'):
        st.markdown("### 📞 Emergency Contacts")
        st.error("⚠️ **Call immediately if you're in danger!**")
        
        cols = st.columns(len(assessment['emergency_contacts']))
        for col, (service, number) in zip(cols, assessment['emergency_contacts'].items()):
            with col:
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; background-color: #dc3545; color: white; border-radius: 10px;">
                    <h3 style="margin:0;">{service.replace('_', ' ').title()}</h3>
                    <h2 style="margin:0.5rem 0;">{number}</h2>
                </div>
                """, unsafe_allow_html=True)
    
    # Current conditions
    with st.expander("🌤️ Current Weather Conditions", expanded=False):
        if 'main' in weather_data:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("🌡️ Temperature", f"{weather_data['main']['temp']:.1f}°C")
                st.metric("💧 Humidity", f"{weather_data['main']['humidity']}%")
            
            with col2:
                if 'wind' in weather_data:
                    wind_kmh = weather_data['wind']['speed'] * 3.6
                    st.metric("💨 Wind Speed", f"{wind_kmh:.1f} km/h")
                
                rain = weather_data.get('rain', {}).get('1h', 0)
                st.metric("🌧️ Rainfall (1h)", f"{rain} mm")
            
            with col3:
                if 'weather' in weather_data and len(weather_data['weather']) > 0:
                    desc = weather_data['weather'][0]['description'].title()
                    st.metric("☁️ Sky Conditions", desc)
    
    # Probability breakdown
    with st.expander("📊 AI Prediction Analysis", expanded=False):
        probs = assessment['prediction']['all_probabilities']
        prob_df = pd.DataFrame({
            'Risk Level': ['Safe', 'Warning', 'High Risk', 'Critical'],
            'Probability (%)': [
                probs['safe'] * 100,
                probs['warning'] * 100,
                probs['high_risk'] * 100,
                probs['critical'] * 100
            ]
        })
        
        fig = px.bar(
            prob_df,
            x='Risk Level',
            y='Probability (%)',
            color='Risk Level',
            color_discrete_map={
                'Safe': '#28a745',
                'Warning': '#ffc107',
                'High Risk': '#fd7e14',
                'Critical': '#dc3545'
            },
            title="AI Model Confidence Distribution"
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info(f"ℹ️ The AI model is **{confidence:.0f}% confident** in this prediction based on current weather conditions and historical flood data.")
    
    # Timestamp
    st.markdown("---")
    st.caption(f"🕐 Assessment generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Stay safe! 💙")

def reset_flow():
    """Reset the flow to check another location"""
    st.session_state.flow_complete = False
    st.session_state.user_city = None
    st.session_state.assessment = None
    st.rerun()

if __name__ == "__main__":
    main()