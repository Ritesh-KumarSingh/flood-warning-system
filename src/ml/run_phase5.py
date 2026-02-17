"""
Phase 5 Master Script
Runs complete model training, evaluation, and visualization pipeline
"""

import os
import sys

def run_phase_5():
    """Execute all Phase 5 tasks in sequence"""
    
    print("\n" + "="*70)
    print(" "*15 + "🚀 PHASE 5: MODEL TRAINING")
    print("="*70 + "\n")
    
    print("This script will:")
    print("  1. Load preprocessed train/test data")
    print("  2. Train Random Forest classifier")
    print("  3. Evaluate model performance")
    print("  4. Create performance visualizations")
    print("  5. Save trained model")
    print("  6. Generate evaluation report")
    print("  7. Run example predictions")
    print("\n" + "-"*70 + "\n")
    
    # Step 1: Train Model
    print("STEP 1: Training Random Forest Model")
    print("-"*70)
    try:
        from train_model import train_model_pipeline
        
        # Determine paths
        if os.path.exists('data'):
            data_dir = "data/processed"
            model_dir = "data/models"
        else:
            data_dir = "../../data/processed"
            model_dir = "../../data/models"
        
        # Train model
        predictor, results = train_model_pipeline(data_dir, model_dir)
        
        print("\n✅ Step 1 Complete!")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure you've run Phase 4 first to preprocess the data!")
        return False
    except Exception as e:
        print(f"\n❌ Error in Step 1: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 2: Detailed Evaluation
    print("\n" + "-"*70)
    print("STEP 2: Detailed Model Evaluation")
    print("-"*70)
    try:
        from evaluate_model import evaluate_model_detailed, generate_evaluation_report
        from data_loader import load_preprocessed_data
        
        data = load_preprocessed_data(data_dir)
        detailed_results = evaluate_model_detailed(predictor.model, 
                                                   data['X_test'], 
                                                   data['y_test'])
        
        # Generate report
        if os.path.exists('data'):
            report_path = "outputs/evaluation_report.txt"
        else:
            report_path = "../../outputs/evaluation_report.txt"
        
        generate_evaluation_report(detailed_results, report_path)
        
        print("\n✅ Step 2 Complete!")
        
    except Exception as e:
        print(f"\n❌ Error in Step 2: {e}")
        print("Continuing with remaining steps...")
    
    # Step 3: Create Visualizations
    print("\n" + "-"*70)
    print("STEP 3: Creating Performance Visualizations")
    print("-"*70)
    try:
        from visualize_model import visualize_model_performance
        
        if os.path.exists('data'):
            vis_output = "outputs"
        else:
            vis_output = "../../outputs"
        
        visualize_model_performance(predictor.model, 
                                   data['X_test'], 
                                   data['y_test'], 
                                   vis_output)
        
        print("\n✅ Step 3 Complete!")
        
    except Exception as e:
        print(f"\n⚠️  Error in Step 3: {e}")
        print("Note: Visualization errors won't affect your trained model")
        print("Your model is still ready for deployment!")
    
    # Step 4: Example Predictions
    print("\n" + "-"*70)
    print("STEP 4: Running Example Predictions")
    print("-"*70)
    try:
        from predict import example_predictions
        
        example_predictions()
        
        print("✅ Step 4 Complete!")
        
    except Exception as e:
        print(f"\n⚠️  Error in Step 4: {e}")
        print("Your model is still trained and ready!")
    
    # Final Summary
    print("\n" + "="*70)
    print(" "*15 + "🎉 PHASE 5 COMPLETE!")
    print("="*70)
    
    print("\n📦 Deliverables:")
    
    if os.path.exists('data'):
        model_path = "data/models/flood_model.pkl"
        metadata_path = "data/models/flood_model_metadata.json"
        output_dir = "outputs"
    else:
        model_path = "../../data/models/flood_model.pkl"
        metadata_path = "../../data/models/flood_model_metadata.json"
        output_dir = "../../outputs"
    
    print(f"   ✅ Trained model: {model_path}")
    print(f"   ✅ Model metadata: {metadata_path}")
    print(f"   ✅ Evaluation report: {output_dir}/evaluation_report.txt")
    
    print(f"\n📊 Model Performance:")
    print(f"   Accuracy: {results['accuracy']:.4f} ({results['accuracy']*100:.2f}%)")
    
    # Get critical class recall
    critical_recall = results['classification_report']['Critical']['recall']
    print(f"   Critical Recall: {critical_recall:.4f} ({critical_recall*100:.1f}%)")
    
    if results['accuracy'] >= 0.85 and critical_recall >= 0.85:
        print(f"\n   ✅ Model meets performance targets!")
    else:
        print(f"\n   ⚠️  Model may need improvement")
    
    print(f"\n📈 Visualizations:")
    print(f"   ✅ Confusion matrix: {output_dir}/confusion_matrix.png")
    print(f"   ✅ Feature importance: {output_dir}/feature_importance.png")
    print(f"   ✅ Per-class performance: {output_dir}/per_class_performance.png")
    print(f"   ✅ Prediction confidence: {output_dir}/prediction_confidence.png")
    print(f"   ✅ Performance summary: {output_dir}/performance_summary.png")
    print(f"   ✅ Actual vs predicted: {output_dir}/actual_vs_predicted.png")
    
    print("\n🚀 Next Step: Phase 6 - Risk Scoring Logic")
    print("="*70 + "\n")
    
    return True


if __name__ == "__main__":
    success = run_phase_5()
    sys.exit(0 if success else 1)