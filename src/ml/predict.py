import os, sys, pandas as pd

# Compute absolute model paths directly - no imports needed
_ML_DIR      = os.path.dirname(os.path.abspath(__file__))
_SRC_DIR     = os.path.dirname(_ML_DIR)
_PROJECT_ROOT = os.path.dirname(_SRC_DIR)
MODEL_PATH   = os.path.join(_PROJECT_ROOT, "data", "models",    "flood_model.pkl")
SCALER_PATH  = os.path.join(_PROJECT_ROOT, "data", "processed", "scaler.pkl")

# Make sure schema.py (in same folder) is importable
if _ML_DIR not in sys.path:
    sys.path.insert(0, _ML_DIR)

from schema import FEATURE_NAMES, get_risk_info


class FloodRiskPredictor:
    def __init__(self, model_path=None, scaler_path=None):
        import joblib
        mp = model_path  or MODEL_PATH
        sp = scaler_path or SCALER_PATH
        if not os.path.isfile(mp):
            raise FileNotFoundError(f"Model not found: {mp}")
        if not os.path.isfile(sp):
            raise FileNotFoundError(f"Scaler not found: {sp}")
        self.model  = joblib.load(mp)
        self.scaler = joblib.load(sp)
        print(f"[OK] Model  : {mp}")
        print(f"[OK] Scaler : {sp}")

    def _prep(self, d):
        df = pd.DataFrame([d])[FEATURE_NAMES]
        return pd.DataFrame(self.scaler.transform(df), columns=FEATURE_NAMES)

    def predict_single(self, features_dict):
        df    = self._prep(features_dict)
        level = int(self.model.predict(df)[0])
        probs = self.model.predict_proba(df)[0]
        info  = get_risk_info(level)
        return {
            "risk_level":  level,
            "risk_label":  info["label"],
            "risk_color":  info["color"],
            "probability": float(probs[level]),
            "probabilities": {
                "safe":      float(probs[0]),
                "warning":   float(probs[1]),
                "high_risk": float(probs[2]),
                "critical":  float(probs[3]),
            },
            "description":        info["description"],
            "recommended_action": info["action"],
        }

    def predict_with_explanation(self, features_dict):
        r = self.predict_single(features_dict)
        flags = []
        if features_dict.get("rainfall_mm", 0) > 200:
            flags.append(f"Heavy rain: {features_dict['rainfall_mm']:.1f} mm")
        if features_dict.get("river_level_m", 0) > 10:
            flags.append(f"Danger river level: {features_dict['river_level_m']:.1f} m")
        if features_dict.get("soil_moisture_percent", 0) > 85:
            flags.append(f"Soil saturated: {features_dict['soil_moisture_percent']:.1f}%")
        if features_dict.get("distance_to_river_km", 99) < 1:
            flags.append(f"Very close to river: {features_dict['distance_to_river_km']:.2f} km")
        r["critical_features"] = flags
        r["input_features"]    = features_dict
        return r

    def predict_batch(self, features_df):
        df  = features_df[FEATURE_NAMES]
        s   = pd.DataFrame(self.scaler.transform(df), columns=FEATURE_NAMES, index=df.index)
        lv  = self.model.predict(s)
        pr  = self.model.predict_proba(s)
        out = features_df.copy()
        out["predicted_risk_level"]   = lv
        out["prediction_probability"] = [p[l] for p, l in zip(pr, lv)]
        out["risk_label"] = out["predicted_risk_level"].map(
            {0: "Safe", 1: "Warning", 2: "High Risk", 3: "Critical"})
        return out


class FallbackFloodPredictor:
    """Rule-based predictor - used when .pkl files are missing."""
    _L = ["Safe", "Warning", "High Risk", "Critical"]
    _C = ["green", "yellow", "orange", "red"]
    _D = ["Low flood risk. Normal conditions.",
          "Moderate risk. Monitor conditions closely.",
          "High risk. Take precautions immediately.",
          "Critical risk. Evacuate flood-prone areas now."]
    _A = ["Stay alert to weather updates.",
          "Prepare emergency supplies. Avoid low-lying areas.",
          "Move valuables to higher ground. Ready to evacuate.",
          "Evacuate immediately. Follow emergency services."]

    def __init__(self, *a, **k):
        print("[WARN] ML model not found - using rule-based fallback predictor.")

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

    def _p(self, lv):
        p = [0.25/3]*4; p[lv] = 0.75; return p

    def predict_single(self, fd):
        lv = self._score(fd); p = self._p(lv)
        return {"risk_level": lv, "risk_label": self._L[lv], "risk_color": self._C[lv],
                "probability": p[lv],
                "probabilities": {"safe":p[0],"warning":p[1],"high_risk":p[2],"critical":p[3]},
                "description": self._D[lv], "recommended_action": self._A[lv],
                "_fallback": True}

    def predict_with_explanation(self, fd):
        r = self.predict_single(fd); flags = []
        if fd.get("rainfall_mm", 0) > 200:
            flags.append(f"Heavy rain: {fd['rainfall_mm']:.1f} mm")
        if fd.get("river_level_m", 0) > 10:
            flags.append(f"Danger river level: {fd['river_level_m']:.1f} m")
        r["critical_features"] = flags; r["input_features"] = fd
        return r

    def predict_batch(self, df):
        out = df.copy()
        out["predicted_risk_level"]   = df.apply(lambda r: self._score(r.to_dict()), axis=1)
        out["prediction_probability"] = 0.75
        out["risk_label"] = out["predicted_risk_level"].map(
            {0:"Safe",1:"Warning",2:"High Risk",3:"Critical"})
        return out


def get_predictor(model_path=None, scaler_path=None):
    """Always returns a working predictor - ML model if available, fallback otherwise."""
    try:
        return FloodRiskPredictor(model_path, scaler_path)
    except FileNotFoundError as e:
        print(f"[predict] {e}")
        return FallbackFloodPredictor()
