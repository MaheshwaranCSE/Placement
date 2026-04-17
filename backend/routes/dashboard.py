from flask import render_template
from flask_login import login_required, current_user
from backend.routes import dashboard_bp
from backend.models import User, Student, PlacementRecord, PredictionLog
from backend.extensions import db
from sqlalchemy import func

@dashboard_bp.route('/')
@login_required
def index():
    if current_user.role == 'admin':
        total_users = User.query.count()
        total_students = Student.query.count()
        
        placed_count = PlacementRecord.query.filter_by(status='placed').count()
        placement_percentage = (placed_count / total_students * 100) if total_students > 0 else 0
        
        recent_predictions = PredictionLog.query.order_by(PredictionLog.created_at.desc()).limit(10).all()
        
        return render_template('dashboard/admin.html', 
                               total_users=total_users, 
                               total_students=total_students, 
                               placement_percentage=round(placement_percentage, 1),
                               recent_predictions=recent_predictions)
                               
    elif current_user.role == 'faculty':
        # Assuming faculty might be assigned to specific departments later. For now, show all or global summary.
        total_students = Student.query.count()
        placed = PlacementRecord.query.filter_by(status='placed').count()
        
        return render_template('dashboard/faculty.html',
                               total_students=total_students,
                               placed=placed)
                               
    else:  # student
        student = Student.query.filter_by(user_id=current_user.id).first()
        latest_prediction = None
        placement_status = None
        
        if student:
            latest_prediction = PredictionLog.query.filter_by(student_id=student.id).order_by(PredictionLog.created_at.desc()).first()
            placement = PlacementRecord.query.filter_by(student_id=student.id).order_by(PlacementRecord.created_at.desc()).first()
            if placement:
                placement_status = placement.status
                
        return render_template('dashboard/student.html', 
                               student=student, 
                               latest_prediction=latest_prediction, 
                               placement_status=placement_status)
