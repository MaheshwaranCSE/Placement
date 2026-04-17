from datetime import datetime
from backend.extensions import db

class PlacementRecord(db.Model):
    __tablename__ = 'placement_records'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    company = db.Column(db.String(100), nullable=True)
    role_offered = db.Column(db.String(100), nullable=True)
    offer_date = db.Column(db.Date, nullable=True)
    joining_date = db.Column(db.Date, nullable=True)
    package_lpa = db.Column(db.Numeric(5, 2), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    
    # Check in: 'placed', 'not_placed', 'waiting', 'internship', 'ppo', 'rejected'
    status = db.Column(db.String(20), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PlacementRecord {self.company} for Student {self.student_id}>"
