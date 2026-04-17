import os
import joblib
import pandas as pd
from backend.models import Student

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../ml/placement_model.pkl')

# Cache the loaded model to avoid reloading on every sync call
_model = None

def get_model():
    global _model
    if _model is None:
        if os.path.exists(MODEL_PATH):
            _model = joblib.load(MODEL_PATH)
    return _model

def extract_features(student: Student):
    """
    Extract features from Student DB model into a dictionary 
    that matches the model's expected inputs.
    """
    return {
        "department": student.department or "Unknown",
        "cgpa": float(student.cgpa) if student.cgpa else 0.0,
        "backlog_count": student.backlogs or 0,
        "communication_score": student.communication_score or 0,
        "aptitude_score": student.aptitude_score or 0,
        "internships": student.internships or 0,
        "projects": student.projects or 0
    }

def sync_predict(student: Student):
    """
    Synchronous fallback prediction if Celery is not used.
    """
    model = get_model()
    if not model:
        # Fallback heuristic if model is missing
        prob = 0.5
        if student.cgpa and student.cgpa > 8.0 and not student.backlogs:
            prob = 0.8
        return {"probability": prob, "class": prob > 0.5, "version": "rule-based-fallback"}
        
    features = extract_features(student)
    df = pd.DataFrame([features])
    
    # Needs to match preprocessing in ml/preprocess.py
    # Assuming the pipeline handles categorical encoding internally:
    try:
        prob = model.predict_proba(df)[0][1] # Probability of positive class
        pred = model.predict(df)[0]
        return {"probability": float(prob), "class": bool(pred), "version": "v1.0-pkl"}
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Prediction failed: {e}")
        return {"probability": 0.0, "class": False, "version": "error"}
