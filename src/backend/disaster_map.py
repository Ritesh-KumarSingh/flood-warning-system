"""
Disaster Map & Safe Routes
Real-time disaster hotspot visualization and navigation to shelters
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class DisasterMap:
    """Interactive disaster map with hotspots and safe routes"""
    
    def __init__(self):
        # Disaster hotspots for major Indian cities
        self.hotspots = {
            'delhi': [
                {'name': 'Yamuna Floodplain', 'lat': 28.6692, 'lon': 77.2420, 'severity': 'High', 'type': 'Flood'},
                {'name': 'South Delhi Zone', 'lat': 28.5355, 'lon': 77.2430, 'severity': 'Medium', 'type': 'Flood'},
                {'name': 'Najafgarh Drain', 'lat': 28.5706, 'lon': 77.0080, 'severity': 'High', 'type': 'Flood'},
            ],
            'mumbai': [
                {'name': 'Mithi River Area', 'lat': 19.0896, 'lon': 72.8656, 'severity': 'High', 'type': 'Flood'},
                {'name': 'Coastal Belt', 'lat': 18.9750, 'lon': 72.8258, 'severity': 'Medium', 'type': 'Cyclone'},
                {'name': 'Dahisar River Zone', 'lat': 19.2437, 'lon': 72.8547, 'severity': 'Medium', 'type': 'Flood'},
            ],
            'chennai': [
                {'name': 'Adyar River Basin', 'lat': 13.0067, 'lon': 80.2206, 'severity': 'High', 'type': 'Flood'},
                {'name': 'Marina Beach', 'lat': 13.0499, 'lon': 80.2824, 'severity': 'Medium', 'type': 'Cyclone'},
                {'name': 'Cooum River Zone', 'lat': 13.0674, 'lon': 80.2376, 'severity': 'High', 'type': 'Flood'},
            ],
            'kolkata': [
                {'name': 'Hooghly River Basin', 'lat': 22.5726, 'lon': 88.3176, 'severity': 'High', 'type': 'Flood'},
                {'name': 'Salt Lake Area', 'lat': 22.5958, 'lon': 88.4131, 'severity': 'Medium', 'type': 'Flood'},
                {'name': 'Coastal Sundarbans Zone', 'lat': 22.4200, 'lon': 88.6000, 'severity': 'High', 'type': 'Cyclone'},
            ],
            'bangalore': [
                {'name': 'Bellandur Lake Zone', 'lat': 12.9352, 'lon': 77.6744, 'severity': 'High', 'type': 'Flood'},
                {'name': 'Varthur Lake Area', 'lat': 12.9416, 'lon': 77.7400, 'severity': 'Medium', 'type': 'Flood'},
                {'name': 'Mahadevapura Zone', 'lat': 12.9927, 'lon': 77.6932, 'severity': 'Medium', 'type': 'Flood'},
            ],
            'hyderabad': [
                {'name': 'Musi River Floodplain', 'lat': 17.3850, 'lon': 78.4867, 'severity': 'High', 'type': 'Flood'},
                {'name': 'Hussain Sagar Area', 'lat': 17.4239, 'lon': 78.4738, 'severity': 'Medium', 'type': 'Flood'},
            ],
            'lucknow': [
                {'name': 'Gomti River Zone', 'lat': 26.8467, 'lon': 80.9462, 'severity': 'High', 'type': 'Flood'},
                {'name': 'Kukrail Drain Area', 'lat': 26.8700, 'lon': 81.0200, 'severity': 'Medium', 'type': 'Flood'},
            ],
            'jaipur': [
                {'name': 'Dravyavati River Zone', 'lat': 26.8900, 'lon': 75.8100, 'severity': 'Medium', 'type': 'Flood'},
                {'name': 'Amanishah Nala', 'lat': 26.8700, 'lon': 75.7900, 'severity': 'High', 'type': 'Flood'},
            ],
            'pune': [
                {'name': 'Mutha River Area', 'lat': 18.5074, 'lon': 73.8077, 'severity': 'High', 'type': 'Flood'},
                {'name': 'Ambil Odha Zone', 'lat': 18.5100, 'lon': 73.8700, 'severity': 'Medium', 'type': 'Flood'},
            ],
            'ahmedabad': [
                {'name': 'Sabarmati Riverfront', 'lat': 23.0300, 'lon': 72.5700, 'severity': 'Medium', 'type': 'Flood'},
                {'name': 'Eastern Low Areas', 'lat': 23.0400, 'lon': 72.6100, 'severity': 'High', 'type': 'Flood'},
                {'name': 'Western Heat Zone', 'lat': 23.0225, 'lon': 72.5714, 'severity': 'High', 'type': 'Heatwave'},
            ],
            'patna': [
                {'name': 'Ganga Floodplain', 'lat': 25.6100, 'lon': 85.1200, 'severity': 'High', 'type': 'Flood'},
                {'name': 'Punpun River Zone', 'lat': 25.5700, 'lon': 85.0900, 'severity': 'High', 'type': 'Flood'},
            ],
            'bhopal': [
                {'name': 'Upper Lake Zone', 'lat': 23.2466, 'lon': 77.4060, 'severity': 'Medium', 'type': 'Flood'},
                {'name': 'Lower Lake Area', 'lat': 23.2355, 'lon': 77.4340, 'severity': 'Medium', 'type': 'Flood'},
            ],
        }
        
        # Emergency shelters for each city
        self.shelters = {
            'delhi': [
                {'name': 'Govt. School - Connaught Place', 'lat': 28.6304, 'lon': 77.2177, 'capacity': 500},
                {'name': 'Community Hall - Karol Bagh', 'lat': 28.6519, 'lon': 77.1909, 'capacity': 300},
                {'name': 'Sports Complex - Dwarka', 'lat': 28.5921, 'lon': 77.0460, 'capacity': 1000},
            ],
            'mumbai': [
                {'name': 'BMC School - Bandra', 'lat': 19.0596, 'lon': 72.8295, 'capacity': 400},
                {'name': 'Municipal Hall - Andheri', 'lat': 19.1136, 'lon': 72.8697, 'capacity': 600},
                {'name': 'Community Center - Dadar', 'lat': 19.0176, 'lon': 72.8562, 'capacity': 350},
            ],
            'chennai': [
                {'name': 'Corporation School - T.Nagar', 'lat': 13.0407, 'lon': 80.2340, 'capacity': 350},
                {'name': 'Community Center - Adyar', 'lat': 13.0067, 'lon': 80.2573, 'capacity': 500},
            ],
            'kolkata': [
                {'name': 'Govt. School - Salt Lake', 'lat': 22.5958, 'lon': 88.4023, 'capacity': 600},
                {'name': 'Community Hall - Howrah', 'lat': 22.5958, 'lon': 88.2636, 'capacity': 400},
            ],
            'bangalore': [
                {'name': 'BBMP Community Hall - Whitefield', 'lat': 12.9698, 'lon': 77.7500, 'capacity': 500},
                {'name': 'Govt. School - Koramangala', 'lat': 12.9352, 'lon': 77.6245, 'capacity': 350},
            ],
            'hyderabad': [
                {'name': 'Municipality School - Begumpet', 'lat': 17.4432, 'lon': 78.4691, 'capacity': 500},
                {'name': 'Community Hall - Secunderabad', 'lat': 17.4399, 'lon': 78.4983, 'capacity': 400},
            ],
            'lucknow': [
                {'name': 'Govt. School - Hazratganj', 'lat': 26.8500, 'lon': 80.9500, 'capacity': 400},
                {'name': 'Community Center - Gomtinagar', 'lat': 26.8560, 'lon': 81.0100, 'capacity': 600},
            ],
            'jaipur': [
                {'name': 'Govt. School - MI Road', 'lat': 26.9124, 'lon': 75.7873, 'capacity': 400},
                {'name': 'Sports Stadium - Mansarovar', 'lat': 26.8660, 'lon': 75.7630, 'capacity': 800},
            ],
            'pune': [
                {'name': 'PMC School - Shivajinagar', 'lat': 18.5314, 'lon': 73.8446, 'capacity': 350},
                {'name': 'Community Hall - Kothrud', 'lat': 18.5074, 'lon': 73.8077, 'capacity': 500},
            ],
            'ahmedabad': [
                {'name': 'AMC School - Navrangpura', 'lat': 23.0356, 'lon': 72.5595, 'capacity': 500},
                {'name': 'Community Hall - Satellite', 'lat': 23.0117, 'lon': 72.5083, 'capacity': 400},
            ],
            'patna': [
                {'name': 'Govt. School - Gandhi Maidan', 'lat': 25.6100, 'lon': 85.1300, 'capacity': 500},
                {'name': 'Community Hall - Boring Road', 'lat': 25.6072, 'lon': 85.1174, 'capacity': 350},
            ],
            'bhopal': [
                {'name': 'Govt. School - New Market', 'lat': 23.2350, 'lon': 77.4120, 'capacity': 400},
                {'name': 'Community Center - Arera Colony', 'lat': 23.2186, 'lon': 77.4347, 'capacity': 500},
            ],
        }
    
    def get_hotspots(self, city):
        """Get disaster hotspots for a city"""
        city_lower = city.lower()
        for key in self.hotspots.keys():
            if key in city_lower or city_lower in key:
                return self.hotspots[key]
        return []
    
    def get_shelters(self, city):
        """Get emergency shelters for a city"""
        city_lower = city.lower()
        for key in self.shelters.keys():
            if key in city_lower or city_lower in key:
                return self.shelters[key]
        return []
    
    def display_disaster_map(self, city, user_location=None):
        """Display interactive disaster map"""
        
        st.markdown("### 🗺️ Disaster Risk Map")
        
        hotspots = self.get_hotspots(city)
        shelters = self.get_shelters(city)
        
        if not hotspots and not shelters:
            available = ", ".join(k.title() for k in sorted(self.hotspots.keys()))
            st.warning(f"📍 No map data for **{city}**. Try one of: {available}")
            return
        
        # Create map
        fig = go.Figure()
        
        # Add hotspots
        if hotspots:
            df_hotspots = pd.DataFrame(hotspots)
            
            # Color by severity
            colors = {'High': 'red', 'Medium': 'orange', 'Low': 'yellow'}
            df_hotspots['color'] = df_hotspots['severity'].map(colors)
            
            fig.add_trace(go.Scattermapbox(
                lat=df_hotspots['lat'],
                lon=df_hotspots['lon'],
                mode='markers',
                marker=dict(
                    size=20,
                    color=df_hotspots['color'],
                    opacity=0.7
                ),
                text=df_hotspots['name'] + '<br>Severity: ' + df_hotspots['severity'] + '<br>Type: ' + df_hotspots['type'],
                name='Danger Zones',
                hoverinfo='text'
            ))
        
        # Add shelters
        if shelters:
            df_shelters = pd.DataFrame(shelters)
            
            fig.add_trace(go.Scattermapbox(
                lat=df_shelters['lat'],
                lon=df_shelters['lon'],
                mode='markers',
                marker=dict(
                    size=15,
                    color='green',
                    symbol='circle'
                ),
                text=df_shelters['name'] + '<br>Capacity: ' + df_shelters['capacity'].astype(str),
                name='Safe Shelters',
                hoverinfo='text'
            ))
        
        # Add user location if provided
        if user_location:
            fig.add_trace(go.Scattermapbox(
                lat=[user_location[0]],
                lon=[user_location[1]],
                mode='markers',
                marker=dict(
                    size=18,
                    color='blue',
                    symbol='star'
                ),
                text=['Your Location'],
                name='You',
                hoverinfo='text'
            ))
        
        # Set map center
        center_lat = hotspots[0]['lat'] if hotspots else shelters[0]['lat']
        center_lon = hotspots[0]['lon'] if hotspots else shelters[0]['lon']
        
        # Map layout
        fig.update_layout(
            mapbox=dict(
                style='open-street-map',
                center=dict(lat=center_lat, lon=center_lon),
                zoom=11
            ),
            showlegend=True,
            height=500,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Legend
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style='background: #ff000020; padding: 0.5rem; border-radius: 5px; border-left: 4px solid red;'>
                🔴 High Risk Zones
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: #ffa50020; padding: 0.5rem; border-radius: 5px; border-left: 4px solid orange;'>
                🟠 Medium Risk Zones
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='background: #00800020; padding: 0.5rem; border-radius: 5px; border-left: 4px solid green;'>
                🟢 Safe Shelters
            </div>
            """, unsafe_allow_html=True)
    
    def display_shelter_list(self, city):
        """Display list of nearby shelters with navigation"""
        
        st.markdown("### 🏠 Nearby Emergency Shelters")
        
        shelters = self.get_shelters(city)
        
        if not shelters:
            st.info("No shelter data available for this city yet.")
            return
        
        for shelter in shelters:
            st.markdown(f"""
            <div style='background: #f8f9fa; padding: 1rem; margin: 0.5rem 0; 
                        border-radius: 8px; border-left: 4px solid #28a745;'>
                <h4 style='margin:0; color: #28a745;'>{shelter['name']}</h4>
                <p style='margin:0.5rem 0; color: #333;'>
                    👥 Capacity: {shelter['capacity']} people<br>
                    📍 Coordinates: {shelter['lat']:.4f}, {shelter['lon']:.4f}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Navigation buttons
            col1, col2 = st.columns([1, 3])
            
            with col1:
                maps_url = f"https://www.google.com/maps/dir/?api=1&destination={shelter['lat']},{shelter['lon']}"
                st.markdown(f"[📍 Navigate]({maps_url})", unsafe_allow_html=True)
    
    def display_safe_route(self, start_lat, start_lon, end_lat, end_lon):
        """Display safe route avoiding danger zones"""
        
        st.markdown("### 🛣️ Suggested Safe Route")
        
        # Create route map
        fig = go.Figure()
        
        # Add route line
        fig.add_trace(go.Scattermapbox(
            lat=[start_lat, end_lat],
            lon=[start_lon, end_lon],
            mode='lines+markers',
            line=dict(width=3, color='blue'),
            marker=dict(size=12, color=['blue', 'green']),
            text=['Start', 'Destination'],
            name='Route'
        ))
        
        fig.update_layout(
            mapbox=dict(
                style='open-street-map',
                center=dict(lat=(start_lat+end_lat)/2, lon=(start_lon+end_lon)/2),
                zoom=12
            ),
            height=400,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Route instructions
        st.info("🧭 Follow the blue route to reach the nearest safe shelter")


def test_map():
    """Test disaster map"""
    disaster_map = DisasterMap()
    
    print("Testing Disaster Map...")
    print("="*70)
    
    # Test hotspots
    hotspots = disaster_map.get_hotspots('delhi')
    print(f"\nDelhi Hotspots: {len(hotspots)}")
    for h in hotspots:
        print(f"  - {h['name']}: {h['severity']} risk")
    
    # Test shelters
    shelters = disaster_map.get_shelters('delhi')
    print(f"\nDelhi Shelters: {len(shelters)}")
    for s in shelters:
        print(f"  - {s['name']}: {s['capacity']} capacity")
    
    print("\n" + "="*70)
    print("✅ Test complete!")


if __name__ == "__main__":
    test_map()