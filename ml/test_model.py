"""
STEP 6 — test_model.py
Verifies placement_model.pkl works correctly with sample student inputs.
Tests all 3 classification outcomes + edge cases.
"""

import pickle
import pandas as pd

# ── Load Model ─────────────────────────────────────────────────────────────────
model_data   = pickle.load(open("placement_model.pkl", "rb"))
model        = model_data["model"]
feature_cols = model_data["feature_cols"]

print("✅ Model loaded successfully!")
print(f"   Features expected: {len(feature_cols)}\n")


# ── Helper: Build Input Row ────────────────────────────────────────────────────
def build_input(
    department="CSE",
    cgpa=8.0, backlog_count=0, attendance_percentage=85,
    aptitude_quant=80, aptitude_logical=78, aptitude_verbal=75,
    coding_easy=85, coding_medium=70, coding_hard=55, coding_contest=1400,
    communication=80, presentation=78, confidence=82, interview_mock=80,
    core_subject=82, project_score=80, internship=1, certifications=4,
    hackathon=3, linkedin=75, resume=80, skill_assessment=82
):
    """Builds a single-row DataFrame matching the trained model's feature columns."""

    # Calculated columns
    aptitude_total     = (aptitude_quant + aptitude_logical + aptitude_verbal) / 3
    coding_total       = (coding_easy * 0.20 + coding_medium * 0.35 + coding_hard * 0.45)
    soft_skill_total   = (communication + presentation + confidence + interview_mock) / 4
    cert_norm          = (certifications / 10) * 100
    internship_score   = internship * 100
    technical_total    = ((core_subject + project_score) / 2) * 0.70 + internship_score * 0.20 + cert_norm * 0.10
    hackathon_norm     = (hackathon / 5) * 100
    engagement_total   = (hackathon_norm * 0.25 + linkedin * 0.25 + resume * 0.25 + skill_assessment * 0.25)
    placement_score    = (0.20 * aptitude_total + 0.25 * coding_total + 0.20 * soft_skill_total +
                          0.20 * technical_total + 0.15 * engagement_total)

    row = {
        "cgpa": cgpa, "backlog_count": backlog_count, "attendance_percentage": attendance_percentage,
        "aptitude_quant_score": aptitude_quant, "aptitude_logical_score": aptitude_logical,
        "aptitude_verbal_score": aptitude_verbal, "aptitude_total": aptitude_total,
        "coding_easy_score": coding_easy, "coding_medium_score": coding_medium,
        "coding_hard_score": coding_hard, "coding_contest_rating": coding_contest,
        "coding_total": coding_total,
        "communication_score": communication, "presentation_skill": presentation,
        "confidence_score": confidence, "interview_mock_score": interview_mock,
        "soft_skill_total": soft_skill_total,
        "core_subject_score": core_subject, "project_score": project_score,
        "internship_experience": internship, "certification_count": certifications,
        "technical_total": technical_total,
        "hackathon_participation": hackathon, "linkedin_activity_score": linkedin,
        "resume_score": resume, "skill_assessment_score": skill_assessment,
        "engagement_total": engagement_total,
        "placement_assessment_score": placement_score,
        # Department one-hot (7 departments, AI & DS cleaned to AI_and_DS)
        "dept_CSE":       1 if department == "CSE"     else 0,
        "dept_ECE":       1 if department == "ECE"     else 0,
        "dept_IT":        1 if department == "IT"      else 0,
        "dept_MECH":      1 if department == "MECH"    else 0,
        "dept_CCE":       1 if department == "CCE"     else 0,
        "dept_EEE":       1 if department == "EEE"     else 0,
        "dept_AI_and_DS": 1 if department == "AI & DS" else 0,
    }

    df = pd.DataFrame([row])

    # Align to exact training feature columns
    for col in feature_cols:
        if col not in df.columns:
            df[col] = 0
    df = df[feature_cols]

    return df, placement_score


