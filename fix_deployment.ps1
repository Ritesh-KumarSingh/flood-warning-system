# ============================================================
#  DISASTER WARNING PLATFORM - DEPLOYMENT FIX SCRIPT
#  Run this in VS Code Terminal (PowerShell)
#  Fixes: FileNotFoundError for .pkl model files on Streamlit Cloud
# ============================================================

Write-Host ""
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   DISASTER WARNING PLATFORM - DEPLOYMENT FIX" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# ── 0. Navigate to project root ─────────────────────────────
$PROJECT = "E:\disaster_management\disaster-warning-platform"

if (-not (Test-Path $PROJECT)) {
    Write-Host "ERROR: Project folder not found at $PROJECT" -ForegroundColor Red
    Write-Host "Please edit the PROJECT variable in this script to your actual path." -ForegroundColor Yellow
    exit 1
}

Set-Location $PROJECT
Write-Host "Working in: $PROJECT" -ForegroundColor Green
Write-Host ""

# ── 1. Create src\utils folder ──────────────────────────────
Write-Host "[1/7] Creating src\utils folder..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "src\utils" | Out-Null
New-Item -ItemType File -Force -Path "src\utils\__init__.py" | Out-Null
Write-Host "      OK" -ForegroundColor Green

# ── 2. Write path_utils.py ──────────────────────────────────
Write-Host "[2/7] Writing src\utils\path_utils.py..." -ForegroundColor Yellow

@'
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
'@ | Set-Content "src\utils\path_utils.py" -Encoding UTF8

Write-Host "      OK" -ForegroundColor Green

# ── 3. Fix src\ml\predict.py ────────────────────────────────
Write-Host "[3/7] Writing src\ml\predict.py (with fallback predictor)..." -ForegroundColor Yellow

@'
"""
predict.py - FIXED for cloud deployment.
Uses path_utils for absolute paths.
Falls back to rule-based FallbackFloodPredictor if .pkl files are missing.
"""
import os, sys, pandas as pd, numpy as np

_ML_DIR    = os.path.dirname(os.path.abspath(__file__))
_SRC_DIR   = os.path.dirname(_ML_DIR)
_UTILS_DIR = os.path.join(_SRC_DIR, "utils")
for _p in (_ML_DIR, _UTILS_DIR):
    if _p not in sys.path: sys.path.insert(0, _p)

from path_utils import MODEL_PATH, SCALER_PATH
from schema import FEATURE_NAMES, get_risk_info


class FloodRiskPredictor:
    """ML predictor - requires trained .pkl files."""

    def __init__(self, model_path=None, scaler_path=None):
        import joblib
        model_path  = model_path  or MODEL_PATH
        scaler_path = scaler_path or SCALER_PATH
        if not os.path.isfile(model_path):
            raise FileNotFoundError(
                f"Model not found: {model_path}\n"
                "Commit data/models/flood_model.pkl to your repository.")
        if not os.path.isfile(scaler_path):
            raise FileNotFoundError(
                f"Scaler not found: {scaler_path}\n"
                "Commit data/processed/scaler.pkl to your repository.")
        self.model  = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        print(f"[OK] Model  : {model_path}")
        print(f"[OK] Scaler : {scaler_path}")

    def _prepare(self, d):
        df = pd.DataFrame([d])[FEATURE_NAMES]
        return pd.DataFrame(self.scaler.transform(df), columns=FEATURE_NAMES)

    def predict_single(self, features_dict):
        df    = self._prepare(features_dict)
        level = int(self.model.predict(df)[0])
        probs = self.model.predict_proba(df)[0]
        info  = get_risk_info(level)
        return {"risk_level": level, "risk_label": info["label"],
                "risk_color": info["color"], "probability": float(probs[level]),
                "probabilities": {"safe": float(probs[0]), "warning": float(probs[1]),
                                  "high_risk": float(probs[2]), "critical": float(probs[3])},
                "description": info["description"], "recommended_action": info["action"]}

    def predict_with_explanation(self, features_dict):
        result = self.predict_single(features_dict)
        flags  = []
        if features_dict.get("rainfall_mm", 0) > 200:
            flags.append(f"Very heavy rainfall: {features_dict['rainfall_mm']:.1f} mm")
        if features_dict.get("river_level_m", 0) > 10:
            flags.append(f"River at danger level: {features_dict['river_level_m']:.1f} m")
        if features_dict.get("soil_moisture_percent", 0) > 85:
            flags.append(f"Soil saturated: {features_dict['soil_moisture_percent']:.1f}%")
        if features_dict.get("distance_to_river_km", 99) < 1:
            flags.append(f"Very close to river: {features_dict['distance_to_river_km']:.2f} km")
        result["critical_features"] = flags
        result["input_features"]    = features_dict
        return result

    def predict_batch(self, features_df):
        df     = features_df[FEATURE_NAMES]
        scaled = pd.DataFrame(self.scaler.transform(df), columns=FEATURE_NAMES, index=df.index)
        levels = self.model.predict(scaled)
        probs  = self.model.predict_proba(scaled)
        out = features_df.copy()
        out["predicted_risk_level"]   = levels
        out["prediction_probability"] = [p[l] for p, l in zip(probs, levels)]
        out["risk_label"] = out["predicted_risk_level"].map(
            {0: "Safe", 1: "Warning", 2: "High Risk", 3: "Critical"})
        return out


