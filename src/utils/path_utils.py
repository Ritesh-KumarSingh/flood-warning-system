"""
path_utils.py — Central path resolver for the project.

Import this from any module to get reliable absolute paths
regardless of where Python is launched from.
"""

import os

# Resolve the project root: this file lives at src/utils/path_utils.py
# so root is three directories up.
_THIS_FILE = os.path.abspath(__file__)          # .../src/utils/path_utils.py
_SRC_DIR   = os.path.dirname(_THIS_FILE)        # .../src/utils
_SRC_ROOT  = os.path.dirname(_SRC_DIR)          # .../src
PROJECT_ROOT = os.path.dirname(_SRC_ROOT)       # .../<project-root>

# Canonical model & scaler locations
MODEL_PATH  = os.path.join(PROJECT_ROOT, "data", "models",    "flood_model.pkl")
SCALER_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "scaler.pkl")

def get_project_root() -> str:
    return PROJECT_ROOT

def get_model_path() -> str:
    return MODEL_PATH

def get_scaler_path() -> str:
    return SCALER_PATH

def paths_exist() -> bool:
    """Return True only if BOTH model files are present."""
    return os.path.isfile(MODEL_PATH) and os.path.isfile(SCALER_PATH)

if __name__ == "__main__":
    print(f"Project root : {PROJECT_ROOT}")
    print(f"Model path   : {MODEL_PATH}  — exists: {os.path.isfile(MODEL_PATH)}")
    print(f"Scaler path  : {SCALER_PATH} — exists: {os.path.isfile(SCALER_PATH)}")