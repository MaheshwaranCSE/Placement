import pytest

def test_login_page_renders(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_login_success(client, faculty_user):
    # Need to simulate CSRF or disable it for tests. conftest disables it.
    response = client.post('/login', data={'username': 'testfaculty', 'password': 'password@123'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Logout' in response.data

def test_login_failure(client, faculty_user):
    response = client.post('/login', data={'username': 'testfaculty', 'password': 'wrongpassword'})
    assert b'Invalid username or password' in response.data

def test_logout(client, faculty_user):
    client.post('/login', data={'username': 'testfaculty', 'password': 'password@123'})
    response = client.get('/logout', follow_redirects=True)
    assert b'You have been logged out.' in response.data
    assert b'Login' in response.data

def test_role_redirect_student_accessing_faculty_route(client, faculty_user, db):
    from backend.models import User
    stu = User(username='stu1', email='stu@stu.com', password='pwd', role='student')
    db.session.add(stu)
    db.session.commit()
    
    client.post('/login', data={'username': 'stu1', 'password': 'pwd'})
    response = client.get('/students')
    # Should be forbidden for students to access list all students
    assert response.status_code == 403