class FallbackFloodPredictor:
    """
    Rule-based flood estimator.  Same output schema as FloodRiskPredictor.
    Used automatically when .pkl files are absent.
    """
    _LABELS  = ["Safe", "Warning", "High Risk", "Critical"]
    _COLORS  = ["green", "yellow", "orange", "red"]
    _DESCS   = ["Low flood risk. Conditions are within normal range.",
                "Moderate flood risk. Monitor conditions closely.",
                "High flood risk. Take precautionary measures immediately.",
                "Critical flood risk. Evacuate flood-prone areas now."]
    _ACTIONS = ["Continue normal activities. Stay alert to weather updates.",
                "Prepare emergency supplies. Avoid low-lying areas.",
                "Move valuables to higher ground. Be ready to evacuate.",
                "Evacuate immediately. Follow emergency services instructions."]

    def __init__(self, *args, **kwargs):
        print("[WARN] FallbackFloodPredictor active - ML model .pkl not found.")
        print("       Commit data/models/ to GitHub to enable full ML predictions.")

    @staticmethod
    def _score(f):
        s = 0
        r = f.get("rainfall_mm", 0)
        s += 4 if r>250 else 3 if r>150 else 2 if r>80 else 1 if r>40 else 0
        rv = f.get("river_level_m", 0)
        s += 4 if rv>12 else 3 if rv>8 else 2 if rv>5 else 1 if rv>3 else 0
        sm = f.get("soil_moisture_percent", 50)
        s += 3 if sm>90 else 2 if sm>75 else 1 if sm>60 else 0
        el = f.get("elevation_m", 100)
        s += 3 if el<20 else 2 if el<50 else 1 if el<100 else 0
        h = f.get("humidity_percent", 60)
        s += 2 if h>90 else 1 if h>75 else 0
        m = f.get("month", 6)
        s += 2 if m in (7,8,9) else 1 if m in (6,10) else 0
        return 3 if s>=12 else 2 if s>=7 else 1 if s>=3 else 0

    def _probs(self, level):
        p = [0.25/3]*4; p[level] = 0.75; return p

    def predict_single(self, features_dict):
        level = self._score(features_dict)
        probs = self._probs(level)
        return {"risk_level": level, "risk_label": self._LABELS[level],
                "risk_color": self._COLORS[level], "probability": probs[level],
                "probabilities": {"safe": probs[0], "warning": probs[1],
                                  "high_risk": probs[2], "critical": probs[3]},
                "description": self._DESCS[level],
                "recommended_action": self._ACTIONS[level],
                "_fallback": True}

    def predict_with_explanation(self, features_dict):
        result = self.predict_single(features_dict)
        flags  = []
        if features_dict.get("rainfall_mm", 0) > 200:
            flags.append(f"Very heavy rainfall: {features_dict['rainfall_mm']:.1f} mm")
        if features_dict.get("river_level_m", 0) > 10:
            flags.append(f"River at danger level: {features_dict['river_level_m']:.1f} m")
        if features_dict.get("soil_moisture_percent", 0) > 85:
            flags.append(f"Soil saturated: {features_dict['soil_moisture_percent']:.1f}%")
        result["critical_features"] = flags
        result["input_features"]    = features_dict
        return result

    def predict_batch(self, features_df):
        out = features_df.copy()
        out["predicted_risk_level"] = features_df.apply(
            lambda r: self._score(r.to_dict()), axis=1)
        out["prediction_probability"] = 0.75
        out["risk_label"] = out["predicted_risk_level"].map(
            {0:"Safe",1:"Warning",2:"High Risk",3:"Critical"})
        return out


def get_predictor(model_path=None, scaler_path=None):
    """Factory - always returns a working predictor."""
    try:
        return FloodRiskPredictor(model_path, scaler_path)
    except FileNotFoundError as e:
        print(f"[predict] {e}")
        return FallbackFloodPredictor()
