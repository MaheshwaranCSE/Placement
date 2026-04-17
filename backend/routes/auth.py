from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from backend.routes import auth_bp
from backend.forms import LoginForm, ChangePasswordForm
from backend.models import User, AuditLog
from backend.extensions import db, limiter

@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Account is deactivated. Contact Admin.', 'danger')
                return render_template('auth/login.html', form=form)

            login_user(user, remember=True)
            
            # Log successful login
            audit = AuditLog(user_id=user.id, action='auth.login', target_type='user', target_id=user.id, ip_address=request.remote_addr)
            db.session.add(audit)
            db.session.commit()
            
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))
            
        flash('Invalid username or password', 'danger')
        
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    audit = AuditLog(user_id=current_user.id, action='auth.logout', target_type='user', target_id=current_user.id, ip_address=request.remote_addr)
    db.session.add(audit)
    db.session.commit()
    
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.new_password.data)
            
            audit = AuditLog(user_id=current_user.id, action='auth.change_password', target_type='user', target_id=current_user.id, ip_address=request.remote_addr)
            db.session.add(audit)
            db.session.commit()
            
            flash('Password successfully updated.', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Incorrect current password.', 'danger')
            
    return render_template('auth/change_password.html', form=form)
