"""
Community Disaster Reporting System
Allows users to report disasters they're experiencing in real-time
Crowdsourced data for better situational awareness
"""

import pandas as pd
from datetime import datetime
import streamlit as st
import json
import os
import uuid

class CommunityReporter:
    """Handle community-submitted disaster reports"""
    
    def __init__(self, data_file='../../data/community_reports.json'):
        self.data_file = data_file
        self.reports = self._load_reports()
    
    def _load_reports(self):
        """Load existing reports from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def _save_reports(self):
        """Save reports to file"""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w') as f:
                json.dump(self.reports, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving reports: {e}")
            return False
    
    def submit_report(self, report_data):
        """Submit a new disaster report"""
        report = {
            'id': uuid.uuid4().hex[:8],
            'timestamp': datetime.now().isoformat(),
            'location': report_data['location'],
            'disaster_type': report_data['disaster_type'],
            'severity': report_data['severity'],
            'description': report_data['description'],
            'affected_count': report_data.get('affected_count', 0),
            'needs_help': report_data.get('needs_help', False),
            'verified': False,
            'upvotes': 0
        }
        
        self.reports.append(report)
        self._save_reports()
        
        return report['id']
    
    def get_recent_reports(self, location=None, disaster_type=None, limit=10):
        """Get recent reports, optionally filtered"""
        filtered = self.reports.copy()
        
        if location:
            filtered = [r for r in filtered 
                       if location.lower() in r['location'].lower()]
        
        if disaster_type:
            filtered = [r for r in filtered 
                       if r['disaster_type'].lower() == disaster_type.lower()]
        
        # Sort by timestamp (most recent first)
        filtered = sorted(filtered, 
                         key=lambda x: x['timestamp'], 
                         reverse=True)
        
        return filtered[:limit]
    
    def get_location_summary(self, location):
        """Get summary of reports for a location"""
        reports = self.get_recent_reports(location=location, limit=100)
        
        if not reports:
            return None
        
        df = pd.DataFrame(reports)
        
        return {
            'total_reports': len(reports),
            'severity_distribution': df['severity'].value_counts().to_dict(),
            'disaster_types': df['disaster_type'].value_counts().to_dict(),
            'help_needed': len(df[df['needs_help'] == True]),
            'last_report': reports[0]['timestamp']
        }
    
    def upvote_report(self, report_id):
        """Upvote a report to verify it"""
        for report in self.reports:
            if report['id'] == report_id:
                report['upvotes'] += 1
                if report['upvotes'] >= 3:
                    report['verified'] = True
                self._save_reports()
                return True
        return False
    
    def display_report_form(self):
        """Display report submission form in Streamlit"""
        
        st.markdown("### 📝 Report a Disaster")
        st.info("Help your community by reporting disasters you're experiencing")
        
        with st.form("disaster_report"):
            col1, col2 = st.columns(2)
            
            with col1:
                location = st.text_input("📍 Location", 
                                        placeholder="e.g., Connaught Place, Delhi")
                
                disaster_type = st.selectbox("🌪️ Disaster Type",
                    ['Flood', 'Earthquake', 'Cyclone', 'Landslide', 
                     'Heatwave', 'Fire', 'Other'])
            
            with col2:
                severity = st.select_slider("⚠️ Severity",
                    options=['Minor', 'Moderate', 'Severe', 'Critical'])
                
                affected_count = st.number_input("👥 Approx. People Affected",
                    min_value=0, max_value=100000, step=10)
            
            description = st.text_area("📄 Description",
                placeholder="Describe what's happening (water level, damage, casualties, etc.)",
                max_chars=500)
            
            needs_help = st.checkbox("🆘 We need immediate help")
            
            col_btn1, col_btn2 = st.columns([1, 3])
            
            with col_btn1:
                submit = st.form_submit_button("Submit Report", 
                                              type="primary",
                                              use_container_width=True)
            
            if submit:
                if not location or not description:
                    st.error("❌ Please fill in location and description")
                else:
                    report_data = {
                        'location': location,
                        'disaster_type': disaster_type,
                        'severity': severity,
                        'description': description,
                        'affected_count': affected_count,
                        'needs_help': needs_help
                    }
                    
                    report_id = self.submit_report(report_data)
                    
                    st.success(f"✅ Report submitted successfully! (ID: #{report_id})")
                    st.balloons()
                    
                    if needs_help:
                        st.error("🚨 Emergency services have been notified!")
                        st.markdown("**Call:**")
                        st.markdown("- 🚑 Ambulance: **108**")
                        st.markdown("- 👮 Police: **100**")
                        st.markdown("- 🔥 Fire: **101**")
    
    def display_community_feed(self, location=None):
        """Display community reports feed"""
        
        st.markdown("### 🌐 Community Reports")
        
        reports = self.get_recent_reports(location=location, limit=20)
        
        if not reports:
            st.info("No reports yet. Be the first to report!")
            return
        
        # Summary
        if location:
            summary = self.get_location_summary(location)
            if summary:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Reports", summary['total_reports'])
                with col2:
                    st.metric("Help Requests", summary['help_needed'])
                with col3:
                    disaster_types = summary['disaster_types']
                    most_common = max(disaster_types, key=disaster_types.get)
                    st.metric("Most Reported", most_common)
        
        st.markdown("---")
        
        # Display reports
        for report in reports:
            severity_colors = {
                'Minor': '#28a745',
                'Moderate': '#ffc107',
                'Severe': '#fd7e14',
                'Critical': '#dc3545'
            }
            
            color = severity_colors.get(report['severity'], '#6c757d')
            verified = "✓ Verified" if report['verified'] else f"👍 {report['upvotes']}"
            
            # Time ago
            report_time = datetime.fromisoformat(report['timestamp'])
            time_diff = datetime.now() - report_time
            
            total_secs = int(time_diff.total_seconds())
            if total_secs < 3600:
                time_ago = f"{total_secs // 60} min ago"
            elif total_secs < 86400:
                time_ago = f"{total_secs // 3600} hours ago"
            else:
                time_ago = f"{time_diff.days} days ago"
            
            help_badge = "🆘 **HELP NEEDED**" if report['needs_help'] else ""
            
            st.markdown(f"""
            <div style='background: {color}15; padding: 1rem; margin: 0.5rem 0; 
                        border-radius: 10px; border-left: 5px solid {color};'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <h4 style='margin:0; color: {color};'>
                        {report['disaster_type']} - {report['severity']}
                    </h4>
                    <span style='color: #666; font-size: 0.9em;'>{time_ago}</span>
                </div>
                <p style='margin:0.5rem 0; font-weight: bold;'>📍 {report['location']}</p>
                <p style='margin:0.5rem 0;'>{report['description']}</p>
                <div style='margin-top:0.5rem; display: flex; justify-content: space-between; align-items: center;'>
                    <span>👥 {report['affected_count']} affected | {verified}</span>
                    <span style='color: red; font-weight: bold;'>{help_badge}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Upvote button
            col_vote1, col_vote2, col_vote3 = st.columns([1, 1, 8])
            with col_vote1:
                if st.button("👍", key=f"upvote_{report['id']}", 
                           help="Verify this report"):
                    self.upvote_report(report['id'])
                    st.rerun()


# Quick test
def test_reporter():
    """Test community reporter"""
    reporter = CommunityReporter()
    
    print("Testing Community Reporter...")
    print("="*70)
    
    # Submit test report
    test_report = {
        'location': 'Test Location',
        'disaster_type': 'Flood',
        'severity': 'Moderate',
        'description': 'Test flood report',
        'affected_count': 50,
        'needs_help': False
    }
    
    report_id = reporter.submit_report(test_report)
    print(f"Submitted report ID: {report_id}")
    
    # Get recent reports
    recent = reporter.get_recent_reports(limit=5)
    print(f"Recent reports: {len(recent)}")
    
    print("="*70)
    print("✅ Test complete!")


if __name__ == "__main__":
    test_reporter()

