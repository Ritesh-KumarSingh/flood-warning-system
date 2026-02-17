"""
Model Evaluation Module
Detailed evaluation metrics and analysis
"""

import os
import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                            f1_score, confusion_matrix, classification_report)
import joblib

def evaluate_model_detailed(model, X_test, y_test):
    """
    Perform detailed model evaluation with multiple metrics
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test labels
        
    Returns:
        Dictionary with comprehensive metrics
    """
    print("\n" + "="*70)
    print(" "*15 + "📊 DETAILED MODEL EVALUATION")
    print("="*70 + "\n")
    
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)
    
    # Overall metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision_macro = precision_score(y_test, y_pred, average='macro', zero_division=0)
    recall_macro = recall_score(y_test, y_pred, average='macro', zero_division=0)
    f1_macro = f1_score(y_test, y_pred, average='macro', zero_division=0)
    
    precision_weighted = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall_weighted = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1_weighted = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    print("🎯 OVERALL PERFORMANCE METRICS")
    print("-" * 70)
    print(f"Accuracy:           {accuracy:.4f} ({accuracy*100:.2f}%)")
    print()
    print("Macro Averages (unweighted):")
    print(f"  Precision:        {precision_macro:.4f}")
    print(f"  Recall:           {recall_macro:.4f}")
    print(f"  F1-Score:         {f1_macro:.4f}")
    print()
    print("Weighted Averages (by support):")
    print(f"  Precision:        {precision_weighted:.4f}")
    print(f"  Recall:           {recall_weighted:.4f}")
    print(f"  F1-Score:         {f1_weighted:.4f}")
    print()
    
    # Per-class metrics
    print("📊 PER-CLASS PERFORMANCE")
    print("-" * 70)
    
    risk_labels = ['Safe', 'Warning', 'High Risk', 'Critical']
    class_report = classification_report(y_test, y_pred, 
                                        target_names=risk_labels,
                                        output_dict=True,
                                        zero_division=0)
    
    print(f"{'Class':<15} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Support':<10}")
    print("-" * 70)
    
    for idx, label in enumerate(risk_labels):
        metrics = class_report[label]
        emoji = "🟢" if idx == 0 else "🟡" if idx == 1 else "🟠" if idx == 2 else "🔴"
        print(f"{emoji} {label:<13} {metrics['precision']:<12.4f} {metrics['recall']:<12.4f} "
              f"{metrics['f1-score']:<12.4f} {int(metrics['support']):<10}")
    
    print()
    
    # Confusion Matrix Analysis
    conf_matrix = confusion_matrix(y_test, y_pred)
    
    print("🔍 CONFUSION MATRIX ANALYSIS")
    print("-" * 70)
    print("\nConfusion Matrix:")
    print("                 Predicted →")
    print("Actual ↓    Safe    Warning  High    Critical")
    print("-" * 70)
    for idx, label in enumerate(['Safe     ', 'Warning  ', 'High Risk', 'Critical ']):
        row = conf_matrix[idx]
        print(f"{label}  {row[0]:6d}  {row[1]:7d}  {row[2]:7d}  {row[3]:8d}")
    print()
    
    # Calculate per-class accuracy
    print("Per-class accuracy:")
    for idx, label in enumerate(risk_labels):
        class_accuracy = conf_matrix[idx, idx] / conf_matrix[idx].sum()
        print(f"  {label:<15}: {class_accuracy:.4f} ({class_accuracy*100:.1f}%)")
    print()
    
    # Misclassification analysis
    print("⚠️  MISCLASSIFICATION ANALYSIS")
    print("-" * 70)
    
    total_errors = len(y_test) - np.sum(np.diag(conf_matrix))
    error_rate = total_errors / len(y_test)
    
    print(f"Total misclassifications: {total_errors} / {len(y_test)} ({error_rate*100:.2f}%)")
    print()
    
    print("Most common errors:")
    errors = []
    for i in range(4):
        for j in range(4):
            if i != j and conf_matrix[i, j] > 0:
                errors.append({
                    'from': risk_labels[i],
                    'to': risk_labels[j],
                    'count': conf_matrix[i, j],
                    'severity': abs(i - j)  # How many levels off
                })
    
    errors_df = pd.DataFrame(errors).sort_values('count', ascending=False)
    
    for idx, row in errors_df.head(5).iterrows():
        severity = "⚠️ " if row['severity'] == 1 else "⚠️⚠️ " if row['severity'] == 2 else "⚠️⚠️⚠️ "
        print(f"  {severity}{row['from']:<12} → {row['to']:<12}: {int(row['count']):3d} cases")
    
    print()
    
    # Critical class analysis (most important!)
    print("🚨 CRITICAL CLASS ANALYSIS (Most Important)")
    print("-" * 70)
    
    critical_idx = 3
    critical_recall = class_report['Critical']['recall']
    critical_precision = class_report['Critical']['precision']
    
    print(f"Critical class recall:    {critical_recall:.4f} ({critical_recall*100:.1f}%)")
    print(f"Critical class precision: {critical_precision:.4f} ({critical_precision*100:.1f}%)")
    print()
    
    # False negatives (missed critical floods - MOST DANGEROUS!)
    false_negatives = conf_matrix[critical_idx].sum() - conf_matrix[critical_idx, critical_idx]
    print(f"False Negatives (Missed critical floods): {false_negatives}")
    if false_negatives > 0:
        print(f"  ⚠️  Model missed {false_negatives} critical flood events!")
        print(f"  These are the most dangerous errors - floods we didn't warn about.")
    else:
        print(f"  ✅ Model caught all critical floods!")
    
    print()
    
    # False positives (false alarms)
    false_positives = conf_matrix[:, critical_idx].sum() - conf_matrix[critical_idx, critical_idx]
    print(f"False Positives (False critical alarms): {false_positives}")
    if false_positives > 0:
        print(f"  ⚠️  Model gave {false_positives} false critical alarms")
        print(f"  These reduce trust but are safer than missing real floods.")
    else:
        print(f"  ✅ No false critical alarms!")
    
    print()
    
    # Overall assessment
    print("📝 OVERALL MODEL ASSESSMENT")
    print("-" * 70)
    
    if accuracy >= 0.90:
        print("✅ EXCELLENT: Accuracy ≥ 90%")
    elif accuracy >= 0.85:
        print("✅ GOOD: Accuracy ≥ 85%")
    elif accuracy >= 0.80:
        print("⚠️  ACCEPTABLE: Accuracy ≥ 80%")
    else:
        print("❌ NEEDS IMPROVEMENT: Accuracy < 80%")
    
    if critical_recall >= 0.90:
        print("✅ EXCELLENT: Critical recall ≥ 90% (catching most dangerous floods)")
    elif critical_recall >= 0.85:
        print("✅ GOOD: Critical recall ≥ 85%")
    elif critical_recall >= 0.80:
        print("⚠️  ACCEPTABLE: Critical recall ≥ 80%")
    else:
        print("❌ CRITICAL: Recall < 80% - Too many missed critical floods!")
    
    print()
    print("="*70 + "\n")
    
    return {
        'accuracy': accuracy,
        'precision_macro': precision_macro,
        'recall_macro': recall_macro,
        'f1_macro': f1_macro,
        'precision_weighted': precision_weighted,
        'recall_weighted': recall_weighted,
        'f1_weighted': f1_weighted,
        'confusion_matrix': conf_matrix,
        'classification_report': class_report,
        'predictions': y_pred,
        'probabilities': y_pred_proba,
        'critical_recall': critical_recall,
        'critical_precision': critical_precision,
        'false_negatives': false_negatives,
        'false_positives': false_positives
    }


