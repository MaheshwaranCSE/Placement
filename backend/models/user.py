from datetime import datetime
from backend.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    students = db.relationship('Student', backref='user_account', lazy=True)
    placement_records = db.relationship('PlacementRecord', backref='creator', lazy=True)
    audit_logs = db.relationship('AuditLog', backref='user', lazy=True)
    prediction_logs = db.relationship('PredictionLog', backref='trigger_user', lazy=True)

    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.set_password(password)
        
        if role not in ['admin', 'faculty', 'student']:
            raise ValueError("Role must be admin, faculty, or student")
        self.role = role

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username} (Role: {self.role})>"