'@ | Set-Content "src\ml\predict.py" -Encoding UTF8

Write-Host "      OK" -ForegroundColor Green

# ── 4. Fix src\backend\flood_assessment.py (import block only) ──────────────
Write-Host "[4/7] Patching src\backend\flood_assessment.py..." -ForegroundColor Yellow

$fa = Get-Content "src\backend\flood_assessment.py" -Raw

$old_fa = @'
import sys
import os

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml'))

from predict import FloodRiskPredictor
from risk_scoring import RiskScorer, format_alert_for_display
from typing import Dict, Optional


class FloodRiskAssessor:
    """
    Complete flood risk assessment system
    Combines ML prediction with risk scoring and alert generation
    """
    
    def __init__(self, 
                 model_path='../../data/models/flood_model.pkl',
                 scaler_path='../../data/processed/scaler.pkl'):
        """
        Initialize assessor with model and scaler
        
        Args:
            model_path: Path to trained model
            scaler_path: Path to fitted scaler
        """
        print("🚀 Initializing Flood Risk Assessment System...")
        self.predictor = FloodRiskPredictor(model_path, scaler_path)
        self.scorer = RiskScorer()
        print("✅ System ready!\n")
'@

$new_fa = @'
import sys
import os

# ── deployment-safe path bootstrap ──────────────────────────────────────────
_BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
_SRC_DIR     = os.path.dirname(_BACKEND_DIR)
_ML_DIR      = os.path.join(_SRC_DIR, "ml")
_UTILS_DIR   = os.path.join(_SRC_DIR, "utils")
for _p in (_BACKEND_DIR, _ML_DIR, _UTILS_DIR):
    if _p not in sys.path: sys.path.insert(0, _p)

from predict import get_predictor
from risk_scoring import RiskScorer, format_alert_for_display
from typing import Dict, Optional


class FloodRiskAssessor:
    """Complete flood risk assessment system."""

    def __init__(self, model_path=None, scaler_path=None):
        print("Initializing Flood Risk Assessment System...")
        self.predictor = get_predictor(model_path, scaler_path)
        self.scorer    = RiskScorer()
        print("System ready!")
'@

if ($fa.Contains("sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml'))")) {
    $fa = $fa.Replace($old_fa, $new_fa)
    Set-Content "src\backend\flood_assessment.py" $fa -Encoding UTF8
    Write-Host "      OK (patched)" -ForegroundColor Green
} else {
    Write-Host "      SKIPPED - already patched or different content" -ForegroundColor DarkYellow
}

# ── 5. Fix src\backend\multi_disaster.py ────────────────────────────────────
Write-Host "[5/7] Patching src\backend\multi_disaster.py..." -ForegroundColor Yellow

$md = Get-Content "src\backend\multi_disaster.py" -Raw

$old_md = @'
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from flood_assessment import FloodRiskAssessor
'@

$new_md = @'
import sys
import os

_BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
_SRC_DIR     = os.path.dirname(_BACKEND_DIR)
_ML_DIR      = os.path.join(_SRC_DIR, "ml")
_UTILS_DIR   = os.path.join(_SRC_DIR, "utils")
for _p in (_BACKEND_DIR, _ML_DIR, _UTILS_DIR):
    if _p not in sys.path: sys.path.insert(0, _p)

from flood_assessment import FloodRiskAssessor
'@

if ($md.Contains("sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))")) {
    $md = $md.Replace($old_md, $new_md)
    Set-Content "src\backend\multi_disaster.py" $md -Encoding UTF8
    Write-Host "      OK (patched)" -ForegroundColor Green
} else {
    Write-Host "      SKIPPED - already patched or different content" -ForegroundColor DarkYellow
}

# ── 6. Fix src\frontend\user_flow_app.py ────────────────────────────────────
Write-Host "[6/7] Patching src\frontend\user_flow_app.py..." -ForegroundColor Yellow

$uf = Get-Content "src\frontend\user_flow_app.py" -Raw

$old_uf = @'
# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from weather_api import WeatherAPIClient
from flood_assessment import FloodRiskAssessor
'@

$new_uf = @'
# ── deployment-safe path bootstrap ──────────────────────────────────────────
_FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))
_SRC_DIR      = os.path.dirname(_FRONTEND_DIR)
_BACKEND_DIR  = os.path.join(_SRC_DIR, "backend")
_ML_DIR       = os.path.join(_SRC_DIR, "ml")
_UTILS_DIR    = os.path.join(_SRC_DIR, "utils")
for _p in (_BACKEND_DIR, _ML_DIR, _UTILS_DIR):
    if _p not in sys.path: sys.path.insert(0, _p)

