import os
from flask import render_template, redirect, url_for, flash, request, current_app, Response
from flask_login import login_required, current_user
from backend.routes import students_bp
from backend.forms import StudentForm, ImportForm
from backend.models import Student, AuditLog
from backend.extensions import db
from backend.decorators import faculty_required
from backend.services.export import generate_student_csv

@students_bp.route('/students')
@login_required
@faculty_required
def list_students():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('q', '')
    department = request.args.get('dept', '')
    
    query = Student.query
    
    if search:
        query = query.filter(db.or_(
            Student.name.ilike(f'%{search}%'),
            Student.roll_number.ilike(f'%{search}%')
        ))
    if department:
        query = query.filter(Student.department == department)
        
    pagination = query.order_by(Student.roll_number).paginate(page=page, per_page=25, error_out=False)
    
    if request.headers.get('HX-Request'):
        return render_template('students/_list_partial.html', students=pagination.items, pagination=pagination)
        
    return render_template('students/list.html', students=pagination.items, pagination=pagination, search=search, dept=department)

@students_bp.route('/students/new', methods=['GET', 'POST'])
@login_required
@faculty_required
def create():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(
            roll_number=form.roll_number.data,
            name=form.name.data,
            email=form.email.data,
            department=form.department.data,
            batch_year=form.batch_year.data,
            cgpa=form.cgpa.data,
            backlogs=form.backlogs.data or 0,
            internships=form.internships.data or 0,
            projects=form.projects.data or 0,
            skills=[s.strip() for s in form.skills.data.split(',')] if form.skills.data else [],
            communication_score=form.communication_score.data,
            aptitude_score=form.aptitude_score.data,
            extra_curricular=form.extra_curricular.data,
            linkedin_url=form.linkedin_url.data,
            github_url=form.github_url.data
        )
        
        if form.resume.data:
            filename = f"{student.roll_number}_resume.pdf"
            upload_path = os.path.join(current_app.root_path, '../uploads', filename)
            form.resume.data.save(upload_path)
            student.resume_path = filename
            
        db.session.add(student)
        db.session.flush() # to get id
        
        audit = AuditLog(user_id=current_user.id, action='student.create', target_type='student', target_id=student.id, ip_address=request.remote_addr)
        db.session.add(audit)
        db.session.commit()
        
        flash('Student created successfully.', 'success')
        return redirect(url_for('students.detail', id=student.id))
        
    return render_template('students/form.html', form=form, title="Add New Student")

@students_bp.route('/students/<int:id>')
@login_required
def detail(id):
    student = Student.query.get_or_404(id)
    
    # Students can only view their own profile
    if current_user.role == 'student' and student.user_id != current_user.id:
        from flask import abort
        abort(403)
        
    return render_template('students/detail.html', student=student)

@students_bp.route('/students/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@faculty_required
def edit(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    
    if request.method == 'GET':
        if student.skills:
            form.skills.data = ', '.join(student.skills)
            
    if form.validate_on_submit():
        form.populate_obj(student)
        if form.skills.data:
            student.skills = [s.strip() for s in form.skills.data.split(',')]
            
        if form.resume.data:
            filename = f"{student.roll_number}_resume.pdf"
            upload_path = os.path.join(current_app.root_path, '../uploads', filename)
            form.resume.data.save(upload_path)
            student.resume_path = filename
            
        audit = AuditLog(user_id=current_user.id, action='student.update', target_type='student', target_id=student.id, ip_address=request.remote_addr)
        db.session.add(audit)
        db.session.commit()
        
        flash('Student updated successfully.', 'success')
        return redirect(url_for('students.detail', id=student.id))
        
    return render_template('students/form.html', form=form, title="Edit Student", student=student)

@students_bp.route('/students/export')
@login_required
@faculty_required
def export():
    department = request.args.get('dept', '')
    csv_data = generate_student_csv(department)
    
    audit = AuditLog(user_id=current_user.id, action='student.export', target_type='bulk', ip_address=request.remote_addr)
    db.session.add(audit)
    db.session.commit()
    
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=students_export.csv"}
    )
