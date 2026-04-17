import pandas as pd
from backend.models import Student
from backend.extensions import db

def process_import_file(filepath):
    """
    Parses CSV/Excel, validates required columns, and upserts students.
    Returns (success_count, fail_count, list_of_errors)
    """
    try:
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
            
        required_cols = ['roll_number', 'name', 'department', 'cgpa']
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            return 0, 0, [f"Missing required columns: {', '.join(missing)}"]
            
        success = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                roll_no = str(row['roll_number']).strip()
                if not roll_no:
                    continue
                    
                student = Student.query.filter_by(roll_number=roll_no).first()
                if not student:
                    student = Student(roll_number=roll_no)
                    db.session.add(student)
                    
                student.name = str(row.get('name', ''))
                student.department = str(row.get('department', ''))
                student.cgpa = float(row.get('cgpa', 0.0))
                
                # Optional fields
                if 'email' in df.columns and pd.notna(row['email']):
                    student.email = str(row['email'])
                if 'batch_year' in df.columns and pd.notna(row['batch_year']):
                    student.batch_year = int(row['batch_year'])
                if 'backlogs' in df.columns and pd.notna(row['backlogs']):
                    student.backlogs = int(row['backlogs'])
                if 'skills' in df.columns and pd.notna(row['skills']):
                    student.skills = [s.strip() for s in str(row['skills']).split(';')]
                    
                db.session.commit()
                success += 1
                
            except Exception as e:
                db.session.rollback()
                errors.append(f"Row {index + 1} ({roll_no}): {str(e)}")
                
        return success, len(errors), errors
        
    except Exception as e:
        return 0, 0, [f"File processing error: {str(e)}"]