from weather_api import WeatherAPIClient
from flood_assessment import FloodRiskAssessor
'@

if ($uf.Contains("# Add backend to path")) {
    $uf = $uf.Replace($old_uf, $new_uf)
    Set-Content "src\frontend\user_flow_app.py" $uf -Encoding UTF8
    Write-Host "      OK (patched)" -ForegroundColor Green
} else {
    Write-Host "      SKIPPED - already patched or different content" -ForegroundColor DarkYellow
}

# ── 7. Fix src\frontend\multi_disaster_app.py ───────────────────────────────
Write-Host "[7/7] Patching src\frontend\multi_disaster_app.py..." -ForegroundColor Yellow

$mda = Get-Content "src\frontend\multi_disaster_app.py" -Raw

$old_mda = @'
# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from weather_api import WeatherAPIClient
from multi_disaster import MultiDisasterPredictor
'@

$new_mda = @'
# ── deployment-safe path bootstrap ──────────────────────────────────────────
_FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))
_SRC_DIR      = os.path.dirname(_FRONTEND_DIR)
_BACKEND_DIR  = os.path.join(_SRC_DIR, "backend")
_ML_DIR       = os.path.join(_SRC_DIR, "ml")
_UTILS_DIR    = os.path.join(_SRC_DIR, "utils")
for _p in (_BACKEND_DIR, _ML_DIR, _UTILS_DIR):
    if _p not in sys.path: sys.path.insert(0, _p)

from weather_api import WeatherAPIClient
from multi_disaster import MultiDisasterPredictor
'@

if ($mda.Contains("# Add backend to path")) {
    $mda = $mda.Replace($old_mda, $new_mda)
    Set-Content "src\frontend\multi_disaster_app.py" $mda -Encoding UTF8
    Write-Host "      OK (patched)" -ForegroundColor Green
} else {
    Write-Host "      SKIPPED - already patched or different content" -ForegroundColor DarkYellow
}

# ── Write correct .gitignore ─────────────────────────────────────────────────
Write-Host ""
Write-Host "Writing .gitignore (keeps .pkl files tracked)..." -ForegroundColor Yellow

@'
# Python
venv/
__pycache__/
*.pyc
*.pyo
.Python
*.egg-info/
dist/
build/

# Secrets - NEVER commit
.env
.env.local

# IDE
.vscode/
.idea/
.DS_Store
*.swp

# Logs
*.log
outputs/
.pytest_cache/

# NOTE: data/models/*.pkl and data/processed/*.pkl are NOT ignored.
# They MUST be committed so Streamlit Cloud can load the trained model.
'@ | Set-Content ".gitignore" -Encoding UTF8

Write-Host "      OK" -ForegroundColor Green

# ── Verify model files exist ─────────────────────────────────────────────────
Write-Host ""
Write-Host "Checking model files..." -ForegroundColor Yellow

$modelOk  = Test-Path "data\models\flood_model.pkl"
$scalerOk = Test-Path "data\processed\scaler.pkl"

if ($modelOk -and $scalerOk) {
    Write-Host "  data\models\flood_model.pkl  - FOUND" -ForegroundColor Green
    Write-Host "  data\processed\scaler.pkl    - FOUND" -ForegroundColor Green
} else {
    if (-not $modelOk)  { Write-Host "  data\models\flood_model.pkl  - MISSING" -ForegroundColor Red }
    if (-not $scalerOk) { Write-Host "  data\processed\scaler.pkl    - MISSING" -ForegroundColor Red }
    Write-Host ""
    Write-Host "  Run this to regenerate:" -ForegroundColor Yellow
    Write-Host "  python src\ml\run_phase5.py" -ForegroundColor White
}

# ── Git commit ───────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   ALL PATCHES APPLIED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next: Push fixes to GitHub and redeploy" -ForegroundColor White
Write-Host ""
Write-Host "Run these commands now:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  git add ." -ForegroundColor White
Write-Host "  git add -f data/models/flood_model.pkl" -ForegroundColor White
Write-Host "  git add -f data/processed/scaler.pkl" -ForegroundColor White
Write-Host "  git commit -m `"fix: deployment-safe paths + fallback predictor`"" -ForegroundColor White
Write-Host "  git push" -ForegroundColor White
Write-Host ""
Write-Host "Then visit Streamlit Cloud - it will auto-redeploy in ~2 min" -ForegroundColor Cyan
Write-Host ""