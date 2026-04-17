from flask import Blueprint

# Initialize all blueprints here
auth_bp = Blueprint('auth', __name__)
dashboard_bp = Blueprint('dashboard', __name__)
students_bp = Blueprint('students', __name__)
placement_bp = Blueprint('placement', __name__)
predict_bp = Blueprint('predict', __name__)
reports_bp = Blueprint('reports', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Import routes to register them with the blueprints
from . import auth, dashboard, students, placement, predict, reports, api
