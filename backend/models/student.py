from datetime import datetime
from backend.extensions import db
from sqlalchemy.dialects.postgresql import ARRAY

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    roll_number = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    department = db.Column(db.String(50), nullable=True)
    batch_year = db.Column(db.Integer, nullable=True)
    cgpa = db.Column(db.Numeric(3, 2), nullable=True)
    backlogs = db.Column(db.Integer, default=0)
    internships = db.Column(db.Integer, default=0)
    projects = db.Column(db.Integer, default=0)
    
    # Store skills as an array of strings in postgres, falls back beautifully with SQLAlchemy
    skills = db.Column(db.ARRAY(db.String) if hasattr(db, 'ARRAY') else db.JSON, nullable=True)
    
    communication_score = db.Column(db.Integer, nullable=True) # Check 0-10 handled in code
    aptitude_score = db.Column(db.Integer, nullable=True)      # Check 0-10 handled in code
    extra_curricular = db.Column(db.Text, nullable=True)
    linkedin_url = db.Column(db.String(200), nullable=True)
    github_url = db.Column(db.String(200), nullable=True)
    resume_path = db.Column(db.String(300), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    placement_records = db.relationship('PlacementRecord', backref='student', lazy=True, cascade='all, delete-orphan')
    prediction_logs = db.relationship('PredictionLog', backref='student', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Student {self.roll_number} - {self.name}>"
