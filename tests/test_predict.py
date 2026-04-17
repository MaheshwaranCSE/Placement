import pytest
from backend.services.ml_predict import extract_features, sync_predict

def test_extract_features(test_student):
    features = extract_features(test_student)
    assert features['cgpa'] == 8.0
    assert features['department'] == 'CSE'
    assert features['backlog_count'] == 0

def test_sync_predict_fallback(test_student):
    # Without model, should return fallback heuristic
    result = sync_predict(test_student)
    assert 'probability' in result
    assert 'class' in result
    assert result['version'] == 'rule-based-fallback'
    
def test_predict_route_requires_auth(client, test_student):
    response = client.post(f'/predict/{test_student.id}')
    # Redirects to login
    assert response.status_code == 302
    assert '/login' in response.headers.get('Location')

def test_predict_task_queued(client, faculty_user, test_student):
    client.post('/login', data={'username': 'testfaculty', 'password': 'password@123'})
    response = client.post(f'/predict/{test_student.id}')
    # Currently redirects back to student detail after queueing
    assert response.status_code == 302
    assert f'/students/{test_student.id}' in response.headers.get('Location')
