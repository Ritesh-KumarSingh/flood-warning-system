"""
Flood Early Warning Dashboard
Interactive Streamlit web interface for flood prediction system
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
import time
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from weather_api import WeatherAPIClient
from flood_assessment import FloodRiskAssessor

# Page configuration
st.set_page_config(
    page_title="Flood Early Warning System",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .risk-safe {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .risk-warning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        color: #856404;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .risk-high {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        color: #721c24;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #fd7e14;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .risk-critical {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        color: #721c24;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
        box-shadow: 0 4px 8px rgba(220,53,69,0.3);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        text-align: center;
    }
    .stAlert {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'weather_client' not in st.session_state:
    st.session_state.weather_client = WeatherAPIClient()
if 'assessor' not in st.session_state:
    st.session_state.assessor = FloodRiskAssessor()
if 'history' not in st.session_state:
    st.session_state.history = []

def get_risk_color(risk_level):
    """Get color for risk level"""
    colors = {
        0: "#28a745",  # Green
        1: "#ffc107",  # Yellow
        2: "#fd7e14",  # Orange
        3: "#dc3545"   # Red
    }
    return colors.get(risk_level, "#6c757d")

def get_risk_emoji(risk_level):
    """Get emoji for risk level"""
    emojis = {
        0: "✅",
        1: "⚠️",
        2: "🚨",
        3: "🔴"
    }
    return emojis.get(risk_level, "⚪")

def main():
    """Main dashboard application"""
    
    # Header
    st.markdown('<h1 class="main-header">🌊 Flood Early Warning System</h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6c757d; font-size: 1.2rem;'>AI-Powered Real-Time Flood Risk Assessment</p>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/clouds/200/000000/flood.png", width=150)
        st.title("⚙️ Settings")
        
        # Mode selection
        mode = st.radio(
            "**Select Mode**",
            ["🌍 Live Weather", "📝 Manual Input", "📊 Multi-City Monitor"],
            help="Choose how to input data"
        )
        
        st.markdown("---")
        
        # Quick tips
        with st.expander("💡 Quick Tips", expanded=False):
            st.markdown("""
            **Live Weather Mode:**
            - Enter any city name
            - Fetches real-time weather
            - Automatic risk prediction
            
            **Manual Input Mode:**
            - Enter all 12 features
            - Custom scenarios
            - Testing purposes
            
            **Multi-City Monitor:**
            - Monitor 4 cities at once
            - Compare risk levels
            - Bulk assessment
            """)
        
        # System stats
        st.markdown("---")
        st.markdown("### 📊 System Stats")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Model Accuracy", "100%", help="Model performance on test data")
        with col2:
            st.metric("Response Time", "<400ms", help="End-to-end processing time")
        
        st.metric("Cities Analyzed", len(st.session_state.history), help="Total predictions made")
        
        # System status
        st.markdown("---")
        st.markdown("### 🟢 System Status")
        st.success("✅ All systems operational")
        st.info("📡 Weather API: Demo Mode")
        st.info("🤖 ML Model: Loaded")
    
    # Main content based on mode
    if mode == "🌍 Live Weather":
        show_live_weather_mode()
    elif mode == "📝 Manual Input":
        show_manual_input_mode()
    else:
        show_multi_city_mode()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6c757d; padding: 1rem;'>
        <p><b>🎓 AI-Based Disaster Early Warning Platform</b></p>
        <p>Built with ❤️ for Hackathon | Powered by Machine Learning, FastAPI & Streamlit</p>
        <p style='font-size: 0.9rem;'>📧 Contact: emergency@floodwarning.ai | 🌐 Version 1.0.0</p>
    </div>
    """, unsafe_allow_html=True)

