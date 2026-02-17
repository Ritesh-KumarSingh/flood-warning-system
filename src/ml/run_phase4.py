"""
Phase 4 Master Script
Runs complete data preprocessing pipeline
"""

import os
import sys

def run_phase_4():
    """Execute all Phase 4 tasks in sequence"""
    
    print("\n" + "="*70)
    print(" "*15 + "🚀 PHASE 4: DATA PREPROCESSING")
    print("="*70 + "\n")
    
    print("This script will:")
    print("  1. Load raw flood data")
    print("  2. Clean and validate data")
    print("  3. Normalize features (StandardScaler)")
    print("  4. Split into train/test sets (80/20)")
    print("  5. Save processed datasets")
    print("  6. Create preprocessing visualizations")
    print("\n" + "-"*70 + "\n")
    
    # Step 1: Run preprocessing pipeline
    print("STEP 1: Running Preprocessing Pipeline")
    print("-"*70)
    try:
        from data_preprocessing import FloodDataPreprocessor
        
        # Determine paths
        if os.path.exists('data'):
            input_path = "data/raw/flood_data.csv"
            output_dir = "data/processed"
        else:
            input_path = "../../data/raw/flood_data.csv"
            output_dir = "../../data/processed"
        
        # Run preprocessing
        preprocessor = FloodDataPreprocessor()
        results = preprocessor.preprocess_pipeline(input_path, output_dir, test_size=0.2)
        
        print("\n✅ Step 1 Complete!")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure you've run Phase 3 first to generate the dataset!")
        return False
    except Exception as e:
        print(f"\n❌ Error in Step 1: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 2: Load and display processed data info
    print("\n" + "-"*70)
    print("STEP 2: Verifying Processed Data")
    print("-"*70)
    try:
        from data_loader import load_preprocessed_data, display_data_info
        
        data = load_preprocessed_data(output_dir)
        display_data_info(data)
        
        print("✅ Step 2 Complete!")
        
    except Exception as e:
        print(f"\n❌ Error in Step 2: {e}")
        return False
    
    # Step 3: Create visualizations
    print("\n" + "-"*70)
    print("STEP 3: Creating Preprocessing Visualizations")
    print("-"*70)
    try:
        from visualize_preprocessing import visualize_preprocessing
        
        if os.path.exists('data'):
            vis_output = "outputs"
        else:
            vis_output = "../../outputs"
        
        visualize_preprocessing(input_path, output_dir, vis_output)
        
        print("\n✅ Step 3 Complete!")
        
    except Exception as e:
        print(f"\n⚠️  Error in Step 3: {e}")
        print("Note: Visualization errors won't affect your processed data")
        print("Your data is still ready for model training!")
    
    # Final Summary
    print("\n" + "="*70)
    print(" "*15 + "🎉 PHASE 4 COMPLETE!")
    print("="*70)
    print("\n📦 Deliverables:")
    print(f"   ✅ Training set: {output_dir}/train.csv")
    print(f"   ✅ Test set: {output_dir}/test.csv")
    print(f"   ✅ Scaler: {output_dir}/scaler.pkl")
    print(f"   ✅ Metadata: {output_dir}/preprocessing_metadata.json")
    
    if os.path.exists('data'):
        vis_dir = "outputs"
    else:
        vis_dir = "../../outputs"
    
    print(f"\n📊 Visualizations:")
    print(f"   ✅ Normalization effects: {vis_dir}/normalization_effect.png")
    print(f"   ✅ Train/test split: {vis_dir}/train_test_split.png")
    print(f"   ✅ Feature scaling: {vis_dir}/feature_scaling.png")
    
    print("\n🚀 Next Step: Phase 5 - Model Training")
    print("="*70 + "\n")
    
    return True


if __name__ == "__main__":
    success = run_phase_4()
    sys.exit(0 if success else 1)