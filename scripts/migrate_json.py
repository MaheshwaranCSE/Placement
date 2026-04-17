import os
import json
from backend.app import create_app
from backend.models import Student, PlacementRecord, PredictionLog
from backend.extensions import db

app = create_app(os.getenv('FLASK_ENV', 'development'))

def migrate():
    json_path = os.path.join(os.path.dirname(__file__), '../backend/students.json')
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return
        
    with open(json_path, 'r') as f:
        data = json.load(f)
        
    inserted = 0
    skipped = 0
    errors = 0
    
    with app.app_context():
        for item in data:
            try:
                roll_number = item.get('student_id')  # old JSON used student_id for roll number
                if not roll_number:
                    continue
                    
                if Student.query.filter_by(roll_number=roll_number).first():
                    skipped += 1
                    continue
                    
                s = Student(
                    roll_number=roll_number,
                    name=item.get('name', 'Unknown'),
                    department=item.get('department'),
                    cgpa=item.get('cgpa'),
                    backlogs=item.get('backlog_count', 0),
                    internships=item.get('internship_experience', 0),
                    projects=0, # Assuming no project count in old json
                    communication_score=item.get('communication_score'),
                    aptitude_score=int(item.get('aptitude_total', 0) / 10), # roughly scaling old 0-100 to 0-10
                )
                db.session.add(s)
                db.session.flush() # get s.id
                
                # Add placement if any
                status = item.get('placement_status')
                if status:
                    pr = PlacementRecord(
                        student_id=s.id,
                        status=status.lower().replace(' ', '_'),
                    )
                    db.session.add(pr)
                    
                # Add prediction log if any
                score = item.get('placement_assessment_score')
                if score is not None:
                    pl = PredictionLog(
                        student_id=s.id,
                        predicted_probability=float(score) / 100.0,
                        predicted_class=(score > 50),
                        model_version='legacy-json-import'
                    )
                    db.session.add(pl)
                    
                db.session.commit()
                inserted += 1
                
            except Exception as e:
                db.session.rollback()
                print(f"Error importing {item.get('student_id')}: {e}")
                errors += 1
                
    print(f"Migration Complete: {inserted} inserted, {skipped} skipped, {errors} errors.")

if __name__ == '__main__':
    migrate()
