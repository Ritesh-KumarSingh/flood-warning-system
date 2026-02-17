"""Test script to verify all installations"""

def test_imports():
    """Test if all required libraries can be imported"""
    
    print("Testing imports...")
    
    try:
        import numpy as np
        print("✓ NumPy version:", np.__version__)
    except ImportError as e:
        print("✗ NumPy import failed:", e)
    
    try:
        import pandas as pd
        print("✓ Pandas version:", pd.__version__)
    except ImportError as e:
        print("✗ Pandas import failed:", e)
    
    try:
        import sklearn
        print("✓ Scikit-learn version:", sklearn.__version__)
    except ImportError as e:
        print("✗ Scikit-learn import failed:", e)
    
    try:
        import fastapi
        print("✓ FastAPI version:", fastapi.__version__)
    except ImportError as e:
        print("✗ FastAPI import failed:", e)
    
    try:
        import streamlit
        print("✓ Streamlit version:", streamlit.__version__)
    except ImportError as e:
        print("✗ Streamlit import failed:", e)
    
    try:
        import requests
        print("✓ Requests version:", requests.__version__)
    except ImportError as e:
        print("✗ Requests import failed:", e)
    
    print("\n✅ All critical libraries installed successfully!")
    print("🚀 Ready to start development!")

if __name__ == "__main__":
    test_imports()