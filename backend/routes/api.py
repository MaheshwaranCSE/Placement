from flask import jsonify, request
from backend.routes import api_bp
from backend.models import User, Student, PlacementRecord
from backend.extensions import db, limiter
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@api_bp.route('/auth/token', methods=['POST'])
@limiter.limit("10 per minute")
def get_token():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"msg": "Missing username or password"}), 400
        
    user = User.query.filter_by(username=data.get('username')).first()
    if user and user.check_password(data.get('password')):
        if not user.is_active:
            return jsonify({"msg": "Account deactivated"}), 403
            
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
        
    return jsonify({"msg": "Bad username or password"}), 401

@api_bp.route('/students', methods=['GET'])
@jwt_required()
@limiter.limit("100 per hour")
def get_students():
    page = request.args.get('page', 1, type=int)
    pagination = Student.query.paginate(page=page, per_page=25, error_out=False)
    
    students_data = []
    for s in pagination.items:
        students_data.append({
            "id": s.id,
            "roll_number": s.roll_number,
            "name": s.name,
            "department": s.department,
            "cgpa": float(s.cgpa) if s.cgpa else None
        })
        
    return jsonify({
        "items": students_data,
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": page
    }), 200

# Additional stubs for other endpoints as requested
@api_bp.route('/students', methods=['POST'])
@jwt_required()
def create_student():
    return jsonify({"msg": "Not implemented yet"}), 501

@api_bp.route('/predict/status/<task_id>', methods=['GET'])
@jwt_required()
def get_prediction_status(task_id):
    from backend.services.ml_tasks import predict_student_placement
    task = predict_student_placement.AsyncResult(task_id)
    if task.state == 'PENDING':
        return jsonify({"state": task.state, "status": "Pending..."})
    elif task.state != 'FAILURE':
        return jsonify({"state": task.state, "result": task.result})
    else:
        return jsonify({"state": task.state, "status": str(task.info)})
