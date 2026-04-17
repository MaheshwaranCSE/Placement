import pytest
import os
from backend.app import create_app
from backend.extensions import db as _db
from backend.models import User, Student, PlacementRecord

@pytest.fixture(scope='session')
def app():
    # Set testing env vars
    os.environ['FLASK_ENV'] = 'test'
    os.environ['SECRET_KEY'] = 'test-secret'
    
    app = create_app('test')
    
    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()

@pytest.fixture(scope='session')
def db(app):
    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()

@pytest.fixture(autouse=True)
def clean_db(db):
    """Clean the db before each test."""
    db.session.rollback()
    
    # Delete in reverse dependency order
    PlacementRecord.query.delete()
    Student.query.delete()
    User.query.delete()
    db.session.commit()

@pytest.fixture
def client(app, clean_db):
    return app.test_client()

@pytest.fixture
def admin_user(db):
    u = User(username='testadmin', email='admin@test.com', password='password@123', role='admin')
    db.session.add(u)
    db.session.commit()
    return u

@pytest.fixture
def faculty_user(db):
    u = User(username='testfaculty', email='faculty@test.com', password='password@123', role='faculty')
    db.session.add(u)
    db.session.commit()
    return u

@pytest.fixture
def test_student(db, faculty_user):
    s = Student(roll_number='TEST001', name='Test Student', department='CSE', cgpa=8.0)
    db.session.add(s)
    db.session.commit()
    return s
