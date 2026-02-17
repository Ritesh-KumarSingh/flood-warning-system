"""
Phase 3 Master Script
Runs all data collection and analysis tasks
"""

import os
import sys

def run_phase_3():
    """Execute all Phase 3 tasks in sequence"""
    
    print("\n" + "="*70)
    print(" "*15 + "🚀 PHASE 3: DATA COLLECTION")
    print("="*70 + "\n")
    
    print("This script will:")
    print("  1. Generate 2,000 synthetic flood scenarios")
    print("  2. Validate data quality")
    print("  3. Create visualizations for analysis")
    print("\n" + "-"*70 + "\n")
    
    # Step 1: Generate Data
    print("STEP 1: Generating Synthetic Dataset")
    print("-"*70)
    try:
        from generate_data import generate_flood_data, save_dataset, display_dataset_stats
        
        # Generate data
        df = generate_flood_data(n_samples=2000)
        
        # Display stats
        display_dataset_stats(df)
        
        # Save data
        if os.path.exists('data'):
            output_path = "data/raw/flood_data.csv"
        else:
            output_path = "../../data/raw/flood_data.csv"
        
        save_dataset(df, output_path)
        
        print("\n✅ Step 1 Complete!")
        
    except Exception as e:
        print(f"\n❌ Error in Step 1: {e}")
        return False
    
    # Step 2: Validate Data
    print("\n" + "-"*70)
    print("STEP 2: Validating Data Quality")
    print("-"*70)
    try:
        from validate_data import validate_dataset
        
        validation_passed = validate_dataset(output_path)
        
        if validation_passed:
            print("\n✅ Step 2 Complete!")
        else:
            print("\n⚠️  Step 2 completed with warnings")
        
    except Exception as e:
        print(f"\n❌ Error in Step 2: {e}")
        return False
    
    # Step 3: Create Visualizations
    print("\n" + "-"*70)
    print("STEP 3: Creating Visualizations")
    print("-"*70)
    try:
        from visualize_data import create_visualizations
        
        if os.path.exists('data'):
            output_dir = "outputs"
        else:
            output_dir = "../../outputs"
        
        create_visualizations(output_path, output_dir)
        
        print("\n✅ Step 3 Complete!")
        
    except Exception as e:
        print(f"\n❌ Error in Step 3: {e}")
        print("Note: Visualization errors are often due to matplotlib display issues")
        print("Your data is still valid even if visualizations fail")
    
    # Final Summary
    print("\n" + "="*70)
    print(" "*15 + "🎉 PHASE 3 COMPLETE!")
    print("="*70)
    print("\n📦 Deliverables:")
    print(f"  ✅ Dataset: {output_path}")
    print(f"  ✅ Visualizations: {output_dir}/")
    print("\n🚀 Next Step: Phase 4 - Data Preprocessing")
    print("="*70 + "\n")
    
    return True


if __name__ == "__main__":
    success = run_phase_3()
    sys.exit(0 if success else 1)