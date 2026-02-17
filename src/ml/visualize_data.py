"""
Data Visualization Script
Creates charts and plots for exploratory data analysis and presentation
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def create_visualizations(filepath: str, output_dir: str = "outputs"):
    """
    Create comprehensive visualizations of the flood dataset
    
    Args:
        filepath: Path to the CSV dataset
        output_dir: Directory to save plots
    """
    print("\n" + "="*70)
    print(" "*20 + "📊 DATA VISUALIZATION")
    print("="*70 + "\n")
    
    # Load dataset
    print("📂 Loading dataset...")
    df = pd.read_csv(filepath)
    print(f"✅ Loaded {len(df)} samples\n")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    risk_labels = {0: 'Safe', 1: 'Warning', 2: 'High Risk', 3: 'Critical'}
    colors = ['green', 'yellow', 'orange', 'red']
    
    # 1. Risk Level Distribution
    print("1️⃣  Creating risk level distribution plot...")
    fig, ax = plt.subplots(figsize=(10, 6))
    risk_counts = df['flood_risk'].value_counts().sort_index()
    bars = ax.bar(
        [risk_labels[i] for i in risk_counts.index], 
        risk_counts.values,
        color=colors
    )
    ax.set_xlabel('Risk Level', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Samples', fontsize=12, fontweight='bold')
    ax.set_title('Flood Risk Level Distribution', fontsize=14, fontweight='bold')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/risk_distribution.png', dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {output_dir}/risk_distribution.png")
    plt.close()
    
    # 2. Feature Distributions by Risk Level
    print("2️⃣  Creating feature distribution plots...")
    key_features = ['rainfall_mm', 'river_level_m', 'soil_moisture_percent', 'elevation_m']
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, feature in enumerate(key_features):
        ax = axes[idx]
        for risk_level in [0, 1, 2, 3]:
            data = df[df['flood_risk'] == risk_level][feature]
            ax.hist(data, alpha=0.5, label=risk_labels[risk_level], 
                   color=colors[risk_level], bins=20)
        
        ax.set_xlabel(feature.replace('_', ' ').title(), fontsize=10, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=10, fontweight='bold')
        ax.set_title(f'{feature.replace("_", " ").title()} by Risk Level', 
                    fontsize=11, fontweight='bold')
        ax.legend()
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/feature_distributions.png', dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {output_dir}/feature_distributions.png")
    plt.close()
    
    # 3. Correlation Heatmap
    print("3️⃣  Creating correlation heatmap...")
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Select numeric columns only
    numeric_cols = ['rainfall_mm', 'rainfall_7day_avg', 'rainfall_intensity',
                   'river_level_m', 'river_level_change', 'soil_moisture_percent',
                   'elevation_m', 'temperature_celsius', 'humidity_percent',
                   'wind_speed_kmh', 'distance_to_river_km', 'month', 'flood_risk']
    
    correlation = df[numeric_cols].corr()
    
    sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', 
               center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8},
               ax=ax)
    ax.set_title('Feature Correlation Heatmap', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/correlation_heatmap.png', dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {output_dir}/correlation_heatmap.png")
    plt.close()
    
    # 4. Box Plots - Key Features vs Risk
    print("4️⃣  Creating box plots...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, feature in enumerate(key_features):
        ax = axes[idx]
        df_plot = df.copy()
        df_plot['risk_label'] = df_plot['flood_risk'].map(risk_labels)
        
        box_parts = ax.boxplot(
            [df_plot[df_plot['flood_risk'] == i][feature].values for i in [0, 1, 2, 3]],
            labels=[risk_labels[i] for i in [0, 1, 2, 3]],
            patch_artist=True
        )
        
        # Color the boxes
        for patch, color in zip(box_parts['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)
        
        ax.set_xlabel('Risk Level', fontsize=10, fontweight='bold')
        ax.set_ylabel(feature.replace('_', ' ').title(), fontsize=10, fontweight='bold')
        ax.set_title(f'{feature.replace("_", " ").title()} Distribution by Risk', 
                    fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/box_plots.png', dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {output_dir}/box_plots.png")
    plt.close()
    
    # 5. Scatter Plot - Rainfall vs River Level colored by Risk
    print("5️⃣  Creating scatter plot...")
    fig, ax = plt.subplots(figsize=(10, 8))
    
    for risk_level in [0, 1, 2, 3]:
        data = df[df['flood_risk'] == risk_level]
        ax.scatter(data['rainfall_mm'], data['river_level_m'], 
                  c=colors[risk_level], label=risk_labels[risk_level],
                  alpha=0.6, s=50)
    
    ax.set_xlabel('Rainfall (mm)', fontsize=12, fontweight='bold')
    ax.set_ylabel('River Level (m)', fontsize=12, fontweight='bold')
    ax.set_title('Rainfall vs River Level by Risk Level', fontsize=14, fontweight='bold')
    ax.legend(title='Risk Level', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/rainfall_vs_river.png', dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {output_dir}/rainfall_vs_river.png")
    plt.close()
    
    # 6. Monthly Risk Distribution
    print("6️⃣  Creating monthly risk distribution...")
    fig, ax = plt.subplots(figsize=(12, 6))
    
    month_risk = pd.crosstab(df['month'], df['flood_risk'], normalize='index') * 100
    month_risk.plot(kind='bar', stacked=True, ax=ax, color=colors, width=0.8)
    
    ax.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
    ax.set_title('Monthly Flood Risk Distribution', fontsize=14, fontweight='bold')
    ax.legend(title='Risk Level', labels=[risk_labels[i] for i in [0, 1, 2, 3]])
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/monthly_distribution.png', dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {output_dir}/monthly_distribution.png")
    plt.close()
    
    # Summary Statistics
    print("\n7️⃣  Generating summary statistics...")
    summary = df.groupby('flood_risk').agg({
        'rainfall_mm': 'mean',
        'river_level_m': 'mean',
        'soil_moisture_percent': 'mean',
        'elevation_m': 'mean'
    }).round(2)
    
    summary.index = [risk_labels[i] for i in summary.index]
    
    print("\n📊 Average Feature Values by Risk Level:")
    print(summary.to_string())
    
    print("\n" + "="*70)
    print("✅ All visualizations created successfully!")
    print(f"📁 Saved in: {output_dir}/")
    print("="*70 + "\n")


if __name__ == "__main__":
    # Determine the correct path
    if os.path.exists('data'):
        filepath = "data/raw/flood_data.csv"
        output_dir = "outputs"
    else:
        filepath = "../../data/raw/flood_data.csv"
        output_dir = "../../outputs"
    
    create_visualizations(filepath, output_dir)