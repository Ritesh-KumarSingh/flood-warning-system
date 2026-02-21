"""
Live Location Sharing & Family Safety Check
Allows users to share location with family and check if they're safe
"""

import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

class FamilySafetyTracker:
    """Track family members' locations and safety status during disasters"""
    
    def __init__(self, data_file='../../data/family_safety.json'):
        self.data_file = data_file
        self.circles = self._load_circles()
    
    def _load_circles(self):
        """Load family circles data"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_circles(self):
        """Save family circles data"""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w') as f:
                json.dump(self.circles, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving: {e}")
            return False
    
    def create_circle(self, user_id, circle_name):
        """Create a new family safety circle"""
        if user_id not in self.circles:
            self.circles[user_id] = {
                'circles': {},
                'my_status': {
                    'safe': True,
                    'location': None,
                    'last_updated': None
                }
            }
        
        circle_id = f"{user_id}_{circle_name.lower().replace(' ', '_')}"
        self.circles[user_id]['circles'][circle_id] = {
            'name': circle_name,
            'members': [],
            'created': datetime.now().isoformat()
        }
        
        self._save_circles()
        return circle_id
    
    def add_member(self, user_id, circle_id, member_data):
        """Add a member to a safety circle"""
        if user_id in self.circles and circle_id in self.circles[user_id]['circles']:
            member = {
                'name': member_data['name'],
                'phone': member_data['phone'],
                'relation': member_data['relation'],
                'location': member_data.get('location', 'Unknown'),
                'safe': None,  # Unknown status
                'last_checkin': None
            }
            
            self.circles[user_id]['circles'][circle_id]['members'].append(member)
            self._save_circles()
            return True
        return False
    
    def update_my_status(self, user_id, safe, location=None):
        """Update user's own safety status"""
        if user_id not in self.circles:
            self.circles[user_id] = {
                'circles': {},
                'my_status': {}
            }
        
        self.circles[user_id]['my_status'] = {
            'safe': safe,
            'location': location,
            'last_updated': datetime.now().isoformat()
        }
        
        self._save_circles()
        return True
    
    def update_member_status(self, user_id, circle_id, member_index, safe, location=None):
        """Update a family member's status"""
        if user_id in self.circles and circle_id in self.circles[user_id]['circles']:
            if member_index < len(self.circles[user_id]['circles'][circle_id]['members']):
                self.circles[user_id]['circles'][circle_id]['members'][member_index]['safe'] = safe
                if location:
                    self.circles[user_id]['circles'][circle_id]['members'][member_index]['location'] = location
                self.circles[user_id]['circles'][circle_id]['members'][member_index]['last_checkin'] = datetime.now().isoformat()
                self._save_circles()
                return True
        return False
    
    def get_circle_status(self, user_id, circle_id):
        """Get safety status of all members in a circle"""
        if user_id in self.circles and circle_id in self.circles[user_id]['circles']:
            members = self.circles[user_id]['circles'][circle_id]['members']
            
            safe_count = sum(1 for m in members if m['safe'] == True)
            unsafe_count = sum(1 for m in members if m['safe'] == False)
            unknown_count = sum(1 for m in members if m['safe'] is None)
            
            return {
                'total': len(members),
                'safe': safe_count,
                'unsafe': unsafe_count,
                'unknown': unknown_count,
                'members': members
            }
        return None
    
    def display_safety_interface(self):
        """Display family safety tracking interface in Streamlit"""
        
        st.markdown("### 👨‍👩‍👧‍👦 Family Safety Tracker")
        
        # User ID (simplified - in production use proper auth)
        if 'user_id' not in st.session_state:
            st.session_state.user_id = f"user_{hash(datetime.now()) % 10000}"
        
        user_id = st.session_state.user_id
        
        # My Status
        st.markdown("#### 📍 My Status")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            my_location = st.text_input("My Current Location", 
                                       placeholder="e.g., Connaught Place, Delhi",
                                       key='my_loc')
        
        with col2:
            if st.button("✅ I'm Safe", type="primary", use_container_width=True):
                self.update_my_status(user_id, True, my_location)
                st.success("✅ Status updated: You're marked as SAFE")
        
        with col3:
            if st.button("🆘 Need Help", use_container_width=True):
                self.update_my_status(user_id, False, my_location)
                st.error("🆘 Status updated: HELP NEEDED")
                st.markdown("**Emergency: 112**")
        
        # Show my current status
        if user_id in self.circles and self.circles[user_id]['my_status'].get('last_updated'):
            status = self.circles[user_id]['my_status']
            status_emoji = "✅" if status['safe'] else "🆘"
            status_text = "SAFE" if status['safe'] else "NEED HELP"
            status_color = "green" if status['safe'] else "red"
            
            st.markdown(f"""
            <div style='background: {status_color}20; padding: 1rem; border-radius: 8px; border-left: 4px solid {status_color};'>
                <strong>{status_emoji} Your Status: {status_text}</strong><br>
                📍 Location: {status.get('location', 'Not provided')}<br>
                🕐 Last updated: {datetime.fromisoformat(status['last_updated']).strftime('%I:%M %p')}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Family Circles
        st.markdown("#### 👥 Family Circles")
        
        # Create or select circle
        if user_id not in self.circles or not self.circles[user_id]['circles']:
            # Create first circle
            with st.form("create_circle"):
                circle_name = st.text_input("Circle Name", placeholder="e.g., My Family")
                
                if st.form_submit_button("Create Circle"):
                    if circle_name:
                        circle_id = self.create_circle(user_id, circle_name)
                        st.success(f"✅ Circle '{circle_name}' created!")
                        st.rerun()
        else:
            # Select existing circle
            circles = self.circles[user_id]['circles']
            circle_names = {cid: data['name'] for cid, data in circles.items()}
            
            selected_circle = st.selectbox(
                "Select Circle",
                options=list(circle_names.keys()),
                format_func=lambda x: circle_names[x]
            )
            
            if selected_circle:
                self._display_circle_members(user_id, selected_circle)
    
    def _display_circle_members(self, user_id, circle_id):
        """Display members of a circle"""
        
        circle_data = self.circles[user_id]['circles'][circle_id]
        
        # Add member form
        with st.expander("➕ Add Family Member", expanded=False):
            with st.form("add_member"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Name", placeholder="e.g., John Doe")
                    relation = st.selectbox("Relation", 
                        ["Spouse", "Parent", "Child", "Sibling", "Grandparent", "Other"])
                
                with col2:
                    phone = st.text_input("Phone", placeholder="+91 XXXXX XXXXX")
                    location = st.text_input("Last Known Location", placeholder="Optional")
                
                if st.form_submit_button("Add Member"):
                    if name and phone:
                        member_data = {
                            'name': name,
                            'phone': phone,
                            'relation': relation,
                            'location': location
                        }
                        self.add_member(user_id, circle_id, member_data)
                        st.success(f"✅ {name} added to circle!")
                        st.rerun()
        
        # Display members
        st.markdown("#### Family Members Status")
        
        status_summary = self.get_circle_status(user_id, circle_id)
        
        if status_summary:
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Members", status_summary['total'])
            with col2:
                st.metric("✅ Safe", status_summary['safe'])
            with col3:
                st.metric("🆘 Need Help", status_summary['unsafe'])
            with col4:
                st.metric("❓ Unknown", status_summary['unknown'])
            
            st.markdown("---")
            
            # Individual members
            for idx, member in enumerate(status_summary['members']):
                # Status indicators
                if member['safe'] == True:
                    status_emoji = "✅"
                    status_text = "SAFE"
                    status_color = "#28a745"
                elif member['safe'] == False:
                    status_emoji = "🆘"
                    status_text = "NEED HELP"
                    status_color = "#dc3545"
                else:
                    status_emoji = "❓"
                    status_text = "UNKNOWN"
                    status_color = "#6c757d"
                
                # Member card
                st.markdown(f"""
                <div style='background: {status_color}15; padding: 1rem; margin: 0.5rem 0; 
                            border-radius: 10px; border-left: 5px solid {status_color};'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <h4 style='margin:0;'>{status_emoji} {member['name']}</h4>
                            <p style='margin:0.3rem 0; color: #666;'>
                                👤 {member['relation']} | 📞 {member['phone']}<br>
                                📍 {member['location']}
                            </p>
                        </div>
                        <div style='text-align: right;'>
                            <span style='font-weight: bold; color: {status_color};'>{status_text}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Quick status update buttons
                col_btn1, col_btn2, col_btn3, col_btn4 = st.columns([1, 1, 1, 4])
                
                with col_btn1:
                    if st.button("✅ Safe", key=f"safe_{idx}"):
                        self.update_member_status(user_id, circle_id, idx, True)
                        st.rerun()
                
                with col_btn2:
                    if st.button("🆘 Help", key=f"help_{idx}"):
                        self.update_member_status(user_id, circle_id, idx, False)
                        st.rerun()
                
                with col_btn3:
                    if st.button("📞 Call", key=f"call_{idx}"):
                        st.info(f"📞 Calling {member['phone']}...")
                
                st.markdown("---")
        else:
            st.info("No members in this circle yet. Add family members above!")
        
        # Share circle link
        st.markdown("#### 🔗 Share Circle")
        share_code = f"CIRCLE-{circle_id[-6:].upper()}"
        st.code(share_code, language=None)
        st.caption("Share this code with family members to join your circle")


# Test function
def test_tracker():
    """Test family safety tracker"""
    tracker = FamilySafetyTracker()
    
    print("Testing Family Safety Tracker...")
    print("="*70)
    
    # Create test circle
    user_id = "test_user_123"
    circle_id = tracker.create_circle(user_id, "Test Family")
    print(f"Created circle: {circle_id}")
    
    # Add member
    member = {
        'name': 'John Doe',
        'phone': '+91 98765 43210',
        'relation': 'Spouse',
        'location': 'Delhi'
    }
    tracker.add_member(user_id, circle_id, member)
    print(f"Added member: {member['name']}")
    
    # Update status
    tracker.update_my_status(user_id, True, "Home")
    print("Updated my status: SAFE")
    
    # Get status
    status = tracker.get_circle_status(user_id, circle_id)
    print(f"Circle status: {status}")
    
    print("="*70)
    print("✅ Test complete!")


if __name__ == "__main__":
    test_tracker()