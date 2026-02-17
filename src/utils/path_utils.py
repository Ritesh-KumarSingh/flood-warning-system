"""
path_utils.py - Central path resolver for the project.
Computes absolute paths from __file__ so it works on any machine
or cloud platform regardless of working directory.
"""
import os

_THIS_FILE   = os.path.abspath(__file__)          # src/utils/path_utils.py
_UTILS_DIR   = os.path.dirname(_THIS_FILE)        # src/utils
_SRC_DIR     = os.path.dirname(_UTILS_DIR)        # src
PROJECT_ROOT = os.path.dirname(_SRC_DIR)          # project root

MODEL_PATH  = os.path.join(PROJECT_ROOT, "data", "models",    "flood_model.pkl")
SCALER_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "scaler.pkl")

def get_project_root(): return PROJECT_ROOT
def get_model_path():   return MODEL_PATH
def get_scaler_path():  return SCALER_PATH
def paths_exist():      return os.path.isfile(MODEL_PATH) and os.path.isfile(SCALER_PATH)

if __name__ == "__main__":
    print(f"Project root : {PROJECT_ROOT}")
    print(f"Model        : {MODEL_PATH}  -> exists: {os.path.isfile(MODEL_PATH)}")
    print(f"Scaler       : {SCALER_PATH} -> exists: {os.path.isfile(SCALER_PATH)}")
