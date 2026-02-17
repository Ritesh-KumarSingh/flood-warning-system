"""
Phase 6 Master Script
Demonstrates complete risk scoring and alert generation system
"""

import os
import sys

def run_phase_6():
    """Execute Phase 6 demonstrations"""
    
    print("\n" + "="*70)
    print(" "*15 + "🚀 PHASE 6: RISK SCORING LOGIC")
    print("="*70 + "\n")
    
    print("This script will:")
    print("  1. Demonstrate risk scoring module")
    print("  2. Show alert generation for all risk levels")
    print("  3. Display integrated assessment system")
    print("  4. Run comprehensive examples")
    print("\n" + "-"*70 + "\n")
    
    # Step 1: Basic Risk Scoring Demo
    print("STEP 1: Risk Scoring Module Demo")
    print("-"*70)
    try:
        from risk_scoring import RiskScorer, format_alert_for_display
        
        scorer = RiskScorer()
        print("✅ Risk scorer initialized\n")
        
        # Demo all risk levels
        risk_levels = [
            (0, "Safe", "Mumbai"),
            (1, "Warning", "Kolkata"),
            (2, "High Risk", "Patna"),
            (3, "Critical", "Guwahati")
        ]
        
        for level, label, location in risk_levels:
            print(f"📊 Generating {label} alert for {location}...")
            alert = scorer.generate_alert_message(level, location)
            print(f"   ✅ Title: {alert['title']}")
            print(f"   ✅ Actions: {len(alert['recommended_actions'])} recommended")
            if alert['emergency_contacts']:
                print(f"   ✅ Emergency contacts: {len(alert['emergency_contacts'])}")
            print()
        
        print("✅ Step 1 Complete!\n")
        
    except Exception as e:
        print(f"\n❌ Error in Step 1: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 2: Integrated Assessment Demo
    print("\n" + "-"*70)
    print("STEP 2: Integrated Flood Assessment System")
    print("-"*70)
    try:
        from flood_assessment import FloodRiskAssessor, run_examples
        
        print("\n🌊 Running comprehensive examples...\n")
        run_examples()
        
        print("\n✅ Step 2 Complete!")
        
    except Exception as e:
        print(f"\n❌ Error in Step 2: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Final Summary
    print("\n" + "="*70)
    print(" "*15 + "🎉 PHASE 6 COMPLETE!")
    print("="*70)
    
    print("\n📦 Deliverables:")
    print("   ✅ Risk Scoring Module (risk_scoring.py)")
    print("   ✅ Integrated Assessment System (flood_assessment.py)")
    print("   ✅ Alert Generation with 4 risk levels")
    print("   ✅ Actionable recommendations")
    print("   ✅ Emergency contact integration")
    print("   ✅ Feature-based warning system")
    
    print("\n🎯 Key Features:")
    print("   ✅ Converts probabilities to risk levels (0-3)")
    print("   ✅ Generates contextual alert messages")
    print("   ✅ Provides location-specific recommendations")
    print("   ✅ Analyzes critical features automatically")
    print("   ✅ Formats alerts for display")
    print("   ✅ Supports batch assessments")
    
    print("\n📊 Example Output:")
    print("   • Safe: 'Continue normal activities'")
    print("   • Warning: 'Monitor weather, prepare emergency kit'")
    print("   • High Risk: 'Prepare to evacuate'")
    print("   • Critical: 'EVACUATE IMMEDIATELY'")
    
    print("\n🚀 Next Step: Phase 7 - Backend API Development")
    print("   Build FastAPI endpoints to serve predictions and alerts")
    print("="*70 + "\n")
    
    return True


if __name__ == "__main__":
    success = run_phase_6()
    sys.exit(0 if success else 1)