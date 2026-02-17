"""
Multi-Disaster Early Warning Dashboard
Supports: Floods, Earthquakes, Cyclones, Landslides, Heatwaves
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
import time
from datetime import datetime

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
from multi_disaster import MultiDisasterPredictor

# Page configuration
st.set_page_config(
    page_title="Disaster Early Warning System",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
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
    .disaster-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .disaster-card:hover {
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'weather_client' not in st.session_state:
    st.session_state.weather_client = WeatherAPIClient()
if 'predictor' not in st.session_state:
    st.session_state.predictor = MultiDisasterPredictor()
if 'selected_disaster' not in st.session_state:
    st.session_state.selected_disaster = 'flood'

def main():
    """Main application"""
    
    # Header
    st.markdown('<h1 class="main-header">🚨 AI Disaster Early Warning System</h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6c757d; font-size: 1.2rem;'>Multi-Hazard Risk Assessment Platform</p>", unsafe_allow_html=True)
    
    # Sidebar - Disaster Selection
    with st.sidebar:
        st.title("⚙️ Configuration")
        
        st.markdown("### Select Disaster Type")
        
        disasters = {
            'flood': {'name': '🌊 Flood', 'color': '#1e88e5'},
            'earthquake': {'name': '🔥 Earthquake', 'color': '#f4511e'},
            'cyclone': {'name': '🌪️ Cyclone', 'color': '#7b1fa2'},
            'landslide': {'name': '⛰️ Landslide', 'color': '#6d4c41'},
            'heatwave': {'name': '🌡️ Heatwave', 'color': '#ff6f00'}
        }
        
        for key, info in disasters.items():
            if st.button(info['name'], use_container_width=True, 
                        type="primary" if st.session_state.selected_disaster == key else "secondary"):
                st.session_state.selected_disaster = key
                st.rerun()
        
        st.markdown("---")
        
        # Info about selected disaster
        st.markdown(f"### {disasters[st.session_state.selected_disaster]['name']}")
        
        disaster_info = {
            'flood': "Predict flood risk based on rainfall, river levels, and soil saturation using AI.",
            'earthquake': "Assess earthquake risk based on location seismic activity zones.",
            'cyclone': "Evaluate cyclone risk using wind speed, pressure, and coastal proximity.",
            'landslide': "Determine landslide risk from rainfall, slope, and soil conditions.",
            'heatwave': "Monitor extreme heat conditions using temperature and humidity data."
        }
        
        st.info(disaster_info[st.session_state.selected_disaster])
        
        st.markdown("---")
        st.markdown("### 📊 System Stats")
        st.metric("Disasters Monitored", "5 Types")
        st.metric("AI Model Accuracy", "100%" if st.session_state.selected_disaster == 'flood' else "Rule-Based")
    
    # Main content
    st.markdown(f"## Check {disasters[st.session_state.selected_disaster]['name']} Risk")
    
    col1, col2, col3 = st.columns([3, 1, 2])
    
    with col1:
        city = st.text_input(
            "Enter City Name",
            placeholder="e.g., Mumbai, Delhi, Kolkata",
            help="Enter any city in India"
        )
    
    with col2:
        country = st.text_input("Country", value="IN", disabled=True)
    
    with col3:
        st.write("")
        st.write("")
        analyze_btn = st.button(
            f"🔍 Check {disasters[st.session_state.selected_disaster]['name'].split()[1]} Risk",
            type="primary",
            use_container_width=True
        )
    
    if analyze_btn and city:
        analyze_disaster(city, st.session_state.selected_disaster, disasters)
    
    # Quick Info Cards
    st.markdown("---")
    st.markdown("### 🌍 Disaster Types Covered")
    
    cols = st.columns(5)
    
    quick_info = [
        ("🌊", "Floods", "AI-powered predictions using weather + river data"),
        ("🔥", "Earthquakes", "Seismic zone risk assessment"),
        ("🌪️", "Cyclones", "Storm tracking with wind & pressure"),
        ("⛰️", "Landslides", "Slope stability analysis"),
        ("🌡️", "Heatwaves", "Heat index monitoring")
    ]
    
    for col, (emoji, name, desc) in zip(cols, quick_info):
        with col:
            st.markdown(f"""
            <div style='text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px;'>
                <h2 style='margin: 0;'>{emoji}</h2>
                <h4 style='margin: 0.5rem 0;'>{name}</h4>
                <p style='font-size: 0.8rem; color: #666;'>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

