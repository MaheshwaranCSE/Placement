import csv
import io
from backend.models import Student, PlacementRecord

def generate_student_csv(department=None):
    """Generates CSV string format of students and their latest placement status."""
    
    query = Student.query
    if department:
        query = query.filter_by(department=department)
        
    students = query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow([
        'Roll Number', 'Name', 'Email', 'Department', 'Batch Year',
        'CGPA', 'Backlogs', 'Skills', 'Placement Status'
    ])
    
    for s in students:
        # Get latest placement status
        placement = PlacementRecord.query.filter_by(student_id=s.id).order_by(PlacementRecord.created_at.desc()).first()
        status = placement.status if placement else 'Unknown'
        
        skills_str = ';'.join(s.skills) if s.skills else ''
        
        writer.writerow([
            s.roll_number,
            s.name,
            s.email,
            s.department,
            s.batch_year,
            float(s.cgpa) if s.cgpa else '',
            s.backlogs,
            skills_str,
            status
        ])
        
    return output.getvalue()
