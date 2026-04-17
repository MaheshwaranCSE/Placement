from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from backend.routes import placement_bp
from backend.forms import PlacementForm
from backend.models import PlacementRecord, Student, AuditLog
from backend.extensions import db
from backend.decorators import faculty_required

@placement_bp.route('/placement')
@login_required
@faculty_required
def list_records():
    page = request.args.get('page', 1, type=int)
    records = PlacementRecord.query.order_by(PlacementRecord.created_at.desc()).paginate(page=page, per_page=25, error_out=False)
    return render_template('placement/list.html', records=records.items, pagination=records)

@placement_bp.route('/placement/new/<int:student_id>', methods=['GET', 'POST'])
@login_required
@faculty_required
def create(student_id):
    student = Student.query.get_or_404(student_id)
    form = PlacementForm()
    
    if form.validate_on_submit():
        record = PlacementRecord(
            student_id=student.id,
            company=form.company.data,
            role_offered=form.role_offered.data,
            package_lpa=form.package_lpa.data,
            location=form.location.data,
            status=form.status.data,
            notes=form.notes.data,
            created_by=current_user.id
        )
        
        # Handle optional dates properly
        from datetime import datetime
        if form.offer_date.data:
             record.offer_date = datetime.strptime(form.offer_date.data, '%Y-%m-%d').date()
        if form.joining_date.data:
             record.joining_date = datetime.strptime(form.joining_date.data, '%Y-%m-%d').date()
             
        db.session.add(record)
        
        audit = AuditLog(user_id=current_user.id, action='placement.create', target_type='placement_record', ip_address=request.remote_addr)
        db.session.add(audit)
        db.session.commit()
        
        flash('Placement record added successfully.', 'success')
        return redirect(url_for('students.detail', id=student.id))
        
    return render_template('placement/form.html', form=form, student=student)
