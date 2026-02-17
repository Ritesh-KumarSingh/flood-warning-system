"""
Model Training Module
Trains Random Forest classifier for flood prediction
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os
import json
from datetime import datetime
from data_loader import load_preprocessed_data
from schema import FEATURE_NAMES, TARGET_NAME, RISK_LEVELS

class FloodPredictor:
    """Random Forest model for flood risk prediction"""
    
    def __init__(self, n_estimators=100, max_depth=None, random_state=42):
        """
        Initialize Random Forest classifier
        
        Args:
            n_estimators: Number of trees in the forest
            max_depth: Maximum depth of trees
            random_state: Random seed for reproducibility
        """
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1,  # Use all CPU cores
            class_weight='balanced'  # Handle class imbalance
        )
        self.feature_names = FEATURE_NAMES
        self.target_name = TARGET_NAME
        self.is_trained = False
        self.training_date = None
        self.feature_importance = None
        
    def train(self, X_train, y_train):
        """
        Train the Random Forest model
        
        Args:
            X_train: Training features
            y_train: Training labels
        """
        print("\n" + "="*70)
        print(" "*20 + "🌲 TRAINING RANDOM FOREST")
        print("="*70 + "\n")
        
        print(f"📊 Training data shape: {X_train.shape}")
        print(f"   Features: {X_train.shape[1]}")
        print(f"   Samples: {X_train.shape[0]}")
        
        # Display class distribution
        print(f"\n🎯 Target distribution:")
        risk_labels = {0: 'Safe', 1: 'Warning', 2: 'High Risk', 3: 'Critical'}
        for level, count in y_train.value_counts().sort_index().items():
            percentage = (count / len(y_train)) * 100
            print(f"   Level {level} ({risk_labels[level]:10s}): {count:4d} ({percentage:5.1f}%)")
        
        # Train model
        print(f"\n🔧 Training Random Forest...")
        print(f"   Trees: {self.model.n_estimators}")
        print(f"   Max depth: {self.model.max_depth if self.model.max_depth else 'None (unlimited)'}")
        print(f"   Class weight: balanced")
        
        self.model.fit(X_train, y_train)
        
        self.is_trained = True
        self.training_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Calculate feature importance
        self.feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print(f"\n✅ Model training complete!")
        print(f"   Training date: {self.training_date}")
        
        # Display top features
        print(f"\n⭐ Top 5 Most Important Features:")
        for idx, row in self.feature_importance.head(5).iterrows():
            bar = "█" * int(row['importance'] * 100)
            print(f"   {row['feature']:25s}: {row['importance']:.4f} {bar}")
        
        return self
    
    def predict(self, X):
        """
        Make predictions on new data
        
        Args:
            X: Features to predict
            
        Returns:
            Predicted risk levels
        """
        if not self.is_trained:
            raise RuntimeError("Model must be trained before making predictions")
        
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """
        Get probability predictions
        
        Args:
            X: Features to predict
            
        Returns:
            Probability for each class
        """
        if not self.is_trained:
            raise RuntimeError("Model must be trained before making predictions")
        
        return self.model.predict_proba(X)
    
    def evaluate(self, X_test, y_test):
        """
        Evaluate model performance
        
        Args:
            X_test: Test features
            y_test: Test labels
            
        Returns:
            Dictionary with evaluation metrics
        """
        print("\n" + "="*70)
        print(" "*20 + "📊 MODEL EVALUATION")
        print("="*70 + "\n")
        
        # Make predictions
        y_pred = self.predict(X_test)
        y_pred_proba = self.predict_proba(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)
        class_report = classification_report(y_test, y_pred, 
                                            target_names=['Safe', 'Warning', 'High Risk', 'Critical'],
                                            output_dict=True)
        
        # Display results
        print(f"🎯 Overall Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        print()
        
        print("📊 Performance by Risk Level:")
        print("-" * 70)
        print(f"{'Class':<15} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Support':<10}")
        print("-" * 70)
        
        risk_labels = ['Safe', 'Warning', 'High Risk', 'Critical']
        for idx, label in enumerate(risk_labels):
            metrics = class_report[label]
            print(f"{label:<15} {metrics['precision']:<12.4f} {metrics['recall']:<12.4f} "
                  f"{metrics['f1-score']:<12.4f} {int(metrics['support']):<10}")
        
        # Weighted averages
        print("-" * 70)
        weighted = class_report['weighted avg']
        print(f"{'Weighted Avg':<15} {weighted['precision']:<12.4f} {weighted['recall']:<12.4f} "
              f"{weighted['f1-score']:<12.4f} {int(class_report['macro avg']['support']):<10}")
        print()
        
        # Confusion Matrix
        print("🔍 Confusion Matrix:")
        print("-" * 70)
        print("         Predicted →")
        print("Actual ↓   Safe  Warn  High  Crit")
        print("-" * 70)
        for idx, label in enumerate(['Safe', 'Warn', 'High', 'Crit']):
            row = conf_matrix[idx]
            print(f"{label:8s}  {row[0]:5d} {row[1]:5d} {row[2]:5d} {row[3]:5d}")
        print()
        
        # Critical metric: Recall for Critical class
        critical_recall = class_report['Critical']['recall']
        print(f"⚠️  Critical Class Recall: {critical_recall:.4f} ({critical_recall*100:.1f}%)")
        if critical_recall < 0.85:
            print("   ⚠️  Warning: Critical class recall is below target (85%)")
        else:
            print("   ✅ Critical class recall meets target!")
        
        print("\n" + "="*70)
        
        return {
            'accuracy': accuracy,
            'confusion_matrix': conf_matrix,
            'classification_report': class_report,
            'predictions': y_pred,
            'probabilities': y_pred_proba
        }
    
    def save_model(self, filepath):
        """
        Save trained model to file
        
        Args:
            filepath: Path to save model
        """
        if not self.is_trained:
            raise RuntimeError("Cannot save untrained model")
        
        # Create directory if needed
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save model
        joblib.dump(self.model, filepath)
        
        # Save metadata
        metadata = {
            'training_date': self.training_date,
            'n_estimators': self.model.n_estimators,
            'max_depth': self.model.max_depth,
            'feature_names': self.feature_names,
            'feature_importance': self.feature_importance.to_dict('records'),
            'model_type': 'RandomForestClassifier'
        }
        
        metadata_path = filepath.replace('.pkl', '_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n💾 Model saved:")
        print(f"   Model: {filepath}")
        print(f"   Metadata: {metadata_path}")
        
        return filepath
    
    @classmethod
    def load_model(cls, filepath):
        """
        Load trained model from file
        
        Args:
            filepath: Path to model file
            
        Returns:
            Loaded FloodPredictor instance
        """
        predictor = cls()
        predictor.model = joblib.load(filepath)
        predictor.is_trained = True
        
        # Load metadata if available
        metadata_path = filepath.replace('.pkl', '_metadata.json')
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            predictor.training_date = metadata.get('training_date')
            
            if 'feature_importance' in metadata:
                predictor.feature_importance = pd.DataFrame(metadata['feature_importance'])
        
        print(f"✅ Model loaded from {filepath}")
        if predictor.training_date:
            print(f"   Training date: {predictor.training_date}")
        
        return predictor


def train_model_pipeline(data_dir='../../data/processed', model_dir='../../data/models'):
    """
    Complete model training pipeline
    
    Args:
        data_dir: Directory with preprocessed data
        model_dir: Directory to save trained model
        
    Returns:
        Trained model and evaluation results
    """
    print("\n" + "="*70)
    print(" "*15 + "🚀 MODEL TRAINING PIPELINE")
    print("="*70 + "\n")
    
    # Load preprocessed data
    print("📂 Loading preprocessed data...")
    data = load_preprocessed_data(data_dir)
    
    X_train = data['X_train']
    y_train = data['y_train']
    X_test = data['X_test']
    y_test = data['y_test']
    
    print(f"✅ Data loaded successfully")
    
    # Initialize and train model
    predictor = FloodPredictor(n_estimators=100, random_state=42)
    predictor.train(X_train, y_train)
    
    # Evaluate model
    results = predictor.evaluate(X_test, y_test)
    
    # Save model
    model_path = os.path.join(model_dir, 'flood_model.pkl')
    predictor.save_model(model_path)
    
    print("\n" + "="*70)
    print("✅ TRAINING PIPELINE COMPLETE!")
    print("="*70)
    print(f"\n📦 Outputs:")
    print(f"   Model: {model_path}")
    print(f"   Accuracy: {results['accuracy']:.4f} ({results['accuracy']*100:.2f}%)")
    print(f"\n🚀 Ready for Phase 6: Risk Scoring Logic")
    print("="*70 + "\n")
    
    return predictor, results


if __name__ == "__main__":
    # Run training pipeline
    predictor, results = train_model_pipeline()