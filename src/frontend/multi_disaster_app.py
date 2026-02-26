"""
ENHANCED Multi-Disaster Early Warning Dashboard
Now includes:
- Emergency Resources Locator
- Hindi Language Support
- Historical Disaster Data
- Community Reporting System
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
import time
from datetime import datetime
import json


# ── deployment-safe path bootstrap ──────────────────────────────────────────
_FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))
_SRC_DIR      = os.path.dirname(_FRONTEND_DIR)
_BACKEND_DIR  = os.path.join(_SRC_DIR, "backend")
_ML_DIR       = os.path.join(_SRC_DIR, "ml")
_UTILS_DIR    = os.path.join(_SRC_DIR, "utils")
for _p in (_BACKEND_DIR, _ML_DIR, _UTILS_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Core imports
from awareness_games import DisasterGames
from disaster_chatbot import DisasterChatbot
from family_safety import FamilySafetyTracker
from weather_api import WeatherAPIClient
from multi_disaster import MultiDisasterMLPredictor as MultiDisasterPredictor

# Feature imports
from emergency_resources import EmergencyResourceLocator
from language_support import LanguageTranslator
from historical_data import HistoricalDataAnalyzer
from community_reporting import CommunityReporter
from disaster_map import DisasterMap

# Auth & DB
import auth
import database as db

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


# ─── Initialize session state ────────────────────────────────────────────────
def _init_session_state():
    """Initialize all session state variables. Must be called on every run."""
    if 'weather_client' not in st.session_state:
        st.session_state.weather_client = WeatherAPIClient()
    if 'predictor' not in st.session_state:
        st.session_state.predictor = MultiDisasterPredictor()
    if 'selected_disaster' not in st.session_state:
        st.session_state.selected_disaster = 'flood'

    # Feature modules
    if 'resource_locator' not in st.session_state:
        st.session_state.resource_locator = EmergencyResourceLocator()
    if 'translator' not in st.session_state:
        st.session_state.translator = LanguageTranslator()
    if 'historical' not in st.session_state:
        st.session_state.historical = HistoricalDataAnalyzer()
    if 'reporter' not in st.session_state:
        st.session_state.reporter = CommunityReporter()
    if 'language' not in st.session_state:
        st.session_state.language = 'en'


# ─── Login / Register page ──────────────────────────────────────────────────
def show_login_page():
    """Show a styled login / register UI."""
    st.markdown("""
    <style>
        .auth-container {
            max-width: 440px;
            margin: 2rem auto;
            padding: 2.5rem 2rem;
            background: linear-gradient(135deg, #1e3a5f 0%, #0d2137 100%);
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.35);
        }
        .auth-title {
            text-align: center;
            font-size: 2rem;
            color: #e2e8f0;
            margin-bottom: 0.2rem;
        }
        .auth-subtitle {
            text-align: center;
            color: #94a3b8;
            font-size: 0.95rem;
            margin-bottom: 1.5rem;
        }
    </style>
    <div class="auth-container">
        <div class="auth-title">🚨 Disaster Warning</div>
        <div class="auth-subtitle">Sign in to access the early-warning dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    login_tab, register_tab = st.tabs(["🔑 Login", "📝 Register"])

    # ── Login tab ──
    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("Login", use_container_width=True, type="primary")

            if submit:
                if not username or not password:
                    st.error("Please fill in all fields.")
                else:
                    ok, msg, user = auth.login(username, password)
                    if ok:
                        st.session_state.user = user
                        st.success(msg)
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(msg)

    # ── Register tab ──
    with register_tab:
        with st.form("register_form"):
            new_name = st.text_input("Full Name", placeholder="Your full name")
            new_user = st.text_input("Username", placeholder="Choose a username (min 3 chars)")
            new_email = st.text_input("Email", placeholder="you@example.com")
            new_pass = st.text_input("Password", type="password", placeholder="Min 6 characters")
            new_pass2 = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
            register = st.form_submit_button("Create Account", use_container_width=True, type="primary")

            if register:
                if new_pass != new_pass2:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = auth.register(new_user, new_email, new_pass, new_name)
                    if ok:
                        st.success(msg + " Please switch to the **Login** tab.")
                    else:
                        st.error(msg)


