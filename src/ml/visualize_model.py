"""
Model Visualization Module
Creates charts and plots for model performance analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def visualize_model_performance(model, X_test, y_test, output_dir='outputs'):
    """
    Create comprehensive visualizations of model performance
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test labels
        output_dir: Directory to save plots
    """
    print("\n" + "="*70)
    print(" "*15 + "📊 MODEL PERFORMANCE VISUALIZATION")
    print("="*70 + "\n")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)
    
    risk_labels = ['Safe', 'Warning', 'High Risk', 'Critical']
    colors = ['green', 'yellow', 'orange', 'red']
    
    # 1. Confusion Matrix Heatmap
    print("1️⃣  Creating confusion matrix heatmap...")
    fig, ax = plt.subplots(figsize=(10, 8))
    
    cm = confusion_matrix(y_test, y_pred)
    
    # Create custom colormap
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True,
                xticklabels=risk_labels, yticklabels=risk_labels,
                ax=ax, square=True, linewidths=1, linecolor='gray')
    
    ax.set_xlabel('Predicted Label', fontsize=12, fontweight='bold')
    ax.set_ylabel('True Label', fontsize=12, fontweight='bold')
    ax.set_title('Confusion Matrix - Flood Risk Prediction', fontsize=14, fontweight='bold', pad=20)
    
    # Add accuracy on diagonal
    for i in range(len(risk_labels)):
        if cm[i].sum() > 0:
            accuracy = cm[i, i] / cm[i].sum()
            ax.text(i + 0.5, i - 0.3, f'{accuracy*100:.1f}%',
                   ha='center', va='center', fontsize=9, color='darkgreen', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/confusion_matrix.png', dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {output_dir}/confusion_matrix.png")
    plt.close()
    
    # 2. Feature Importance
    print("2️⃣  Creating feature importance chart...")
    
    if hasattr(model, 'feature_importances_'):
        fig, ax = plt.subplots(figsize=(10, 8))
        
        from schema import FEATURE_NAMES
        feature_importance = pd.DataFrame({
            'feature': FEATURE_NAMES,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=True)
        
        colors_importance = plt.cm.viridis(np.linspace(0.3, 0.9, len(feature_importance)))
        
        bars = ax.barh(feature_importance['feature'], feature_importance['importance'], 
                      color=colors_importance, edgecolor='black', linewidth=0.5)
        
        ax.set_xlabel('Importance Score', fontsize=12, fontweight='bold')
        ax.set_ylabel('Features', fontsize=12, fontweight='bold')
        ax.set_title('Feature Importance for Flood Prediction', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2,
                   f'{width:.4f}',
                   ha='left', va='center', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/feature_importance.png', dpi=300, bbox_inches='tight')
        print(f"   ✅ Saved: {output_dir}/feature_importance.png")
        plt.close()
    
    # 3. Per-Class Performance
    print("3️⃣  Creating per-class performance chart...")
    
    from sklearn.metrics import precision_score, recall_score, f1_score
    
    precision = precision_score(y_test, y_pred, average=None, zero_division=0)
    recall = recall_score(y_test, y_pred, average=None, zero_division=0)
    f1 = f1_score(y_test, y_pred, average=None, zero_division=0)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(risk_labels))
    width = 0.25
    
    bars1 = ax.bar(x - width, precision, width, label='Precision', color='skyblue', edgecolor='black')
    bars2 = ax.bar(x, recall, width, label='Recall', color='lightcoral', edgecolor='black')
    bars3 = ax.bar(x + width, f1, width, label='F1-Score', color='lightgreen', edgecolor='black')
    
    ax.set_xlabel('Risk Level', fontsize=12, fontweight='bold')
    ax.set_ylabel('Score', fontsize=12, fontweight='bold')
    ax.set_title('Per-Class Performance Metrics', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(risk_labels)
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, 1.1)
    
    # Add value labels
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}',
                   ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/per_class_performance.png', dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {output_dir}/per_class_performance.png")
    plt.close()
    
    # 4. Prediction Confidence Distribution
    print("4️⃣  Creating prediction confidence distribution...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, (ax, label) in enumerate(zip(axes, risk_labels)):
        # Get max probability for each prediction
        class_mask = y_pred == idx
        if class_mask.sum() > 0:
            confidences = y_pred_proba[class_mask, idx]
            
            ax.hist(confidences, bins=20, color=colors[idx], alpha=0.7, edgecolor='black')
            ax.axvline(confidences.mean(), color='red', linestyle='--', linewidth=2, 
                      label=f'Mean: {confidences.mean():.3f}')
            
            ax.set_xlabel('Prediction Confidence', fontsize=10, fontweight='bold')
            ax.set_ylabel('Frequency', fontsize=10, fontweight='bold')
            ax.set_title(f'{label} Predictions Confidence', fontsize=11, fontweight='bold')
            ax.legend()
            ax.grid(alpha=0.3)
        else:
            ax.text(0.5, 0.5, 'No predictions\nfor this class', 
                   ha='center', va='center', fontsize=12)
            ax.set_title(f'{label} Predictions Confidence', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/prediction_confidence.png', dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {output_dir}/prediction_confidence.png")
    plt.close()
    
    # 5. Model Performance Summary
    print("5️⃣  Creating performance summary chart...")
    
    from sklearn.metrics import accuracy_score
    
    accuracy = accuracy_score(y_test, y_pred)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    metrics = {
        'Overall\nAccuracy': accuracy,
        'Precision\n(Safe)': precision[0],
        'Precision\n(Warning)': precision[1],
        'Precision\n(High Risk)': precision[2],
        'Precision\n(Critical)': precision[3],
        'Recall\n(Critical)': recall[3]  # Most important!
    }
    
    bars = ax.bar(metrics.keys(), metrics.values(), 
                  color=['blue', 'green', 'yellow', 'orange', 'red', 'darkred'],
                  alpha=0.7, edgecolor='black', linewidth=1.5)
    
    ax.set_ylabel('Score', fontsize=12, fontweight='bold')
    ax.set_title('Model Performance Summary', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 1.1)
    ax.axhline(0.85, color='green', linestyle='--', linewidth=2, alpha=0.5, label='Target: 85%')
    ax.grid(axis='y', alpha=0.3)
    ax.legend()
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        color = 'green' if height >= 0.85 else 'red'
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.3f}',
               ha='center', va='bottom', fontsize=10, fontweight='bold', color=color)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/performance_summary.png', dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {output_dir}/performance_summary.png")
    plt.close()
    
    # 6. Actual vs Predicted
    print("6️⃣  Creating actual vs predicted scatter...")
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Add jitter for better visualization
    jitter = 0.1
    y_test_jittered = y_test + np.random.uniform(-jitter, jitter, len(y_test))
    y_pred_jittered = y_pred + np.random.uniform(-jitter, jitter, len(y_pred))
    
    # Color by whether prediction was correct
    correct = y_test == y_pred
    
    ax.scatter(y_test_jittered[correct], y_pred_jittered[correct], 
              c='green', alpha=0.6, s=50, label='Correct', edgecolors='black', linewidth=0.5)
    ax.scatter(y_test_jittered[~correct], y_pred_jittered[~correct], 
              c='red', alpha=0.6, s=50, label='Incorrect', edgecolors='black', linewidth=0.5)
    
    # Perfect prediction line
    ax.plot([0, 3], [0, 3], 'k--', linewidth=2, label='Perfect Prediction')
    
    ax.set_xlabel('True Risk Level', fontsize=12, fontweight='bold')
    ax.set_ylabel('Predicted Risk Level', fontsize=12, fontweight='bold')
    ax.set_title('Actual vs Predicted Risk Levels', fontsize=14, fontweight='bold')
    ax.set_xticks([0, 1, 2, 3])
    ax.set_yticks([0, 1, 2, 3])
    ax.set_xticklabels(risk_labels, rotation=45)
    ax.set_yticklabels(risk_labels)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/actual_vs_predicted.png', dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {output_dir}/actual_vs_predicted.png")
    plt.close()
    
    print("\n" + "="*70)
    print("✅ All visualizations created successfully!")
    print(f"📁 Saved in: {output_dir}/")
    print("="*70 + "\n")


if __name__ == "__main__":
    # Load model and data for visualization
    import joblib
    from data_loader import load_preprocessed_data
    
    # Determine paths
    if os.path.exists('data'):
        model_path = "data/models/flood_model.pkl"
        output_dir = "outputs"
    else:
        model_path = "../../data/models/flood_model.pkl"
        output_dir = "../../outputs"
    
    model = joblib.load(model_path)
    data = load_preprocessed_data()
    
    visualize_model_performance(model, data['X_test'], data['y_test'], output_dir)