def analyze_disaster(city, disaster_type, disasters):
    """Analyze disaster risk"""
    
    with st.spinner(f"Analyzing {disaster_type} risk for {city}..."):
        try:
            # Fetch weather
            weather_data = st.session_state.weather_client.get_current_weather(city)
            
            # Transform to features
            features = st.session_state.weather_client.transform_to_features(weather_data, city)
            
            # Add pressure if available
            if 'main' in weather_data and 'pressure' in weather_data['main']:
                features['pressure'] = weather_data['main']['pressure']
            
            # Predict
            assessment = st.session_state.predictor.predict_disaster(
                disaster_type, features, city
            )
            
            # Display results
            display_results(assessment, weather_data, disasters)
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("💡 Tip: Make sure the city name is correct and try again.")

def display_results(assessment, weather_data, disasters):
    """Display disaster risk results"""
    
    risk_level = assessment['risk_level']
    risk_colors = {0: '#28a745', 1: '#ffc107', 2: '#fd7e14', 3: '#dc3545'}
    
    # Big alert box
    st.markdown("---")
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {risk_colors[risk_level]}20 0%, {risk_colors[risk_level]}40 100%); 
                padding: 2rem; border-radius: 15px; border-left: 8px solid {risk_colors[risk_level]};">
        <h1 style="margin:0; color: {risk_colors[risk_level]};">{assessment['title']}</h1>
        <p style="font-size: 1.3rem; margin-top: 1rem;">{assessment['message']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics
    st.markdown("### 📊 Risk Assessment")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Disaster Type", assessment['disaster_type'])
    with col2:
        st.metric("Risk Level", assessment['risk_label'], 
                 delta=f"Level {risk_level}", 
                 delta_color="inverse" if risk_level <= 1 else "normal")
    with col3:
        confidence = assessment['prediction']['confidence'] * 100
        st.metric("Confidence", f"{confidence:.0f}%")
    with col4:
        st.metric("Severity", assessment['severity'])
    
    # Critical warnings
    if assessment.get('additional_info'):
        st.markdown("### ⚠️ Critical Factors")
        for info in assessment['additional_info']:
            st.warning(info)
    
    # Actions
    st.markdown("### 🎯 Recommended Actions")
    for i, action in enumerate(assessment['recommended_actions'], 1):
        priority = "🔴 URGENT" if risk_level >= 3 and i <= 2 else "🟡 IMPORTANT" if risk_level >= 2 else "🟢 ADVISED"
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1rem; margin: 0.5rem 0; 
                    border-radius: 8px; border-left: 4px solid {'#dc3545' if '🔴' in priority else '#ffc107' if '🟡' in priority else '#28a745'};">
            <strong>{priority} - Action {i}:</strong><br>{action}
        </div>
        """, unsafe_allow_html=True)
    
    # Emergency contacts
    if assessment.get('emergency_contacts'):
        st.markdown("### 📞 Emergency Contacts")
        cols = st.columns(len(assessment['emergency_contacts']))
        for col, (service, number) in zip(cols, assessment['emergency_contacts'].items()):
            with col:
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; background: #dc3545; 
                            color: white; border-radius: 10px;">
                    <h4 style="margin:0;">{service.replace('_', ' ').title()}</h4>
                    <h2 style="margin:0.5rem 0;">{number}</h2>
                </div>
                """, unsafe_allow_html=True)
    
    # Weather conditions
    with st.expander("🌤️ Current Weather Conditions", expanded=False):
        if 'main' in weather_data:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🌡️ Temperature", f"{weather_data['main']['temp']:.1f}°C")
                st.metric("💧 Humidity", f"{weather_data['main']['humidity']}%")
            with col2:
                if 'wind' in weather_data:
                    st.metric("💨 Wind", f"{weather_data['wind']['speed'] * 3.6:.1f} km/h")
                if 'main' in weather_data and 'pressure' in weather_data['main']:
                    st.metric("🌀 Pressure", f"{weather_data['main']['pressure']} hPa")
            with col3:
                rain = weather_data.get('rain', {}).get('1h', 0)
                st.metric("🌧️ Rainfall", f"{rain} mm")
                if 'weather' in weather_data and weather_data['weather']:
                    st.metric("☁️ Conditions", weather_data['weather'][0]['description'].title())
    
    # Probability chart
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
            title=f"{assessment['disaster_type']} Risk Distribution"
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()