from datetime import datetime
from backend.extensions import db

class PredictionLog(db.Model):
    __tablename__ = 'prediction_logs'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=True)
    predicted_probability = db.Column(db.Numeric(5, 4), nullable=True)
    predicted_class = db.Column(db.Boolean, nullable=True)
    
    # Store input features as JSON
    input_features = db.Column(db.JSON, nullable=True)
    
    model_version = db.Column(db.String(50), nullable=True)
    triggered_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PredictionLog for Student {self.student_id}>"
