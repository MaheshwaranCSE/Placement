from backend.extensions import celery, db
from backend.models import Student, PredictionLog
from backend.services.ml_predict import extract_features, get_model
import pandas as pd

@celery.task(bind=True, max_retries=3)
def predict_student_placement(self, student_id, model_version="v1.0"):
    try:
        # Need application context for DB access
        from backend.app import create_app
        app = create_app()
        
        with app.app_context():
            student = Student.query.get(student_id)
            if not student:
                return {"status": "error", "message": "Student not found"}
                
            features = extract_features(student)
            model = get_model()
            
            if model:
                df = pd.DataFrame([features])
                probability = float(model.predict_proba(df)[0][1])
                predicted_class = bool(model.predict(df)[0])
                version = "v1.0-pkl"
            else:
                probability = 0.5
                predicted_class = False
                version = "fallback-no-model"
                
            log = PredictionLog(
                student_id=student.id,
                predicted_probability=probability,
                predicted_class=predicted_class,
                input_features=features,
                model_version=version
            )
            db.session.add(log)
            db.session.commit()
            
            return {
                "status": "success", 
                "student_id": student.id, 
                "probability": probability,
                "class": predicted_class
            }
            
    except Exception as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60)

@celery.task
def batch_predict_department(department, model_version="v1.0"):
    # Stub for batch predictions
    return {"status": "queued"}

@celery.task
def retrain_model(dataset_path):
    # Stub for triggering ml/train_model.py
    return {"status": "queued"}
