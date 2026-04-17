import pytest
import json

def test_api_auth_token(client, faculty_user):
    response = client.post('/api/v1/auth/token', json={
        'username': 'testfaculty',
        'password': 'password@123'
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data

def test_api_auth_token_invalid(client, faculty_user):
    response = client.post('/api/v1/auth/token', json={
        'username': 'testfaculty',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 401

def test_api_get_students_requires_auth(client):
    response = client.get('/api/v1/students')
    assert response.status_code == 401

def test_api_get_students(client, faculty_user, test_student):
    # Get token
    auth_resp = client.post('/api/v1/auth/token', json={
        'username': 'testfaculty',
        'password': 'password@123'
    })
    token = json.loads(auth_resp.data)['access_token']
    
    # Get students
    response = client.get('/api/v1/students', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'items' in data
    assert len(data['items']) > 0
    assert data['items'][0]['roll_number'] == 'TEST001'
