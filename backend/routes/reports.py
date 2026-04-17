from flask import render_template
from flask_login import login_required
from backend.routes import reports_bp
from backend.decorators import faculty_required
from backend.models import Student, PlacementRecord
from sqlalchemy import func
from backend.extensions import db

@reports_bp.route('/reports')
@login_required
@faculty_required
def index():
    # Example aggregate queries for Chart.js
    
    # Department breakdown
    dept_stats_query = db.session.query(
        Student.department, 
        func.count(Student.id).label('total')
    ).group_by(Student.department).all()
    
    dept_stats = {d[0] or 'Unknown': d[1] for d in dept_stats_query}
    
    # Placement status overall
    status_stats_query = db.session.query(
        PlacementRecord.status,
        func.count(PlacementRecord.id).label('total')
    ).group_by(PlacementRecord.status).all()
    
    status_stats = {s[0] or 'Unknown': s[1] for s in status_stats_query}
    
    # Top companies
    top_companies_query = db.session.query(
        PlacementRecord.company,
        func.count(PlacementRecord.id).label('offers'),
        func.avg(PlacementRecord.package_lpa).label('avg_package')
    ).group_by(PlacementRecord.company).order_by(func.count(PlacementRecord.id).desc()).limit(10).all()
    
    top_companies = [
        {"company": r[0] or "Unknown", "offers": r[1], "avg_package": round(r[2] or 0, 2)} 
        for r in top_companies_query
    ]

    return render_template('reports/index.html', 
                           dept_stats=dept_stats, 
                           status_stats=status_stats,
                           top_companies=top_companies)
