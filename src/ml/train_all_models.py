"""
Multi-Disaster ML Model Trainer
Trains Random Forest models for all 5 disaster types
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os
import json

def train_disaster_model(disaster_type, data_path, output_dir):
    """
    Train a Random Forest model for a specific disaster type
    
    Args:
        disaster_type: Name of disaster (flood, earthquake, etc.)
        data_path: Path to CSV data file
        output_dir: Where to save the trained model
    
    Returns:
        Dictionary with training results
    """
    
    print(f"\n{'='*70}")
    print(f" Training {disaster_type.upper()} Model")
    print(f"{'='*70}\n")
    
    # Load data
    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    print(f"✓ Loaded {len(df)} samples with {len(df.columns)} columns")
    
    # Separate features and target
    X = df.drop('risk_level', axis=1)
    y = df['risk_level']
    
    feature_names = list(X.columns)
    print(f"✓ Features: {len(feature_names)}")
    print(f"  {', '.join(feature_names[:5])}{'...' if len(feature_names) > 5 else ''}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"✓ Train: {len(X_train)}, Test: {len(X_test)}")
    
    # Scale features
    print("\nScaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("✓ Features scaled")
    
    # Train Random Forest
    print("\nTraining Random Forest...")
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train_scaled, y_train)
    print("✓ Model trained")
    
    # Evaluate
    print("\nEvaluating model...")
    y_pred_train = model.predict(X_train_scaled)
    y_pred_test = model.predict(X_test_scaled)
    
    train_acc = accuracy_score(y_train, y_pred_train)
    test_acc = accuracy_score(y_test, y_pred_test)
    
    print(f"✓ Train Accuracy: {train_acc*100:.2f}%")
    print(f"✓ Test Accuracy:  {test_acc*100:.2f}%")
    
    # Detailed classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred_test, 
                                target_names=['Safe', 'Warning', 'High Risk', 'Critical']))
    
    # Confusion matrix
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred_test)
    print(cm)
    
    # Feature importance
    importances = model.feature_importances_
    feature_importance = sorted(zip(feature_names, importances), 
                                key=lambda x: x[1], reverse=True)
    
    print("\nTop 5 Most Important Features:")
    for name, importance in feature_importance[:5]:
        print(f"  {name:30s} {importance:.4f}")
    
    # Save model and scaler
    print(f"\nSaving model to {output_dir}...")
    os.makedirs(output_dir, exist_ok=True)
    
    model_path = os.path.join(output_dir, f"{disaster_type}_model.pkl")
    scaler_path = os.path.join(output_dir, f"{disaster_type}_scaler.pkl")
    meta_path = os.path.join(output_dir, f"{disaster_type}_metadata.json")
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    
    # Save metadata
    metadata = {
        'disaster_type': disaster_type,
        'features': feature_names,
        'n_features': len(feature_names),
        'n_samples_train': len(X_train),
        'n_samples_test': len(X_test),
        'train_accuracy': float(train_acc),
        'test_accuracy': float(test_acc),
        'feature_importance': {name: float(imp) for name, imp in feature_importance},
        'risk_levels': {
            0: 'Safe',
            1: 'Warning', 
            2: 'High Risk',
            3: 'Critical'
        }
    }
    
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✓ Model saved: {model_path}")
    print(f"✓ Scaler saved: {scaler_path}")
    print(f"✓ Metadata saved: {meta_path}")
    
    return metadata


def main():
    """Train all disaster models"""
    
    print("\n" + "="*70)
    print(" "*10 + "MULTI-DISASTER ML MODEL TRAINING SYSTEM")
    print("="*70 + "\n")
    
    # Define disasters and their data paths
    disasters = {
        'flood': '../../data/raw_multi_disaster/flood_data.csv',
        'earthquake': '../../data/raw_multi_disaster/earthquake_data.csv',
        'cyclone': '../../data/raw_multi_disaster/cyclone_data.csv',
        'landslide': '../../data/raw_multi_disaster/landslide_data.csv',
        'heatwave': '../../data/raw_multi_disaster/heatwave_data.csv'
    }
    
    output_dir = '../../data/disaster_models'
    
    results = {}
    
    # Train each model
    for disaster_type, data_path in disasters.items():
        try:
            metadata = train_disaster_model(disaster_type, data_path, output_dir)
            results[disaster_type] = metadata
        except Exception as e:
            print(f"\n❌ ERROR training {disaster_type}: {str(e)}")
            continue
    
    # Summary
    print("\n" + "="*70)
    print(" "*20 + "TRAINING SUMMARY")
    print("="*70 + "\n")
    
    print(f"{'Disaster':<15} {'Train Acc':<12} {'Test Acc':<12} {'Features':<10}")
    print("-"*70)
    
    for disaster, meta in results.items():
        print(f"{disaster.capitalize():<15} "
              f"{meta['train_accuracy']*100:>6.2f}%     "
              f"{meta['test_accuracy']*100:>6.2f}%     "
              f"{meta['n_features']:>3}")
    
    print("\n" + "="*70)
    print("✅ ALL MODELS TRAINED SUCCESSFULLY!")
    print("="*70)
    print(f"\nModels saved to: {output_dir}/")
    print("\nFiles created for each disaster:")
    print("  • {disaster}_model.pkl   - Trained Random Forest model")
    print("  • {disaster}_scaler.pkl  - Feature scaler")
    print("  • {disaster}_metadata.json - Model info & feature names")
    print("\nNext step: Update multi_disaster.py to use these trained models")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()