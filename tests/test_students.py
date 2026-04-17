import pytest
from backend.models import Student

def test_student_list_access(client, faculty_user):
    client.post('/login', data={'username': 'testfaculty', 'password': 'password@123'})
    response = client.get('/students')
    assert response.status_code == 200

def test_student_create(client, faculty_user, db):
    client.post('/login', data={'username': 'testfaculty', 'password': 'password@123'})
    
    data = {
        'roll_number': '12345',
        'name': 'New Student',
        'department': 'CSE',
        'batch_year': 2025,
        'cgpa': 9.1
    }
    response = client.post('/students/new', data=data, follow_redirects=True)
    assert response.status_code == 200
    
    s = Student.query.filter_by(roll_number='12345').first()
    assert s is not None
    assert s.name == 'New Student'
    assert s.cgpa == 9.1

def test_student_export(client, faculty_user, test_student):
    client.post('/login', data={'username': 'testfaculty', 'password': 'password@123'})
    response = client.get('/students/export')
    assert response.status_code == 200
    assert response.headers['Content-disposition'].startswith('attachment; filename=students_export.csv')
    assert b'TEST001' in response.data
    assert b'Test Student' in response.data