def generate_evaluation_report(results, output_path='../../outputs/evaluation_report.txt'):
    """
    Generate text evaluation report
    
    Args:
        results: Evaluation results dictionary
        output_path: Path to save report
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write("="*70 + "\n")
        f.write(" "*15 + "FLOOD PREDICTION MODEL EVALUATION REPORT\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("OVERALL PERFORMANCE\n")
        f.write("-"*70 + "\n")
        f.write(f"Accuracy:           {results['accuracy']:.4f} ({results['accuracy']*100:.2f}%)\n")
        f.write(f"Precision (macro):  {results['precision_macro']:.4f}\n")
        f.write(f"Recall (macro):     {results['recall_macro']:.4f}\n")
        f.write(f"F1-Score (macro):   {results['f1_macro']:.4f}\n\n")
        
        f.write("PER-CLASS METRICS\n")
        f.write("-"*70 + "\n")
        
        risk_labels = ['Safe', 'Warning', 'High Risk', 'Critical']
        class_report = results['classification_report']
        
        for label in risk_labels:
            metrics = class_report[label]
            f.write(f"\n{label}:\n")
            f.write(f"  Precision: {metrics['precision']:.4f}\n")
            f.write(f"  Recall:    {metrics['recall']:.4f}\n")
            f.write(f"  F1-Score:  {metrics['f1-score']:.4f}\n")
            f.write(f"  Support:   {int(metrics['support'])}\n")
        
        f.write("\n" + "="*70 + "\n")
    
    print(f"✅ Evaluation report saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    # Load model and data for evaluation
    from data_loader import load_preprocessed_data
    
    data = load_preprocessed_data()
    model = joblib.load('../../data/models/flood_model.pkl')
    
    results = evaluate_model_detailed(model, data['X_test'], data['y_test'])
    generate_evaluation_report(results)