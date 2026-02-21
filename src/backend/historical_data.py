"""
Historical Disaster Data Viewer
Shows past disaster trends, seasonal patterns, and risk history
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit as st
import numpy as np

class HistoricalDataAnalyzer:
    """Analyze and display historical disaster data"""
    
    def __init__(self):
        # Sample historical disaster data for Indian cities
        # In production, this would come from a database
        self.historical_data = self._generate_sample_history()
    
    def _generate_sample_history(self):
        """Generate sample historical disaster data"""
        # Last 5 years of data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365*5)
        
        data = []
        
        # Major cities
        cities = ['Delhi', 'Mumbai', 'Kolkata', 'Chennai', 'Bangalore']
        disasters = ['Flood', 'Earthquake', 'Cyclone', 'Landslide', 'Heatwave']
        
        # Generate historical events
        current_date = start_date
        while current_date <= end_date:
            # Random disasters throughout the year
            if np.random.random() < 0.05:  # 5% chance each day
                city = np.random.choice(cities)
                disaster = np.random.choice(disasters, p=[0.3, 0.15, 0.15, 0.2, 0.2])
                risk_level = np.random.choice([1, 2, 3], p=[0.5, 0.35, 0.15])
                
                data.append({
                    'date': current_date,
                    'city': city,
                    'disaster_type': disaster,
                    'risk_level': risk_level,
                    'affected_people': np.random.randint(100, 10000),
                    'severity': ['Warning', 'High Risk', 'Critical'][risk_level-1]
                })
            
            current_date += timedelta(days=1)
        
        return pd.DataFrame(data)
    
    def get_city_history(self, city: str, disaster_type: str = None):
        """Get historical data for a specific city"""
        df = self.historical_data.copy()
        
        # Filter by city (case insensitive)
        df = df[df['city'].str.lower() == city.lower()]
        
        # Filter by disaster type if specified
        if disaster_type:
            df = df[df['disaster_type'].str.lower() == disaster_type.lower()]
        
        return df
    
    def get_seasonal_pattern(self, city: str, disaster_type: str):
        """Analyze seasonal patterns"""
        df = self.get_city_history(city, disaster_type)
        
        if len(df) == 0:
            return None
        
        df['month'] = df['date'].dt.month
        monthly_counts = df.groupby('month').size().reindex(range(1, 13), fill_value=0)
        
        return monthly_counts
    
    def get_statistics(self, city: str, disaster_type: str = None):
        """Get summary statistics"""
        df = self.get_city_history(city, disaster_type)
        
        if len(df) == 0:
            return {
                'total_events': 0,
                'avg_risk_level': 0,
                'most_common_month': 'N/A',
                'last_event': 'No records'
            }
        
        return {
            'total_events': len(df),
            'avg_risk_level': df['risk_level'].mean(),
            'most_common_month': df['date'].dt.month.mode()[0] if len(df) > 0 else 'N/A',
            'last_event': df['date'].max().strftime('%d %b %Y'),
            'total_affected': df['affected_people'].sum(),
            'critical_events': len(df[df['risk_level'] == 3])
        }
    
    def display_history(self, city: str, disaster_type: str = None):
        """Display historical data in Streamlit"""
        
        st.markdown("### 📊 Historical Disaster Data")
        
        df = self.get_city_history(city, disaster_type)
        
        if len(df) == 0:
            st.info(f"No historical data available for {city}" + 
                   (f" - {disaster_type}" if disaster_type else ""))
            return
        
        # Summary statistics
        stats = self.get_statistics(city, disaster_type)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Events (5 years)", stats['total_events'])
        
        with col2:
            st.metric("Avg Risk Level", f"{stats['avg_risk_level']:.1f}/3")
        
        with col3:
            st.metric("Critical Events", stats['critical_events'])
        
        with col4:
            st.metric("Last Event", stats['last_event'])
        
        # Timeline chart
        st.markdown("#### 📈 Event Timeline")
        
        df_sorted = df.sort_values('date')
        
        fig = px.scatter(df_sorted, 
                        x='date', 
                        y='disaster_type',
                        color='severity',
                        size='affected_people',
                        color_discrete_map={
                            'Warning': '#ffc107',
                            'High Risk': '#fd7e14',
                            'Critical': '#dc3545'
                        },
                        title=f"Disaster Events in {city}")
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Seasonal pattern
        if disaster_type:
            st.markdown(f"#### 📅 Seasonal Pattern - {disaster_type}")
            
            monthly = self.get_seasonal_pattern(city, disaster_type)
            
            if monthly is not None:
                month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                
                fig2 = go.Figure(data=[
                    go.Bar(x=month_names, y=monthly.values,
                          marker_color='#1f77b4')
                ])
                
                fig2.update_layout(
                    title=f"{disaster_type} Frequency by Month",
                    xaxis_title="Month",
                    yaxis_title="Number of Events",
                    height=350
                )
                
                st.plotly_chart(fig2, use_container_width=True)
                
                # Peak months
                peak_month = monthly.idxmax()
                st.info(f"📊 Peak activity: **{month_names[peak_month-1]}** " +
                       f"({monthly.max()} events)")
        
        # Recent events table
        st.markdown("#### 📋 Recent Events")
        
        recent = df.sort_values('date', ascending=False).head(10)
        
        display_df = recent[['date', 'disaster_type', 'severity', 'affected_people']].copy()
        display_df['date'] = display_df['date'].dt.strftime('%d %b %Y')
        display_df.columns = ['Date', 'Disaster', 'Severity', 'Affected People']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Risk trends
        st.markdown("#### 📉 Risk Level Trends")
        
        df['year_month'] = df['date'].dt.to_period('M').astype(str)
        monthly_risk = df.groupby('year_month')['risk_level'].mean().tail(12)
        
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=list(range(len(monthly_risk))),
            y=monthly_risk.values,
            mode='lines+markers',
            name='Avg Risk Level',
            line=dict(color='#ff6f00', width=3)
        ))
        
        fig3.add_hline(y=2, line_dash="dash", line_color="red", 
                      annotation_text="High Risk Threshold")
        
        fig3.update_layout(
            title="Average Risk Level (Last 12 Months)",
            xaxis_title="Month",
            yaxis_title="Risk Level",
            height=300,
            yaxis_range=[0, 3]
        )
        
        st.plotly_chart(fig3, use_container_width=True)


# Quick test
def test_historical():
    """Test historical data analyzer"""
    analyzer = HistoricalDataAnalyzer()
    
    print("Testing Historical Data Analyzer...")
    print("="*70)
    
    stats = analyzer.get_statistics('Delhi', 'Flood')
    print(f"\nDelhi Flood Statistics:")
    print(f"  Total Events: {stats['total_events']}")
    print(f"  Avg Risk: {stats['avg_risk_level']:.2f}")
    print(f"  Last Event: {stats['last_event']}")
    
    print("\n" + "="*70)
    print("✅ Test complete!")


if __name__ == "__main__":
    test_historical()

