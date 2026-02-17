"""
Preprocessing Visualization Script
Shows the effect of data normalization and preprocessing
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def visualize_preprocessing(raw_path: str, processed_dir: str, output_dir: str = "outputs"):
    """
    Create visualizations showing before/after preprocessing
    
    Args:
        raw_path: Path to raw data CSV
        processed_dir: Directory with processed data
        output_dir: Directory to save plots
    """
    print("\n" + "="*70)
    print(" "*15 + "📊 PREPROCESSING VISUALIZATION")
    print("="*70 + "\n")
    
    # Load raw and processed data
    print("📂 Loading raw data...")
    raw_df = pd.read_csv(raw_path)
    
    print("📂 Loading processed data...")
    train_df = pd.read_csv(os.path.join(processed_dir, 'train.csv'))
    test_df = pd.read_csv(os.path.join(processed_dir, 'test.csv'))
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    from schema import FEATURE_NAMES
    
    # 1. Compare distributions before/after normalization
    print("\n1️⃣  Creating normalization comparison...")
    
    # Select 4 key features to visualize
    key_features = ['rainfall_mm', 'river_level_m', 'soil_moisture_percent', 'elevation_m']
    
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    
    for idx, feature in enumerate(key_features):
        # Before normalization (raw data)
        ax_before = axes[0, idx]
        raw_df[feature].hist(bins=30, ax=ax_before, color='steelblue', alpha=0.7, edgecolor='black')
        ax_before.set_title(f'{feature.replace("_", " ").title()}\n(Before)', fontsize=10, fontweight='bold')
        ax_before.set_xlabel('Value', fontsize=9)
        ax_before.set_ylabel('Frequency', fontsize=9)
        ax_before.grid(alpha=0.3)
        
        # After normalization (processed data)
        ax_after = axes[1, idx]
        train_df[feature].hist(bins=30, ax=ax_after, color='coral', alpha=0.7, edgecolor='black')
        ax_after.set_title(f'{feature.replace("_", " ").title()}\n(After Normalization)', fontsize=10, fontweight='bold')
        ax_after.set_xlabel('Normalized Value', fontsize=9)
        ax_after.set_ylabel('Frequency', fontsize=9)
        ax_after.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/normalization_effect.png', dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {output_dir}/normalization_effect.png")
    plt.close()
    
    # 2. Train-Test split visualization
    print("2️⃣  Creating train-test split visualization...")
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Risk distribution in train set
    ax1 = axes[0]
    train_risk = train_df['flood_risk'].value_counts().sort_index()
    risk_labels = {0: 'Safe', 1: 'Warning', 2: 'High Risk', 3: 'Critical'}
    colors = ['green', 'yellow', 'orange', 'red']
    
    bars1 = ax1.bar([risk_labels[i] for i in train_risk.index], train_risk.values, color=colors, alpha=0.7, edgecolor='black')
    ax1.set_title('Training Set Risk Distribution', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Risk Level', fontsize=10)
    ax1.set_ylabel('Count', fontsize=10)
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Risk distribution in test set
    ax2 = axes[1]
    test_risk = test_df['flood_risk'].value_counts().sort_index()
    
    bars2 = ax2.bar([risk_labels[i] for i in test_risk.index], test_risk.values, color=colors, alpha=0.7, edgecolor='black')
    ax2.set_title('Test Set Risk Distribution', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Risk Level', fontsize=10)
    ax2.set_ylabel('Count', fontsize=10)
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/train_test_split.png', dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {output_dir}/train_test_split.png")
    plt.close()
    
    # 3. Feature scaling comparison
    print("3️⃣  Creating feature scaling comparison...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Before scaling - show raw feature ranges
    ax1 = axes[0]
    feature_stats_raw = []
    for feature in key_features:
        feature_stats_raw.append({
            'feature': feature.replace('_', '\n'),
            'min': raw_df[feature].min(),
            'max': raw_df[feature].max(),
            'mean': raw_df[feature].mean()
        })
    
    positions = range(len(key_features))
    ax1.scatter(positions, [s['mean'] for s in feature_stats_raw], s=100, c='blue', alpha=0.6, label='Mean')
    ax1.errorbar(positions, 
                [s['mean'] for s in feature_stats_raw],
                yerr=[[s['mean']-s['min'] for s in feature_stats_raw],
                      [s['max']-s['mean'] for s in feature_stats_raw]],
                fmt='none', c='blue', alpha=0.3)
    
    ax1.set_xticks(positions)
    ax1.set_xticklabels([s['feature'] for s in feature_stats_raw], fontsize=9)
    ax1.set_ylabel('Value Range', fontsize=10, fontweight='bold')
    ax1.set_title('Raw Feature Scales (Before)', fontsize=12, fontweight='bold')
    ax1.grid(alpha=0.3)
    ax1.legend()
    
    # After scaling - normalized features
    ax2 = axes[1]
    feature_stats_norm = []
    for feature in key_features:
        feature_stats_norm.append({
            'feature': feature.replace('_', '\n'),
            'min': train_df[feature].min(),
            'max': train_df[feature].max(),
            'mean': train_df[feature].mean()
        })
    
    ax2.scatter(positions, [s['mean'] for s in feature_stats_norm], s=100, c='red', alpha=0.6, label='Mean')
    ax2.errorbar(positions,
                [s['mean'] for s in feature_stats_norm],
                yerr=[[s['mean']-s['min'] for s in feature_stats_norm],
                      [s['max']-s['mean'] for s in feature_stats_norm]],
                fmt='none', c='red', alpha=0.3)
    
    ax2.set_xticks(positions)
    ax2.set_xticklabels([s['feature'] for s in feature_stats_norm], fontsize=9)
    ax2.set_ylabel('Normalized Value Range', fontsize=10, fontweight='bold')
    ax2.set_title('Normalized Feature Scales (After)', fontsize=12, fontweight='bold')
    ax2.grid(alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/feature_scaling.png', dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {output_dir}/feature_scaling.png")
    plt.close()
    
    # Print summary statistics
    print("\n" + "="*70)
    print("📊 PREPROCESSING STATISTICS SUMMARY")
    print("="*70)
    
    print(f"\n📈 Dataset Sizes:")
    print(f"   Original dataset: {len(raw_df)} samples")
    print(f"   Training set:     {len(train_df)} samples ({len(train_df)/len(raw_df)*100:.1f}%)")
    print(f"   Test set:         {len(test_df)} samples ({len(test_df)/len(raw_df)*100:.1f}%)")
    
    print(f"\n📏 Feature Scale Changes:")
    for feature in key_features:
        raw_range = raw_df[feature].max() - raw_df[feature].min()
        norm_range = train_df[feature].max() - train_df[feature].min()
        print(f"   {feature:25s}: {raw_range:8.2f} → {norm_range:6.2f} (normalized)")
    
    print(f"\n🎯 Class Balance Maintained:")
    for level in [0, 1, 2, 3]:
        raw_pct = (raw_df['flood_risk'] == level).sum() / len(raw_df) * 100
        train_pct = (train_df['flood_risk'] == level).sum() / len(train_df) * 100
        test_pct = (test_df['flood_risk'] == level).sum() / len(test_df) * 100
        print(f"   Level {level}: Raw {raw_pct:5.1f}% | Train {train_pct:5.1f}% | Test {test_pct:5.1f}%")
    
    print("\n" + "="*70)
    print("✅ Visualization complete!")
    print(f"📁 Saved in: {output_dir}/")
    print("="*70 + "\n")


if __name__ == "__main__":
    # Determine paths
    if os.path.exists('data'):
        raw_path = "data/raw/flood_data.csv"
        processed_dir = "data/processed"
        output_dir = "outputs"
    else:
        raw_path = "../../data/raw/flood_data.csv"
        processed_dir = "../../data/processed"
        output_dir = "../../outputs"
    
    visualize_preprocessing(raw_path, processed_dir, output_dir)