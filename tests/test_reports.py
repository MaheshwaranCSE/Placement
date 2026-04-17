import pytest
from backend.models import PlacementRecord

def test_reports_page_calculates_stats(client, faculty_user, test_student, db):
    # Add a placement record to ensure calculations run
    import datetime
    pr = PlacementRecord(
        student_id=test_student.id,
        company="Test Corp",
        package_lpa=10.5,
        status="placed",
        created_at=datetime.datetime.utcnow()
    )
    db.session.add(pr)
    db.session.commit()
    
    client.post('/login', data={'username': 'testfaculty', 'password': 'password@123'})
    response = client.get('/reports')
    
    assert response.status_code == 200
    assert b'Placement Reports' in response.data
    # Check that javascript vars for reports get injected
    assert b'Test Corp' in response.data
    assert b'10.50 LPA' in response.data
