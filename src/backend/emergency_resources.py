"""
Emergency Resources Locator
Finds nearby hospitals, shelters, fire stations, police stations
"""

import pandas as pd
import streamlit as st
from typing import Dict, List


class EmergencyResourceLocator:
    """Locate emergency resources for disaster response"""
    
    def __init__(self):
        # Major Indian cities with emergency resources
        self.resources = {
            'delhi': {
                'hospitals': [
                    {'name': 'AIIMS Delhi', 'phone': '011-26588500', 'address': 'Ansari Nagar, New Delhi'},
                    {'name': 'Safdarjung Hospital', 'phone': '011-26165060', 'address': 'Ring Road, New Delhi'},
                    {'name': 'Ram Manohar Lohia Hospital', 'phone': '011-23365525', 'address': 'Baba Kharak Singh Marg'},
                ],
                'shelters': [
                    {'name': 'Govt. Boys School', 'capacity': 500, 'address': 'Connaught Place'},
                    {'name': 'Community Hall - Karol Bagh', 'capacity': 300, 'address': 'Karol Bagh'},
                ],
                'police': [
                    {'name': 'Delhi Police HQ', 'phone': '011-23490000', 'address': 'ITO, New Delhi'},
                ],
                'fire': [
                    {'name': 'Delhi Fire Service', 'phone': '101', 'address': 'Multiple Stations'},
                ]
            },
            'mumbai': {
                'hospitals': [
                    {'name': 'KEM Hospital', 'phone': '022-24107000', 'address': 'Parel, Mumbai'},
                    {'name': 'Lilavati Hospital', 'phone': '022-26567891', 'address': 'Bandra West'},
                    {'name': 'JJ Hospital', 'phone': '022-23735555', 'address': 'Byculla, Mumbai'},
                ],
                'shelters': [
                    {'name': 'BMC Schools (Multiple)', 'capacity': 1000, 'address': 'Various Locations'},
                    {'name': 'Community Centers', 'capacity': 500, 'address': 'Ward-wise'},
                ],
                'police': [
                    {'name': 'Mumbai Police HQ', 'phone': '022-22620111', 'address': 'Crawford Market'},
                ],
                'fire': [
                    {'name': 'Mumbai Fire Brigade', 'phone': '101', 'address': 'Multiple Stations'},
                ]
            },
            'bangalore': {
                'hospitals': [
                    {'name': 'Victoria Hospital', 'phone': '080-26700301', 'address': 'K.R. Road'},
                    {'name': 'St. Johns Hospital', 'phone': '080-25532979', 'address': 'Koramangala'},
                    {'name': 'Manipal Hospital', 'phone': '080-25021000', 'address': 'Old Airport Road'},
                ],
                'shelters': [
                    {'name': 'Govt. Schools', 'capacity': 800, 'address': 'Multiple Locations'},
                    {'name': 'Community Halls', 'capacity': 400, 'address': 'Various Wards'},
                ],
                'police': [
                    {'name': 'Bangalore Police', 'phone': '080-22942322', 'address': 'Nrupathunga Road'},
                ],
                'fire': [
                    {'name': 'Bangalore Fire Service', 'phone': '101', 'address': 'Multiple Stations'},
                ]
            },
            'kolkata': {
                'hospitals': [
                    {'name': 'SSKM Hospital', 'phone': '033-22041000', 'address': 'College Street'},
                    {'name': 'Medical College Hospital', 'phone': '033-22413077', 'address': 'Park Street'},
                    {'name': 'Apollo Gleneagles', 'phone': '033-23203040', 'address': 'EM Bypass'},
                ],
                'shelters': [
                    {'name': 'Municipality Schools', 'capacity': 600, 'address': 'Various Areas'},
                    {'name': 'Relief Centers', 'capacity': 400, 'address': 'Ward-wise'},
                ],
                'police': [
                    {'name': 'Kolkata Police', 'phone': '033-22143000', 'address': 'Lalbazar'},
                ],
                'fire': [
                    {'name': 'Kolkata Fire Service', 'phone': '101', 'address': 'Multiple Stations'},
                ]
            },
            'chennai': {
                'hospitals': [
                    {'name': 'Rajiv Gandhi Govt. Hospital', 'phone': '044-25912121', 'address': 'Park Town'},
                    {'name': 'Apollo Hospital', 'phone': '044-28296000', 'address': 'Greams Road'},
                    {'name': 'Stanley Medical College', 'phone': '044-25281351', 'address': 'Old Jail Road'},
                ],
                'shelters': [
                    {'name': 'Corporation Schools', 'capacity': 700, 'address': 'Various Zones'},
                    {'name': 'Kalyana Mandapams', 'capacity': 500, 'address': 'Multiple Areas'},
                ],
                'police': [
                    {'name': 'Chennai Police', 'phone': '044-23452255', 'address': 'Egmore'},
                ],
                'fire': [
                    {'name': 'Chennai Fire Service', 'phone': '101', 'address': 'Multiple Stations'},
                ]
            },
            # Default for other cities
            'default': {
                'hospitals': [
                    {'name': 'District Hospital', 'phone': '108', 'address': 'Check local directory'},
                    {'name': 'Primary Health Center', 'phone': '108', 'address': 'Nearest PHC'},
                ],
                'shelters': [
                    {'name': 'Government Schools', 'capacity': 500, 'address': 'Contact District Collector'},
                    {'name': 'Community Centers', 'capacity': 300, 'address': 'Contact Municipal Office'},
                ],
                'police': [
                    {'name': 'Local Police Station', 'phone': '100', 'address': 'Nearest Station'},
                ],
                'fire': [
                    {'name': 'Fire Service', 'phone': '101', 'address': 'District Headquarters'},
                ]
            }
        }
    
    def get_resources(self, location: str, disaster_type: str = None) -> Dict:
        """Get emergency resources for a location"""
        location_lower = location.lower().strip()
        
        city_resources = None
        for city_key in self.resources.keys():
            if city_key in location_lower:
                city_resources = self.resources[city_key]
                break
        
        if not city_resources:
            city_resources = self.resources['default']
        
        return {
            'hospitals': city_resources['hospitals'],
            'shelters': city_resources['shelters'],
            'police': city_resources['police'],
            'fire': city_resources['fire'],
            'national_emergency': {
                'ambulance': '108/102',
                'police': '100',
                'fire': '101',
                'disaster_mgmt': '1078',
                'women_helpline': '1091',
                'child_helpline': '1098'
            }
        }
    
    def display_resources(self, location: str, risk_level: int = 0):
        """Display emergency resources in Streamlit"""
        
        resources = self.get_resources(location)
        
        st.markdown("### 🏥 Emergency Resources")
        
        # National emergency numbers (always show)
        with st.expander("📞 National Emergency Numbers", expanded=True):
            cols = st.columns(3)
            national = resources['national_emergency']
            
            with cols[0]:
                st.markdown(f"""
                <div style='background: #dc3545; color: white; padding: 1rem; border-radius: 10px; text-align: center;'>
                    <h3 style='margin:0; color: white;'>🚑 Ambulance</h3>
                    <h2 style='margin:0.5rem 0; color: white;'>{national['ambulance']}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with cols[1]:
                st.markdown(f"""
                <div style='background: #007bff; color: white; padding: 1rem; border-radius: 10px; text-align: center;'>
                    <h3 style='margin:0; color: white;'>👮 Police</h3>
                    <h2 style='margin:0.5rem 0; color: white;'>{national['police']}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with cols[2]:
                st.markdown(f"""
                <div style='background: #fd7e14; color: white; padding: 1rem; border-radius: 10px; text-align: center;'>
                    <h3 style='margin:0; color: white;'>🔥 Fire</h3>
                    <h2 style='margin:0.5rem 0; color: white;'>{national['fire']}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            cols2 = st.columns(3)
            with cols2[0]:
                st.info(f"🆘 Disaster Management: **{national['disaster_mgmt']}**")
            with cols2[1]:
                st.info(f"👩 Women Helpline: **{national['women_helpline']}**")
            with cols2[2]:
                st.info(f"👶 Child Helpline: **{national['child_helpline']}**")
        
        # Show detailed resources only if risk level is high
        if risk_level >= 2:
            # Hospitals
            with st.expander("🏥 Nearby Hospitals", expanded=True):
                for hospital in resources['hospitals']:
                    st.markdown(f"""
                    <div style='background: #f8f9fa; padding: 1rem; margin: 0.5rem 0; border-radius: 8px; border-left: 4px solid #28a745;'>
                        <h4 style='margin:0; color: #28a745;'>{hospital['name']}</h4>
                        <p style='margin:0.5rem 0; color: #333;'>📞 {hospital['phone']}</p>
                        <p style='margin:0; color: #555;'>📍 {hospital['address']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Shelters
            with st.expander("🏠 Emergency Shelters", expanded=True):
                for shelter in resources['shelters']:
                    capacity = shelter.get('capacity', 'N/A')
                    st.markdown(f"""
                    <div style='background: #f8f9fa; padding: 1rem; margin: 0.5rem 0; border-radius: 8px; border-left: 4px solid #007bff;'>
                        <h4 style='margin:0; color: #007bff;'>{shelter['name']}</h4>
                        <p style='margin:0.5rem 0; color: #333;'>👥 Capacity: {capacity} people</p>
                        <p style='margin:0; color: #555;'>📍 {shelter['address']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("💡 Detailed hospital and shelter information will appear when risk level is High or Critical")
        
        # Always show essential services
        with st.expander("🚓 Essential Services"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**👮 Police Stations**")
                for station in resources['police']:
                    st.markdown(f"• {station['name']}: {station['phone']}")
            
            with col2:
                st.markdown("**🚒 Fire Stations**")
                for station in resources['fire']:
                    st.markdown(f"• {station['name']}: {station['phone']}")


# Quick test function
def test_locator():
    """Test the emergency locator"""
    locator = EmergencyResourceLocator()
    
    print("Testing Emergency Resource Locator...")
    print("="*70)
    
    test_cities = ['Delhi', 'Mumbai', 'Lucknow']
    
    for city in test_cities:
        print(f"\n{city}:")
        resources = locator.get_resources(city)
        print(f"  Hospitals: {len(resources['hospitals'])}")
        print(f"  Shelters: {len(resources['shelters'])}")
        print(f"  National Emergency: {resources['national_emergency']['ambulance']}")
    
    print("\n" + "="*70)
    print("✅ Test complete!")


if __name__ == "__main__":
    test_locator()