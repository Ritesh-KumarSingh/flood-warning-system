"""
Data Loader Module
Helper functions to load preprocessed data for model training
"""

import pandas as pd
import joblib
import os
import json

def load_preprocessed_data(data_dir: str = "../../data/processed"):
    """
    Load preprocessed train and test datasets
    
    Args:
        data_dir: Directory containing processed data files
        
    Returns:
        Dictionary with X_train, X_test, y_train, y_test, scaler, metadata
    """
    print(f"📂 Loading preprocessed data from {data_dir}...")
    
    # Load training data
    train_path = os.path.join(data_dir, 'train.csv')
    if not os.path.exists(train_path):
        raise FileNotFoundError(f"Training data not found at {train_path}")
    
    train_df = pd.read_csv(train_path)
    print(f"✅ Loaded training data: {train_df.shape}")
    
    # Load test data
    test_path = os.path.join(data_dir, 'test.csv')
    if not os.path.exists(test_path):
        raise FileNotFoundError(f"Test data not found at {test_path}")
    
    test_df = pd.read_csv(test_path)
    print(f"✅ Loaded test data: {test_df.shape}")
    
    # Load scaler
    scaler_path = os.path.join(data_dir, 'scaler.pkl')
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler not found at {scaler_path}")
    
    scaler = joblib.load(scaler_path)
    print(f"✅ Loaded scaler")
    
    # Load metadata
    metadata_path = os.path.join(data_dir, 'preprocessing_metadata.json')
    metadata = None
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        print(f"✅ Loaded metadata")
    
    # Split features and target
    from schema import FEATURE_NAMES, TARGET_NAME
    
    X_train = train_df[FEATURE_NAMES]
    y_train = train_df[TARGET_NAME]
    
    X_test = test_df[FEATURE_NAMES]
    y_test = test_df[TARGET_NAME]
    
    print(f"\n📊 Data Summary:")
    print(f"   Features: {len(FEATURE_NAMES)}")
    print(f"   Training samples: {len(X_train)}")
    print(f"   Test samples: {len(X_test)}")
    print(f"   Target classes: {sorted(y_train.unique())}")
    
    return {
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'scaler': scaler,
        'metadata': metadata
    }


def load_scaler(data_dir: str = "../../data/processed"):
    """Load just the scaler for new predictions"""
    scaler_path = os.path.join(data_dir, 'scaler.pkl')
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler not found at {scaler_path}")
    return joblib.load(scaler_path)


def display_data_info(data: dict):
    """Display information about loaded data"""
    print("\n" + "="*70)
    print(" "*20 + "LOADED DATA INFORMATION")
    print("="*70)
    
    X_train = data['X_train']
    y_train = data['y_train']
    X_test = data['X_test']
    y_test = data['y_test']
    
    print(f"\n📊 Dataset Shapes:")
    print(f"   X_train: {X_train.shape}")
    print(f"   y_train: {y_train.shape}")
    print(f"   X_test:  {X_test.shape}")
    print(f"   y_test:  {y_test.shape}")
    
    print(f"\n🎯 Target Distribution:")
    risk_labels = {0: 'Safe', 1: 'Warning', 2: 'High Risk', 3: 'Critical'}
    
    print("\n   Training Set:")
    for level, count in y_train.value_counts().sort_index().items():
        percentage = (count / len(y_train)) * 100
        print(f"   Level {level} ({risk_labels[level]:10s}): {count:4d} ({percentage:5.1f}%)")
    
    print("\n   Test Set:")
    for level, count in y_test.value_counts().sort_index().items():
        percentage = (count / len(y_test)) * 100
        print(f"   Level {level} ({risk_labels[level]:10s}): {count:4d} ({percentage:5.1f}%)")
    
    print(f"\n📏 Feature Statistics (Training Set):")
    print(f"   Mean: {X_train.mean().mean():.4f}")
    print(f"   Std:  {X_train.std().mean():.4f}")
    print(f"   Min:  {X_train.min().min():.4f}")
    print(f"   Max:  {X_train.max().max():.4f}")
    
    if data['metadata']:
        print(f"\n📝 Metadata:")
        print(f"   Feature count: {data['metadata']['n_features']}")
        print(f"   Features: {', '.join(data['metadata']['feature_names'][:3])}...")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    # Test the data loader
    data = load_preprocessed_data()
    display_data_info(data)