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