def main():
    """Main application"""

    # Initialize session state on every run (critical for Streamlit Cloud)
    _init_session_state()

    # ── Auth gate ──
    if not auth.is_logged_in(st.session_state):
        show_login_page()
        return

    current_user = auth.get_current_user(st.session_state)

    # Get translator
    translator = st.session_state.translator
    lang = st.session_state.language
    
    # Sidebar - User info + Disaster Selection + Language
    with st.sidebar:
        # User greeting & logout
        st.markdown(f"### 👤 {current_user['username']}")
        if st.button("🚪 Logout", use_container_width=True):
            auth.logout(st.session_state)
            st.rerun()

        st.markdown("---")
        st.title("⚙️ Configuration")
        
        # Language Selector
        st.markdown("### 🌐 Language / भाषा")
        languages = translator.get_available_languages()
        selected_lang = st.radio(
            "",
            options=list(languages.keys()),
            format_func=lambda x: languages[x],
            horizontal=True,
            key='lang_selector'
        )
        
        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            st.rerun()
        
        st.markdown("---")
        
        # Disaster Type Selection
        st.markdown(f"### {translator.get_text('select_disaster', lang)}")
        
        disasters = {
            'flood': {'name': f"🌊 {translator.get_text('flood', lang)}", 'color': '#1e88e5'},
            'earthquake': {'name': f"🔥 {translator.get_text('earthquake', lang)}", 'color': '#f4511e'},
            'cyclone': {'name': f"🌪️ {translator.get_text('cyclone', lang)}", 'color': '#7b1fa2'},
            'landslide': {'name': f"⛰️ {translator.get_text('landslide', lang)}", 'color': '#6d4c41'},
            'heatwave': {'name': f"🌡️ {translator.get_text('heatwave', lang)}", 'color': '#ff6f00'}
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
        st.metric("Languages Supported", "2 (EN/HI)")
    
    # Main header (translated)
    st.markdown(f'<h1 class="main-header">{translator.get_text("app_title", lang)}</h1>', 
                unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #6c757d; font-size: 1.2rem;'>{translator.get_text('risk_assessment', lang)}</p>", 
                unsafe_allow_html=True)
    
    # Create main tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "🔍 Risk Assessment",
    "📊 Historical Data",
    "📝 Community Reports",
    "🏥 Emergency Contacts",
    "👨‍👩‍👧‍👦 Family Safety",    
    "🤖 AI Assistant",          
    "🎮 Games & Quizzes",       
    "🗺️ Disaster Map",
    "📜 My Risk History",
    "👤 My Profile"
    ])
    
    # TAB 1: Risk Assessment
    with tab1:
        st.markdown(f"## {translator.get_text('check_risk', lang)} - {disasters[st.session_state.selected_disaster]['name']}")
        
        col1, col2, col3 = st.columns([3, 1, 2])
        
        with col1:
            city = st.text_input(
                translator.get_text('enter_city', lang),
                placeholder="e.g., Mumbai, Delhi, Kolkata",
                help="Enter any city in India"
            )
        
        with col2:
            country = st.text_input("Country", value="IN", disabled=True)
        
        with col3:
            st.write("")
            st.write("")
            analyze_btn = st.button(
                f"🔍 {translator.get_text('check_risk', lang)}",
                type="primary",
                use_container_width=True
            )
        
        if analyze_btn and city:
            analyze_disaster(city, st.session_state.selected_disaster, disasters, translator, lang)
    
    # TAB 2: Historical Data
    with tab2:
        st.markdown("## 📊 Historical Disaster Analysis")
        
        if 'city' in locals() and city:
            st.session_state.historical.display_history(
                city=city,
                disaster_type=st.session_state.selected_disaster
            )
        else:
            st.info("💡 Enter a city in the Risk Assessment tab first")

        # Show user's own risk history alongside city data
        st.markdown("---")
        st.markdown("### 📜 Your Risk History vs City Trends")
        user_history = db.get_risk_history(current_user['id'], limit=50)
        if user_history:
            hist_df = pd.DataFrame(user_history)
            hist_df['checked_at'] = pd.to_datetime(hist_df['checked_at'])
            hist_df['date'] = hist_df['checked_at'].dt.date

            # Chart: user assessments over time
            chart_df = hist_df.groupby(['date', 'risk_label']).size().reset_index(name='count')
            if not chart_df.empty:
                fig = px.bar(
                    chart_df, x='date', y='count', color='risk_label',
                    color_discrete_map={'Safe': '#28a745', 'Warning': '#ffc107',
                                        'High Risk': '#fd7e14', 'Critical': '#dc3545'},
                    title='Your Risk Checks Over Time',
                    labels={'date': 'Date', 'count': 'Checks', 'risk_label': 'Risk Level'}
                )
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No risk history yet — run assessments to see trends here.")
    
    # TAB 3: Community Reports
    with tab3:
        st.markdown("## 📝 Community Disaster Reporting")
        
        col_report1, col_report2 = st.columns([1, 1])
        
        with col_report1:
            st.markdown("### Submit Report")
            st.session_state.reporter.display_report_form()
        
        with col_report2:
            st.markdown("### Live Community Feed")
            location_filter = city if 'city' in locals() and city else None
            st.session_state.reporter.display_community_feed(location=location_filter)
    
    # TAB 4: Emergency Resources
    with tab4:
        st.markdown(f"## 🏥 {translator.get_text('emergency_contacts', lang)}")
        
        resource_city = st.text_input(
            "Enter city to find resources",
            value=city if 'city' in locals() and city else "",
            key='resource_city'
        )
        
        if resource_city:
            st.session_state.resource_locator.display_resources(
                location=resource_city,
                risk_level=2  # Show all resources
            )
        else:
            st.info("Enter a city name to see emergency resources")
            
    if 'family_tracker' not in st.session_state:
        st.session_state.family_tracker = FamilySafetyTracker()
        st.session_state.chatbot = DisasterChatbot()
        st.session_state.games = DisasterGames()
        st.session_state.disaster_map = DisasterMap()
    
    # Tab 5: Family Safety
    with tab5:
        st.session_state.family_tracker.display_safety_interface()

    # Tab 6: AI Chatbot
    with tab6:
        st.session_state.chatbot.display_chatbot(
            disaster_type=st.session_state.selected_disaster,
            language=st.session_state.language
        )

    # Tab 7: Games
    with tab7:
        game_type = st.radio("Choose Game", ["Quiz", "Scenario", "Memory"])
        if game_type == "Quiz":
            st.session_state.games.display_quiz_game(st.session_state.selected_disaster)
        elif game_type == "Scenario":
            st.session_state.games.display_scenario_challenge()
        else:
            st.session_state.games.display_memory_game()

    # Tab 8: Map
    with tab8:
        if 'city' in locals() and city:
            st.session_state.disaster_map.display_disaster_map(city)
            st.markdown("---")
            st.session_state.disaster_map.display_shelter_list(city)
        else:
            st.info("Enter a city in Risk Assessment tab first")
    
    # Quick Info Cards (at bottom)
    st.markdown("---")
    st.markdown("### 🌍 Disaster Types Covered")
    
    cols = st.columns(5)
    
    quick_info = [
        ("🌊", translator.get_text('flood', lang), "AI-powered predictions"),
        ("🔥", translator.get_text('earthquake', lang), "Seismic zone assessment"),
        ("🌪️", translator.get_text('cyclone', lang), "Storm tracking"),
        ("⛰️", translator.get_text('landslide', lang), "Slope stability"),
        ("🌡️", translator.get_text('heatwave', lang), "Heat index monitoring")
    ]
    
    for col, (emoji, name, desc) in zip(cols, quick_info):
        with col:
            st.markdown(f"""
            <div style='text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px; color: #333;'>
                <h2 style='margin: 0;'>{emoji}</h2>
                <h4 style='margin: 0.5rem 0; color: #333;'>{name}</h4>
                <p style='font-size: 0.8rem; color: #555;'>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # ─── Tab 9: Risk History ────────────────────────────────────────────
    with tab9:
        st.markdown("### 📜 Your Recent Risk Checks")
        history = db.get_risk_history(current_user['id'], limit=20)
        if not history:
            st.info("No risk checks yet. Go to the **Risk Assessment** tab to start.")
        else:
            df = pd.DataFrame(history)
            df = df[['checked_at', 'city', 'disaster_type', 'risk_label', 'confidence', 'weather_summary']]
            df.columns = ['Time', 'City', 'Disaster', 'Risk', 'Confidence', 'Weather']
            df['Confidence'] = (df['Confidence'] * 100).round(0).astype(int).astype(str) + '%'
            st.dataframe(df, use_container_width=True, hide_index=True)

    # ─── Tab 10: User Profile ────────────────────────────────────────────
    with tab10:
        st.markdown("### 👤 My Profile")
        profile = db.get_profile(current_user['id']) or {}

        with st.form("profile_form"):
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                phone = st.text_input("📱 Phone", value=profile.get('phone', ''), placeholder='+91 9876543210')
                blood_group = st.selectbox("🩸 Blood Group",
                    ['', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
                    index=['', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'].index(profile.get('blood_group', '')))
                medical = st.text_area("🏥 Medical Conditions", value=profile.get('medical_conditions', ''),
                    placeholder='Allergies, chronic conditions, medications...')
            with col_p2:
                address = st.text_area("🏠 Address", value=profile.get('address', ''),
                    placeholder='Your home address for emergency services')
                ec_name = st.text_input("🆘 Emergency Contact Name", value=profile.get('emergency_contact_name', ''))
                ec_phone = st.text_input("📞 Emergency Contact Phone", value=profile.get('emergency_contact_phone', ''))

            default_city = st.text_input("🌆 Default City (for quick risk checks)",
                value=profile.get('default_city', ''), placeholder='e.g., Mumbai')

            st.markdown("#### 👨‍👩‍👧‍👦 Family Members")
            family_raw = profile.get('family_members', '[]')
            try:
                family_list = json.loads(family_raw) if family_raw else []
            except (json.JSONDecodeError, TypeError):
                family_list = []

            family_text = st.text_area(
                "Enter family members (one per line: Name, Age, Relation)",
                value='\n'.join([f"{m.get('name','')}, {m.get('age','')}, {m.get('relation','')}" for m in family_list]),
                placeholder='Priya, 35, Spouse\nRahul, 8, Son',
                height=100
            )

            save_profile_btn = st.form_submit_button("💾 Save Profile", type="primary", use_container_width=True)

            if save_profile_btn:
                # Parse family members
                parsed_family = []
                for line in family_text.strip().split('\n'):
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) >= 2:
                        parsed_family.append({
                            'name': parts[0],
                            'age': parts[1] if len(parts) > 1 else '',
                            'relation': parts[2] if len(parts) > 2 else ''
                        })

                db.save_profile(current_user['id'], {
                    'phone': phone,
                    'blood_group': blood_group,
                    'medical_conditions': medical,
                    'address': address,
                    'emergency_contact_name': ec_name,
                    'emergency_contact_phone': ec_phone,
                    'family_members': json.dumps(parsed_family),
                    'default_city': default_city,
                })
                st.success("✅ Profile saved!")
                st.rerun()

def analyze_disaster(city, disaster_type, disasters, translator, lang):
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
            display_results(assessment, weather_data, disasters, translator, lang, city)

            # Save risk check to database
            if auth.is_logged_in(st.session_state):
                user = auth.get_current_user(st.session_state)
                weather_summary = (
                    f"Temp: {weather_data.get('main',{}).get('temp','?')}°C, "
                    f"Humidity: {weather_data.get('main',{}).get('humidity','?')}%, "
                    f"Rain: {weather_data.get('rain',{}).get('1h','0')}mm"
                )
                db.save_risk_check(
                    user_id=user['id'],
                    city=city,
                    disaster_type=assessment['disaster_type'],
                    risk_level=assessment['risk_level'],
                    risk_label=assessment['risk_label'],
                    confidence=assessment['prediction']['confidence'],
                    weather_summary=weather_summary,
                )
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("💡 Tip: Make sure the city name is correct and try again.")


def display_results(assessment, weather_data, disasters, translator, lang, city):
    """Display disaster risk results with all features"""
    
    risk_level = assessment['risk_level']
    risk_colors = {0: '#28a745', 1: '#ffc107', 2: '#fd7e14', 3: '#dc3545'}
    
    # Get translated message
    message = translator.get_message(
        disaster_type=assessment['disaster_type'].lower(),
        risk_level=risk_level,
        language=lang
    )
    
    # Big alert box
    st.markdown("---")
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {risk_colors[risk_level]}20 0%, {risk_colors[risk_level]}40 100%); 
                padding: 2rem; border-radius: 15px; border-left: 8px solid {risk_colors[risk_level]};">
        <h1 style="margin:0; color: {risk_colors[risk_level]};">{assessment['title']}</h1>
        <p style="font-size: 1.3rem; margin-top: 1rem;">{message}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics
    st.markdown(f"### 📊 {translator.get_text('risk_assessment', lang)}")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Disaster Type", assessment['disaster_type'])
    with col2:
        risk_label = translator.get_text(assessment['risk_label'].lower().replace(' ', '_'), lang)
        st.metric("Risk Level", risk_label, 
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
    
    # Actions (translated)
    st.markdown(f"### 🎯 {translator.get_text('recommended_actions', lang)}")
    
    # Get translated actions
    translated_actions = translator.get_actions(
        disaster_type=assessment['disaster_type'].lower(),
        risk_level=risk_level,
        language=lang
    )
    
    for i, action in enumerate(translated_actions, 1):
        priority = "🔴 URGENT" if risk_level >= 3 and i <= 2 else "🟡 IMPORTANT" if risk_level >= 2 else "🟢 ADVISED"
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1rem; margin: 0.5rem 0; color: #333;
                    border-radius: 8px; border-left: 4px solid {'#dc3545' if '🔴' in priority else '#ffc107' if '🟡' in priority else '#28a745'};">
            <strong>{priority} - Action {i}:</strong><br>{action}
        </div>
        """, unsafe_allow_html=True)
    
    # NEW: Emergency Resources (if risk is high)
    if risk_level >= 2:
        st.markdown("---")
        st.session_state.resource_locator.display_resources(
            location=city,
            risk_level=risk_level
        )
    
    # Emergency contacts
    if assessment.get('emergency_contacts'):
        st.markdown(f"### 📞 {translator.get_text('emergency_contacts', lang)}")
        cols = st.columns(len(assessment['emergency_contacts']))
        for col, (service, number) in zip(cols, assessment['emergency_contacts'].items()):
            with col:
                service_name = translator.get_text(service, lang) if service in ['ambulance', 'police', 'fire'] else service.replace('_', ' ').title()
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; background: #dc3545; 
                            color: white; border-radius: 10px;">
                    <h4 style="margin:0;">{service_name}</h4>
                    <h2 style="margin:0.5rem 0;">{number}</h2>
                </div>
                """, unsafe_allow_html=True)
    
    # Weather conditions
    with st.expander(f"🌤️ {translator.get_text('current_weather', lang)}", expanded=False):
        if 'main' in weather_data:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(f"🌡️ {translator.get_text('temperature', lang)}", 
                         f"{weather_data['main']['temp']:.1f}°C")
                st.metric(f"💧 {translator.get_text('humidity', lang)}", 
                         f"{weather_data['main']['humidity']}%")
            with col2:
                if 'wind' in weather_data:
                    st.metric(f"💨 {translator.get_text('wind_speed', lang)}", 
                             f"{weather_data['wind']['speed'] * 3.6:.1f} km/h")
                if 'main' in weather_data and 'pressure' in weather_data['main']:
                    st.metric("🌀 Pressure", f"{weather_data['main']['pressure']} hPa")
            with col3:
                rain = weather_data.get('rain', {}).get('1h', 0)
                st.metric(f"🌧️ {translator.get_text('rainfall', lang)}", f"{rain} mm")
                if 'weather' in weather_data and weather_data['weather']:
                    st.metric("☁️ Conditions", weather_data['weather'][0]['description'].title())
    
    # Probability chart
    with st.expander("📊 AI Prediction Analysis", expanded=False):
        probs = assessment['prediction']['all_probabilities']
        
        # Translate risk levels
        risk_labels_translated = [
            translator.get_text('safe', lang),
            translator.get_text('warning', lang),
            translator.get_text('high_risk', lang),
            translator.get_text('critical', lang)
        ]
        
        prob_df = pd.DataFrame({
            'Risk Level': risk_labels_translated,
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
                risk_labels_translated[0]: '#28a745',
                risk_labels_translated[1]: '#ffc107',
                risk_labels_translated[2]: '#fd7e14',
                risk_labels_translated[3]: '#dc3545'
            },
            title=f"{assessment['disaster_type']} Risk Distribution"
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)



if __name__ == "__main__":
    main()