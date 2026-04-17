import os
from backend.app import create_app
from backend.extensions import db
from backend.models import User, Student

app = create_app(os.getenv('FLASK_ENV', 'development'))

def create_admin():
    with app.app_context():
        admin_pass = os.getenv('ADMIN_PASSWORD', 'admin123#Secure')
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@college.edu', password=admin_pass, role='admin')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists.")

def seed():
    with app.app_context():
        db.create_all()
        create_admin()
        
        # Add faculty
        for dept in ['CSE', 'ECE']:
            username = f'faculty_{dept.lower()}'
            if not User.query.filter_by(username=username).first():
                f = User(username=username, email=f'{username}@college.edu', password='faculty#Password1', role='faculty')
                db.session.add(f)
                
        # Add a sample student
        if not Student.query.filter_by(roll_number='23CSE101').first():
            s = Student(roll_number='23CSE101', name='John Doe', department='CSE', batch_year=2026, cgpa=8.5)
            db.session.add(s)
            
        db.session.commit()
        print("Database seeded successfully with initial data.")
        print("\nLogin Instructions:")
        print("Admin: 'admin' / (password from ADMIN_PASSWORD env or 'admin123#Secure')")
        print("Faculty: 'faculty_cse' / 'faculty#Password1'")

if __name__ == '__main__':
    seed()