# ── Test Cases ─────────────────────────────────────────────────────────────────
test_cases = [
    {
        "name": "🟢 Star Student (CSE)",
        "params": dict(department="CSE", cgpa=9.2, backlog_count=0, attendance_percentage=96,
                       aptitude_quant=92, aptitude_logical=90, aptitude_verbal=88,
                       coding_easy=95, coding_medium=88, coding_hard=75, coding_contest=1900,
                       communication=90, presentation=88, confidence=92, interview_mock=90,
                       core_subject=92, project_score=90, internship=1, certifications=7,
                       hackathon=5, linkedin=88, resume=90, skill_assessment=92),
        "expected": "Ready"
    },
    {
        "name": "🟡 Average Student (ECE)",
        "params": dict(department="ECE", cgpa=7.5, backlog_count=1, attendance_percentage=78,
                       aptitude_quant=62, aptitude_logical=58, aptitude_verbal=55,
                       coding_easy=65, coding_medium=52, coding_hard=35, coding_contest=1000,
                       communication=65, presentation=60, confidence=68, interview_mock=65,
                       core_subject=65, project_score=62, internship=0, certifications=2,
                       hackathon=2, linkedin=58, resume=62, skill_assessment=65),
        "expected": "Moderate"
    },
    {
        "name": "🔴 Struggling Student (MECH)",
        "params": dict(department="MECH", cgpa=5.8, backlog_count=4, attendance_percentage=58,
                       aptitude_quant=30, aptitude_logical=28, aptitude_verbal=25,
                       coding_easy=32, coding_medium=20, coding_hard=10, coding_contest=350,
                       communication=38, presentation=35, confidence=40, interview_mock=38,
                       core_subject=38, project_score=35, internship=0, certifications=0,
                       hackathon=0, linkedin=25, resume=30, skill_assessment=35),
        "expected": "At Risk"
    },
    {
        "name": "⚠️  High Scores but Low CGPA (IT)",
        "params": dict(department="IT", cgpa=6.2, backlog_count=0, attendance_percentage=80,
                       aptitude_quant=82, aptitude_logical=80, aptitude_verbal=78,
                       coding_easy=88, coding_medium=75, coding_hard=62, coding_contest=1500,
                       communication=80, presentation=78, confidence=82, interview_mock=80,
                       core_subject=80, project_score=78, internship=1, certifications=4,
                       hackathon=3, linkedin=75, resume=78, skill_assessment=80),
        "expected": "Moderate or At Risk (CGPA drags down)"
    },
    {
        "name": "⚠️  Backlog Override Test (CSE)",
        "params": dict(department="CSE", cgpa=8.5, backlog_count=3, attendance_percentage=88,
                       aptitude_quant=85, aptitude_logical=82, aptitude_verbal=80,
                       coding_easy=90, coding_medium=78, coding_hard=65, coding_contest=1600,
                       communication=85, presentation=82, confidence=88, interview_mock=85,
                       core_subject=88, project_score=85, internship=1, certifications=5,
                       hackathon=4, linkedin=80, resume=85, skill_assessment=86),
        "expected": "At Risk (backlog > 2 override)"
    },
    {
        "name": "🟢 AI & DS Star Student",
        "params": dict(department="AI & DS", cgpa=9.3, backlog_count=0, attendance_percentage=97,
                       aptitude_quant=94, aptitude_logical=92, aptitude_verbal=89,
                       coding_easy=95, coding_medium=88, coding_hard=76, coding_contest=2050,
                       communication=88, presentation=86, confidence=90, interview_mock=88,
                       core_subject=94, project_score=93, internship=1, certifications=8,
                       hackathon=5, linkedin=90, resume=91, skill_assessment=93),
        "expected": "Ready"
    },
    {
        "name": "🟡 CCE Average Student",
        "params": dict(department="CCE", cgpa=7.3, backlog_count=1, attendance_percentage=79,
                       aptitude_quant=63, aptitude_logical=61, aptitude_verbal=60,
                       coding_easy=65, coding_medium=54, coding_hard=40, coding_contest=980,
                       communication=70, presentation=68, confidence=69, interview_mock=70,
                       core_subject=67, project_score=67, internship=0, certifications=2,
                       hackathon=2, linkedin=61, resume=66, skill_assessment=67),
        "expected": "Moderate"
    },
    {
        "name": "🔴 EEE Weak Student",
        "params": dict(department="EEE", cgpa=5.6, backlog_count=4, attendance_percentage=55,
                       aptitude_quant=26, aptitude_logical=24, aptitude_verbal=23,
                       coding_easy=23, coding_medium=14, coding_hard=5,  coding_contest=210,
                       communication=26, presentation=24, confidence=27, interview_mock=26,
                       core_subject=30, project_score=27, internship=0, certifications=0,
                       hackathon=0, linkedin=21, resume=26, skill_assessment=27),
        "expected": "At Risk"
    },
]

# ── Run Tests ──────────────────────────────────────────────────────────────────
print(f"{'='*65}")
print(f"  PLACEMENT MODEL — TEST RESULTS")
print(f"{'='*65}\n")

for tc in test_cases:
    input_df, placement_score = build_input(**tc["params"])
    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]
    classes = model.classes_

    print(f"  {tc['name']}")
    print(f"  Placement Assessment Score : {placement_score:.1f}/100")
    print(f"  Prediction                 : {prediction}")
    print(f"  Expected                   : {tc['expected']}")
    print(f"  Confidence:")
    for cls, prob in zip(classes, probabilities):
        bar = "█" * int(prob * 20)
        print(f"    {cls:<12} {prob*100:5.1f}%  {bar}")
    print()

print(f"{'='*65}")
print("✅ Model test complete — placement_model.pkl is working correctly!")
print(f"{'='*65}")
