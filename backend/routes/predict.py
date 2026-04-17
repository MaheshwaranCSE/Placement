from flask import jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user
from backend.routes import predict_bp
from backend.models import Student, AuditLog
from backend.extensions import db
from backend.decorators import faculty_required
from backend.services.ml_tasks import predict_student_placement

@predict_bp.route('/predict/<int:student_id>', methods=['POST'])
@login_required
@faculty_required
def trigger_prediction(student_id):
    student = Student.query.get_or_404(student_id)
    
    # Trigger Celery task
    task = predict_student_placement.delay(student_id, "v1.0") # Hardcoded version, can read from metadata
    
    audit = AuditLog(user_id=current_user.id, action='prediction.run', target_type='student', target_id=student.id, ip_address=request.remote_addr)
    db.session.add(audit)
    db.session.commit()
    
    if request.headers.get('HX-Request'):
        return jsonify({"status": "Accepted", "task_id": task.id}), 202
        
    flash('Prediction task queued successfully.', 'info')
    return redirect(url_for('students.detail', id=student.id))