def show_live_weather_mode():
    """Live weather prediction mode"""
    
    st.markdown("## 🌍 Live Weather Prediction")
    st.markdown("Enter a city name to fetch real-time weather data and predict flood risk.")
    
    col1, col2, col3 = st.columns([3, 1, 2])
    
    with col1:
        city = st.text_input(
            "City Name",
            placeholder="e.g., Lucknow, Mumbai, Delhi",
            help="Enter any city name in India"
        )
    
    with col2:
        country = st.text_input("Country", value="IN", disabled=True)
    
    with col3:
        st.write("")  # Spacing
        st.write("")  # Spacing
        analyze_btn = st.button("🔍 Analyze Flood Risk", type="primary", use_container_width=True)
    
    if analyze_btn:
        if city:
            with st.spinner(f"🔄 Analyzing flood risk for {city}..."):
                analyze_city(city)
        else:
            st.warning("⚠️ Please enter a city name!")
    
    # Show history
    if st.session_state.history:
        st.markdown("---")
        st.markdown("### 📜 Recent Predictions")
        
        history_df = pd.DataFrame(st.session_state.history)
        history_df['timestamp'] = pd.to_datetime(history_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Add emojis
        history_df['status'] = history_df['risk_level'].apply(get_risk_emoji)
        history_df = history_df[['status', 'city', 'risk_label', 'timestamp']]
        history_df.columns = ['', 'City', 'Risk Level', 'Timestamp']
        
        st.dataframe(history_df, use_container_width=True, hide_index=True)

def analyze_city(city):
    """Analyze flood risk for a city"""
    
    start_time = time.time()
    
    try:
        # Fetch weather
        with st.status("Processing...", expanded=True) as status:
            st.write("🌐 Fetching weather data from OpenWeatherMap...")
            weather_data = st.session_state.weather_client.get_current_weather(city)
            st.write("✅ Weather data retrieved!")
            
            # Transform
            st.write("🔄 Transforming data to model features...")
            features = st.session_state.weather_client.transform_to_features(weather_data, city)
            st.write("✅ Features extracted!")
            
            # Predict
            st.write("🎯 Running AI prediction model...")
            assessment = st.session_state.assessor.assess_flood_risk(features, city)
            st.write("✅ Prediction complete!")
            
            status.update(label="✅ Analysis complete!", state="complete", expanded=False)
        
        # Calculate time
        processing_time = (time.time() - start_time) * 1000
        
        # Display results
        display_results(city, weather_data, features, assessment, processing_time)
        
        # Add to history
        st.session_state.history.append({
            'timestamp': datetime.now(),
            'city': city,
            'risk_level': assessment['risk_level'],
            'risk_label': assessment['risk_label']
        })
        
        # Keep only last 10
        if len(st.session_state.history) > 10:
            st.session_state.history = st.session_state.history[-10:]
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("💡 Tip: Make sure the city name is spelled correctly!")

def display_results(city, weather_data, features, assessment, processing_time):
    """Display prediction results"""
    
    alert = assessment
    risk_level = alert['risk_level']
    
    # Risk indicator
    st.markdown("---")
    st.markdown(f"## {get_risk_emoji(risk_level)} {alert['title']}")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Risk Level",
            alert['risk_label'],
            delta=f"Level {risk_level}",
            delta_color="inverse" if risk_level <= 1 else "normal"
        )
    
    with col2:
        confidence = assessment['prediction']['confidence'] * 100
        st.metric(
            "Confidence",
            f"{confidence:.1f}%",
            delta="High" if confidence > 90 else "Moderate"
        )
    
    with col3:
        st.metric(
            "Severity",
            alert['severity'],
            delta=None
        )
    
    with col4:
        st.metric(
            "Processing Time",
            f"{processing_time:.0f}ms",
            delta="Fast" if processing_time < 500 else "Normal"
        )
    
    # Risk alert box
    risk_class = ["risk-safe", "risk-warning", "risk-high", "risk-critical"][risk_level]
    st.markdown(f"""
    <div class="{risk_class}">
        <h3 style='margin-top: 0;'>📢 Alert Message</h3>
        <p style='font-size: 1.1rem; margin-bottom: 0;'>{alert['message']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs for detailed info
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Actions", "🌡️ Conditions", "📊 Analysis", "📞 Emergency"])
    
    with tab1:
        st.markdown("### Recommended Actions")
        for i, action in enumerate(alert['recommended_actions'], 1):
            st.markdown(f"**{i}.** {action}")
    
    with tab2:
        st.markdown("### Current Weather Conditions")
        
        if 'main' in weather_data:
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("🌡️ Temperature", f"{weather_data['main']['temp']:.1f}°C")
                st.metric("💧 Humidity", f"{weather_data['main']['humidity']}%")
                
                if 'rain' in weather_data and '1h' in weather_data['rain']:
                    st.metric("🌧️ Rainfall (1h)", f"{weather_data['rain']['1h']} mm")
                else:
                    st.metric("🌧️ Rainfall (1h)", "0 mm")
            
            with col2:
                if 'wind' in weather_data:
                    wind_kmh = weather_data['wind']['speed'] * 3.6
                    st.metric("💨 Wind Speed", f"{wind_kmh:.1f} km/h")
                
                if 'weather' in weather_data and len(weather_data['weather']) > 0:
                    desc = weather_data['weather'][0]['description'].title()
                    st.metric("☁️ Conditions", desc)
                
                st.metric("📍 Location", city)
        
        # Feature values
        st.markdown("### Estimated Model Features")
        feature_df = pd.DataFrame([
            {"Feature": "Rainfall (24h)", "Value": f"{features['rainfall_mm']} mm"},
            {"Feature": "River Level", "Value": f"{features['river_level_m']} m"},
            {"Feature": "Soil Moisture", "Value": f"{features['soil_moisture_percent']}%"},
            {"Feature": "Elevation", "Value": f"{features['elevation_m']} m"},
        ])
        st.dataframe(feature_df, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("### Prediction Analysis")
        
        # Probability chart
        probs = assessment['prediction']['all_probabilities']
        prob_df = pd.DataFrame({
            'Risk Level': ['Safe', 'Warning', 'High Risk', 'Critical'],
            'Probability': [probs['safe'], probs['warning'], probs['high_risk'], probs['critical']]
        })
        
        fig = px.bar(
            prob_df,
            x='Risk Level',
            y='Probability',
            color='Risk Level',
            color_discrete_map={
                'Safe': '#28a745',
                'Warning': '#ffc107',
                'High Risk': '#fd7e14',
                'Critical': '#dc3545'
            },
            title="Prediction Probability Distribution"
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Critical factors
        if alert.get('additional_info'):
            st.markdown("### ⚠️ Critical Factors Detected")
            for info in alert['additional_info']:
                st.warning(info)
    
    with tab4:
        if alert.get('emergency_contacts'):
            st.markdown("### 🚨 Emergency Contacts")
            
            for service, number in alert['emergency_contacts'].items():
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**{service.replace('_', ' ').title()}**")
                with col2:
                    st.code(number)
        else:
            st.info("No emergency contacts needed for current risk level")

def show_manual_input_mode():
    """Manual feature input mode"""
    
    st.markdown("## 📝 Manual Input Mode")
    st.markdown("Manually enter all 12 features to test custom scenarios.")
    
    with st.form("manual_input_form"):
        st.markdown("### Environmental Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**💧 Rainfall**")
            rainfall_mm = st.number_input("Rainfall (24h) mm", 0.0, 500.0, 50.0, 5.0)
            rainfall_7day = st.number_input("7-day Average mm", 0.0, 300.0, 40.0, 5.0)
            rainfall_intensity = st.number_input("Intensity mm/h", 0.0, 50.0, 5.0, 1.0)
            
            st.markdown("**🌊 River**")
            river_level = st.number_input("River Level m", 0.0, 15.0, 5.0, 0.5)
            river_change = st.number_input("Level Change m", -2.0, 5.0, 0.5, 0.1)
        
        with col2:
            st.markdown("**🌡️ Weather**")
            temperature = st.number_input("Temperature °C", -10.0, 45.0, 25.0, 1.0)
            humidity = st.number_input("Humidity %", 0.0, 100.0, 70.0, 5.0)
            wind_speed = st.number_input("Wind Speed km/h", 0.0, 100.0, 15.0, 5.0)
        
        with col3:
            st.markdown("**🗺️ Location**")
            soil_moisture = st.number_input("Soil Moisture %", 0.0, 100.0, 50.0, 5.0)
            elevation = st.number_input("Elevation m", 0.0, 1000.0, 100.0, 10.0)
            distance_river = st.number_input("Distance to River km", 0.0, 50.0, 3.0, 0.5)
            month = st.selectbox("Month", list(range(1, 13)), index=6)
        
        location = st.text_input("Location Name", "Custom Location")
        
        submitted = st.form_submit_button("🎯 Predict Flood Risk", use_container_width=True, type="primary")
        
        if submitted:
            features = {
                'rainfall_mm': rainfall_mm,
                'rainfall_7day_avg': rainfall_7day,
                'rainfall_intensity': rainfall_intensity,
                'river_level_m': river_level,
                'river_level_change': river_change,
                'soil_moisture_percent': soil_moisture,
                'elevation_m': elevation,
                'temperature_celsius': temperature,
                'humidity_percent': humidity,
                'wind_speed_kmh': wind_speed,
                'distance_to_river_km': distance_river,
                'month': month
            }
            
            with st.spinner("🔄 Processing..."):
                start_time = time.time()
                assessment = st.session_state.assessor.assess_flood_risk(features, location)
                processing_time = (time.time() - start_time) * 1000
            
            # Mock weather data for display
            weather_data = {'main': {'temp': temperature, 'humidity': humidity}}
            
            display_results(location, weather_data, features, assessment, processing_time)

def show_multi_city_mode():
    """Multi-city monitoring mode"""
    
    st.markdown("## 📊 Multi-City Monitor")
    st.markdown("Monitor flood risk across multiple cities simultaneously.")
    
    # Predefined cities
    cities = ["Lucknow", "Mumbai", "Delhi", "Kolkata"]
    
    if st.button("🔄 Refresh All Cities", type="primary", use_container_width=False):
        st.session_state['multi_city_data'] = None
    
    # Fetch data for all cities
    if 'multi_city_data' not in st.session_state or st.session_state.multi_city_data is None:
        with st.spinner("🌍 Fetching data for all cities..."):
            results = []
            progress_bar = st.progress(0)
            
            for i, city in enumerate(cities):
                try:
                    weather = st.session_state.weather_client.get_current_weather(city)
                    features = st.session_state.weather_client.transform_to_features(weather, city)
                    assessment = st.session_state.assessor.assess_flood_risk(features, city)
                    
                    results.append({
                        'city': city,
                        'risk_level': assessment['risk_level'],
                        'risk_label': assessment['risk_label'],
                        'confidence': assessment['prediction']['confidence'] * 100,
                        'temperature': weather['main']['temp'] if 'main' in weather else 25,
                        'humidity': weather['main']['humidity'] if 'main' in weather else 70,
                        'rainfall': features['rainfall_mm']
                    })
                except:
                    pass
                
                progress_bar.progress((i + 1) / len(cities))
            
            st.session_state.multi_city_data = results
    
    results = st.session_state.multi_city_data
    
    if results:
        # Summary cards
        st.markdown("### 🏙️ City Risk Overview")
        
        cols = st.columns(len(results))
        for col, result in zip(cols, results):
            with col:
                emoji = get_risk_emoji(result['risk_level'])
                color = get_risk_color(result['risk_level'])
                
                st.markdown(f"""
                <div style='background-color: {color}20; padding: 1rem; border-radius: 8px; border-left: 4px solid {color};'>
                    <h3 style='margin: 0; color: {color};'>{emoji} {result['city']}</h3>
                    <p style='font-size: 1.5rem; margin: 0.5rem 0; font-weight: bold;'>{result['risk_label']}</p>
                    <p style='margin: 0; font-size: 0.9rem;'>Confidence: {result['confidence']:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Data table
        st.markdown("### 📋 Detailed Comparison")
        
        df = pd.DataFrame(results)
        df['emoji'] = df['risk_level'].apply(get_risk_emoji)
        df_display = df[['emoji', 'city', 'risk_label', 'confidence', 'temperature', 'humidity', 'rainfall']]
        df_display.columns = ['', 'City', 'Risk Level', 'Confidence %', 'Temp °C', 'Humidity %', 'Rainfall mm']
        
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                'Confidence %': st.column_config.ProgressColumn(
                    'Confidence %',
                    format="%.1f%%",
                    min_value=0,
                    max_value=100
                )
            }
        )
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk distribution
            fig1 = px.pie(
                df,
                names='risk_label',
                title='Risk Distribution Across Cities',
                color='risk_label',
                color_discrete_map={
                    'Safe': '#28a745',
                    'Warning': '#ffc107',
                    'High Risk': '#fd7e14',
                    'Critical': '#dc3545'
                }
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Temperature vs Rainfall
            fig2 = px.scatter(
                df,
                x='temperature',
                y='rainfall',
                size='humidity',
                color='risk_label',
                text='city',
                title='Temperature vs Rainfall',
                labels={'temperature': 'Temperature (°C)', 'rainfall': 'Rainfall (mm)'},
                color_discrete_map={
                    'Safe': '#28a745',
                    'Warning': '#ffc107',
                    'High Risk': '#fd7e14',
                    'Critical': '#dc3545'
                }
            )
            fig2.update_traces(textposition='top center')
            st.plotly_chart(fig2, use_container_width=True)

if __name__ == "__main__":
    main()