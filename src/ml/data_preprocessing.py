"""
Data Preprocessing Module
Cleans and transforms raw flood data for ML training
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os
from schema import FEATURE_NAMES, TARGET_NAME, FEATURE_RANGES

class FloodDataPreprocessor:
    """Handles all data preprocessing for flood prediction"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_names = FEATURE_NAMES
        self.target_name = TARGET_NAME
        
    def load_data(self, filepath: str) -> pd.DataFrame:
        """Load raw dataset from CSV"""
        print(f"📂 Loading data from {filepath}...")
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Dataset not found at {filepath}")
        
        df = pd.read_csv(filepath)
        print(f"✅ Loaded {len(df)} samples with {len(df.columns)} columns")
        
        return df
    
    def check_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Check and handle missing values"""
        print("\n🔍 Checking for missing values...")
        
        missing = df.isnull().sum()
        
        if missing.sum() == 0:
            print("✅ No missing values found")
            return df
        
        print("⚠️  Missing values detected:")
        for col, count in missing[missing > 0].items():
            percentage = (count / len(df)) * 100
            print(f"   {col}: {count} ({percentage:.2f}%)")
        
        # Strategy: Drop rows with missing critical features
        critical_features = ['rainfall_mm', 'river_level_m', TARGET_NAME]
        df_clean = df.dropna(subset=critical_features)
        
        # Fill remaining missing values with median
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                if col in FEATURE_NAMES:
                    median_value = df[col].median()
                    df_clean[col].fillna(median_value, inplace=True)
                    print(f"   Filled {col} with median: {median_value:.2f}")
        
        dropped = len(df) - len(df_clean)
        if dropped > 0:
            print(f"⚠️  Dropped {dropped} rows with critical missing values")
        
        return df_clean
    
    def validate_ranges(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate and clip feature values to expected ranges"""
        print("\n📏 Validating feature ranges...")
        
        clipped_count = 0
        
        for feature, (min_val, max_val) in FEATURE_RANGES.items():
            if feature in df.columns:
                # Check for out-of-range values
                out_of_range = ((df[feature] < min_val) | (df[feature] > max_val)).sum()
                
                if out_of_range > 0:
                    print(f"   ⚠️  {feature}: {out_of_range} values out of range [{min_val}, {max_val}]")
                    # Clip to valid range
                    df[feature] = df[feature].clip(min_val, max_val)
                    clipped_count += out_of_range
        
        if clipped_count == 0:
            print("✅ All values within expected ranges")
        else:
            print(f"⚠️  Clipped {clipped_count} values to valid ranges")
        
        return df
    
    def normalize_features(self, X_train: pd.DataFrame, X_test: pd.DataFrame = None):
        """Normalize features using StandardScaler"""
        print("\n🔧 Normalizing features...")
        
        # Fit scaler on training data
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
        
        print("✅ Training data normalized")
        print(f"   Mean: {X_train_scaled.mean().mean():.4f}")
        print(f"   Std:  {X_train_scaled.std().mean():.4f}")
        
        if X_test is not None:
            # Transform test data using same scaler
            X_test_scaled = self.scaler.transform(X_test)
            X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)
            print("✅ Test data normalized with same scaler")
            return X_train_scaled, X_test_scaled
        
        return X_train_scaled
    
    def split_features_target(self, df: pd.DataFrame):
        """Separate features (X) and target (y)"""
        print("\n✂️  Splitting features and target...")
        
        X = df[self.feature_names]
        y = df[self.target_name]
        
        print(f"✅ Features shape: {X.shape}")
        print(f"✅ Target shape: {y.shape}")
        print(f"\n   Target distribution:")
        
        risk_labels = {0: 'Safe', 1: 'Warning', 2: 'High Risk', 3: 'Critical'}
        for level, count in y.value_counts().sort_index().items():
            percentage = (count / len(y)) * 100
            print(f"   Level {level} ({risk_labels[level]:10s}): {count:4d} ({percentage:5.1f}%)")
        
        return X, y
    
    def split_train_test(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2, random_state: int = 42):
        """Split data into train and test sets with stratification"""
        print(f"\n🔀 Splitting data (train: {int((1-test_size)*100)}%, test: {int(test_size*100)}%)...")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=test_size, 
            random_state=random_state,
            stratify=y  # Maintain class distribution
        )
        
        print(f"✅ Training set: {len(X_train)} samples")
        print(f"✅ Test set: {len(X_test)} samples")
        
        # Verify stratification
        print("\n   Class distribution in train set:")
        risk_labels = {0: 'Safe', 1: 'Warning', 2: 'High Risk', 3: 'Critical'}
        for level, count in y_train.value_counts().sort_index().items():
            percentage = (count / len(y_train)) * 100
            print(f"   Level {level} ({risk_labels[level]:10s}): {count:4d} ({percentage:5.1f}%)")
        
        return X_train, X_test, y_train, y_test
    
    def save_processed_data(self, X_train, X_test, y_train, y_test, output_dir: str):
        """Save processed datasets and scaler"""
        print(f"\n💾 Saving processed data to {output_dir}...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Save train data
        train_data = X_train.copy()
        train_data[self.target_name] = y_train
        train_path = os.path.join(output_dir, 'train.csv')
        train_data.to_csv(train_path, index=False)
        print(f"✅ Saved training set: {train_path}")
        
        # Save test data
        test_data = X_test.copy()
        test_data[self.target_name] = y_test
        test_path = os.path.join(output_dir, 'test.csv')
        test_data.to_csv(test_path, index=False)
        print(f"✅ Saved test set: {test_path}")
        
        # Save scaler
        scaler_path = os.path.join(output_dir, 'scaler.pkl')
        joblib.dump(self.scaler, scaler_path)
        print(f"✅ Saved scaler: {scaler_path}")
        
        # Save preprocessing metadata
        metadata = {
            'feature_names': self.feature_names,
            'target_name': self.target_name,
            'n_features': len(self.feature_names),
            'n_train_samples': len(X_train),
            'n_test_samples': len(X_test),
            'scaler_mean': self.scaler.mean_.tolist(),
            'scaler_std': self.scaler.scale_.tolist()
        }
        
        import json
        metadata_path = os.path.join(output_dir, 'preprocessing_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✅ Saved metadata: {metadata_path}")
        
        return train_path, test_path, scaler_path
    
    def preprocess_pipeline(self, input_path: str, output_dir: str, test_size: float = 0.2):
        """Complete preprocessing pipeline"""
        print("\n" + "="*70)
        print(" "*20 + "🔧 DATA PREPROCESSING PIPELINE")
        print("="*70)
        
        # Step 1: Load data
        df = self.load_data(input_path)
        
        # Step 2: Check missing values
        df = self.check_missing_values(df)
        
        # Step 3: Validate ranges
        df = self.validate_ranges(df)
        
        # Step 4: Split features and target
        X, y = self.split_features_target(df)
        
        # Step 5: Split train/test
        X_train, X_test, y_train, y_test = self.split_train_test(X, y, test_size)
        
        # Step 6: Normalize features
        X_train_scaled, X_test_scaled = self.normalize_features(X_train, X_test)
        
        # Step 7: Save processed data
        train_path, test_path, scaler_path = self.save_processed_data(
            X_train_scaled, X_test_scaled, y_train, y_test, output_dir
        )
        
        print("\n" + "="*70)
        print("✅ PREPROCESSING COMPLETE!")
        print("="*70)
        print(f"\n📦 Output files:")
        print(f"   • {train_path}")
        print(f"   • {test_path}")
        print(f"   • {scaler_path}")
        print(f"\n🚀 Ready for Phase 5: Model Training")
        print("="*70 + "\n")
        
        return {
            'train_path': train_path,
            'test_path': test_path,
            'scaler_path': scaler_path,
            'X_train': X_train_scaled,
            'X_test': X_test_scaled,
            'y_train': y_train,
            'y_test': y_test
        }


def main():
    """Main preprocessing execution"""
    
    # Determine paths
    if os.path.exists('data'):
        input_path = "data/raw/flood_data.csv"
        output_dir = "data/processed"
    else:
        input_path = "../../data/raw/flood_data.csv"
        output_dir = "../../data/processed"
    
    # Create preprocessor and run pipeline
    preprocessor = FloodDataPreprocessor()
    results = preprocessor.preprocess_pipeline(input_path, output_dir, test_size=0.2)
    
    # Display summary statistics
    print("\n📊 PREPROCESSING SUMMARY:")
    print(f"   Original dataset: {input_path}")
    print(f"   Training samples: {len(results['X_train'])}")
    print(f"   Test samples: {len(results['X_test'])}")
    print(f"   Features: {len(FEATURE_NAMES)}")
    print(f"   Classes: 4 (Safe, Warning, High Risk, Critical)")
    print(f"   Output directory: {output_dir}")


if __name__ == "__main__":
    main()