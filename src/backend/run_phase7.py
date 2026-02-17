"""
Phase 7 Master Script
Starts the FastAPI server and provides usage instructions
"""

import os
import sys

def run_phase_7():
    """Execute Phase 7 - Start API Server"""
    
    print("\n" + "="*70)
    print(" "*15 + "🚀 PHASE 7: BACKEND API DEVELOPMENT")
    print("="*70 + "\n")
    
    print("📦 Deliverables:")
    print("   ✅ FastAPI application (main.py)")
    print("   ✅ Pydantic models (models.py)")
    print("   ✅ API endpoints:")
    print("      • POST /predict - Full prediction with alerts")
    print("      • POST /quick-check - Quick risk assessment")
    print("      • POST /batch-predict - Batch predictions")
    print("      • GET /health - Health check")
    print("      • GET /risk-levels - Risk level info")
    print("      • GET /features - Feature info")
    print("   ✅ API testing script (test_api.py)")
    print("   ✅ CORS enabled for frontend")
    print("   ✅ Auto-generated documentation")
    
    print("\n🔧 Features:")
    print("   ✅ Input validation (Pydantic)")
    print("   ✅ Error handling")
    print("   ✅ Processing time tracking")
    print("   ✅ Batch predictions (up to 10)")
    print("   ✅ Interactive API docs")
    
    print("\n" + "-"*70)
    print("🌐 STARTING API SERVER")
    print("-"*70 + "\n")
    
    print("📍 Server will be available at:")
    print("   • API Root: http://localhost:8000")
    print("   • Interactive Docs: http://localhost:8000/docs")
    print("   • Alternative Docs: http://localhost:8000/redoc")
    print("   • Health Check: http://localhost:8000/health")
    
    print("\n💡 To test the API:")
    print("   1. Keep this server running")
    print("   2. Open a new terminal")
    print("   3. Activate venv: venv\\Scripts\\Activate.ps1")
    print("   4. Run: python test_api.py")
    
    print("\n⚠️  Press Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    # Start the server
    import uvicorn
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("🛑 Server stopped")
        print("="*70 + "\n")
        print("✅ PHASE 7 COMPLETE!")
        print("\n🚀 Next Step: Phase 8 - Live Data Integration")
        print("="*70 + "\n")


if __name__ == "__main__":
    run_phase_7()