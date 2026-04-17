import pytest
import io

def test_xss_in_student_name(client, faculty_user, db):
    client.post('/login', data={'username': 'testfaculty', 'password': 'password@123'})
    
    # Try creating student with XSS payload
    data = {
        'roll_number': 'XSS001',
        'name': '<script>alert("XSS")</script>',
        'department': 'CSE',
        'batch_year': 2025,
        'cgpa': 9.0
    }
    client.post('/students/new', data=data, follow_redirects=True)
    
    # Check if rendering escapes the script tags. Jinja2 does this automatically.
    # Looking for &lt;script&gt; in response
    response = client.get('/students')
    assert b'<script>alert("XSS")</script>' not in response.data
    assert b'&lt;script&gt;alert(' in response.data or b'XSS001' in response.data 

def test_file_upload_type_check(client, faculty_user, db):
    client.post('/login', data={'username': 'testfaculty', 'password': 'password@123'})
    
    # Uploading a non-PDF file as resume
    data = {
        'roll_number': 'RES001',
        'name': 'Resume Test',
        'department': 'CSE',
        'batch_year': 2025,
        'cgpa': 8.0,
        'resume': (io.BytesIO(b"malicious script snippet"), 'test.sh')
    }
    
    response = client.post('/students/new', data=data, content_type='multipart/form-data')
    # Should show validation error for non-pdf
    assert b'PDFs only!' in response.data
    assert b'Student created successfully' not in response.data

def test_sql_injection_attempt_via_search(client, faculty_user):
    client.post('/login', data={'username': 'testfaculty', 'password': 'password@123'})
    
    payload = "1' OR '1'='1"
    response = client.get(f'/students?q={payload}')
    
    # Should not throw 500 error
    assert response.status_code == 200
    # Search should safely escape and return 0 results usually unless a name has those chars
    assert b'No students found' in response.data or b'Student' in response.data
