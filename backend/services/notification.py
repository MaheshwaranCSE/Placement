from flask_mail import Message
from flask import render_template
from backend.extensions import celery, mail
from flask import current_app

@celery.task
def send_prediction_result(student_email, probability, recommendation):
    """Stub: Send prediction result email."""
    print(f"Would send email to {student_email} with prob: {probability}")
    # msg = Message("Prediction Result", sender=current_app.config['MAIL_USERNAME'], recipients=[student_email])
    # msg.html = render_template('email/prediction_result.html', probability=probability, recommendation=recommendation)
    # mail.send(msg)

@celery.task
def send_placement_notification(student_email, company, package, status):
    """Stub: Notification on placement status update."""
    print(f"Would notify {student_email} about {company} - {status}")

@celery.task
def send_weekly_report(admin_email, stats_dict):
    """Stub: Weekly summary."""
    pass

@celery.task
def send_import_complete(faculty_email, total, success, failed_count):
    """Stub: Import completion notification."""
    pass
