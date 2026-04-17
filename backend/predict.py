"""
predict.py
Loads placement_model.pkl and handles:
1. Priority Override Logic (before model)
2. Feature building from raw scores
3. Returns classification + assessment score
"""

import pickle
import os
import pandas as pd

# ── Load Model Once at startup ─────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../ml/placement_model.pkl")
model_data   = pickle.load(open(MODEL_PATH, "rb"))
model        = model_data["model"]
feature_cols = model_data["feature_cols"]

# ── Departments list ───────────────────────────────────────────────────────────
DEPARTMENTS = ["CSE", "ECE", "IT", "MECH", "CCE", "EEE", "AI & DS"]


# ══════════════════════════════════════════════════════════════════════════════
# MAIN PREDICTION FUNCTION
# ══════════════════════════════════════════════════════════════════════════════
def predict_placement(data):
    """
    Input : dict with all student scores
    Output: dict with classification, score, confidence, override_reason
    """

    # ── Extract raw values ─────────────────────────────────────────────────────
    department   = data.get("department", "CSE")
    cgpa         = float(data.get("cgpa", 0))
    backlog      = int(data.get("backlog_count", 0))
    attendance   = float(data.get("attendance_percentage", 0))

    apt_quant    = float(data.get("aptitude_quant_score", 0))
    apt_logical  = float(data.get("aptitude_logical_score", 0))
    apt_verbal   = float(data.get("aptitude_verbal_score", 0))

    code_easy    = float(data.get("coding_easy_score", 0))
    code_medium  = float(data.get("coding_medium_score", 0))
    code_hard    = float(data.get("coding_hard_score", 0))
    code_contest = float(data.get("coding_contest_rating", 0))

    communication= float(data.get("communication_score", 0))
    presentation = float(data.get("presentation_skill", 0))
    confidence   = float(data.get("confidence_score", 0))
    mock_interview=float(data.get("interview_mock_score", 0))

    core_subject = float(data.get("core_subject_score", 0))
    project      = float(data.get("project_score", 0))
    internship   = int(data.get("internship_experience", 0))
    certifications=int(data.get("certification_count", 0))

    hackathon    = int(data.get("hackathon_participation", 0))
    linkedin     = float(data.get("linkedin_activity_score", 0))
    resume       = float(data.get("resume_score", 0))
    skill_assess = float(data.get("skill_assessment_score", 0))

    # ── Calculate derived totals ───────────────────────────────────────────────
    aptitude_total   = (apt_quant + apt_logical + apt_verbal) / 3

    coding_total     = (code_easy * 0.20 +
                        code_medium * 0.35 +
                        code_hard * 0.45)

    soft_skill_total = (communication + presentation +
                        confidence + mock_interview) / 4

    cert_norm        = (certifications / 10) * 100
    internship_score = internship * 100
    technical_total  = (((core_subject + project) / 2) * 0.70 +
                        internship_score * 0.20 +
                        cert_norm * 0.10)

    hackathon_norm   = (hackathon / 5) * 100
    engagement_total = (hackathon_norm * 0.25 +
                        linkedin * 0.25 +
                        resume * 0.25 +
                        skill_assess * 0.25)

    placement_score  = round(
        (0.20 * aptitude_total)   +
        (0.25 * coding_total)     +
        (0.20 * soft_skill_total) +
        (0.20 * technical_total)  +
        (0.15 * engagement_total), 2
    )

    # ══════════════════════════════════════════════════════════════════════════
    # PRIORITY OVERRIDE LOGIC (applied BEFORE model)
    # ══════════════════════════════════════════════════════════════════════════
    override_reason = None

    # Priority 1 — Backlog Hard Override
    if backlog > 2:
        return {
            "placement_status":      "At Risk",
            "placement_score":       placement_score,
            "confidence":            {"At Risk": 100.0, "Moderate": 0.0, "Ready": 0.0},
            "override_applied":      True,
            "override_reason":       f"Backlog count ({backlog}) exceeds limit of 2",
            "aptitude_total":        round(aptitude_total, 2),
            "coding_total":          round(coding_total, 2),
            "soft_skill_total":      round(soft_skill_total, 2),
            "technical_total":       round(technical_total, 2),
            "engagement_total":      round(engagement_total, 2),
        }

    # ── Build feature row for ML model ────────────────────────────────────────
    row = {
        "cgpa":                     cgpa,
        "backlog_count":            backlog,
        "attendance_percentage":    attendance,
        "aptitude_quant_score":     apt_quant,
        "aptitude_logical_score":   apt_logical,
        "aptitude_verbal_score":    apt_verbal,
        "aptitude_total":           aptitude_total,
        "coding_easy_score":        code_easy,
        "coding_medium_score":      code_medium,
        "coding_hard_score":        code_hard,
        "coding_contest_rating":    code_contest,
        "coding_total":             coding_total,
        "communication_score":      communication,
        "presentation_skill":       presentation,
        "confidence_score":         confidence,
        "interview_mock_score":     mock_interview,
        "soft_skill_total":         soft_skill_total,
        "core_subject_score":       core_subject,
        "project_score":            project,
        "internship_experience":    internship,
        "certification_count":      certifications,
        "technical_total":          technical_total,
        "hackathon_participation":  hackathon,
        "linkedin_activity_score":  linkedin,
        "resume_score":             resume,
        "skill_assessment_score":   skill_assess,
        "engagement_total":         engagement_total,
        "placement_assessment_score": placement_score,
        # Department one-hot
        "dept_CSE":       1 if department == "CSE"     else 0,
        "dept_ECE":       1 if department == "ECE"     else 0,
        "dept_IT":        1 if department == "IT"      else 0,
        "dept_MECH":      1 if department == "MECH"    else 0,
        "dept_CCE":       1 if department == "CCE"     else 0,
        "dept_EEE":       1 if department == "EEE"     else 0,
        "dept_AI_and_DS": 1 if department == "AI & DS" else 0,
    }

    # Align to training feature columns
    df_input = pd.DataFrame([row])
    for col in feature_cols:
        if col not in df_input.columns:
            df_input[col] = 0
    df_input = df_input[feature_cols]

    # ── ML Model Prediction ────────────────────────────────────────────────────
    ml_prediction  = model.predict(df_input)[0]
    ml_proba       = model.predict_proba(df_input)[0]
    classes        = model.classes_
    confidence_map = {cls: round(prob * 100, 1)
                      for cls, prob in zip(classes, ml_proba)}

    # ── Priority 2 — Academic Constraint (can only downgrade) ─────────────────
    if cgpa >= 8.0:
        academic_label = "Ready"
    elif cgpa >= 7.1:
        academic_label = "Moderate"
    else:
        academic_label = "At Risk"

    priority = {"Ready": 2, "Moderate": 1, "At Risk": 0}
    final_label = min(ml_prediction, academic_label,
                      key=lambda x: priority[x])

    if final_label != ml_prediction:
        override_reason = (f"CGPA ({cgpa}) academic constraint "
                           f"downgraded from {ml_prediction} to {final_label}")

    return {
        "placement_status":      final_label,
        "placement_score":       placement_score,
        "confidence":            confidence_map,
        "override_applied":      override_reason is not None,
        "override_reason":       override_reason,
        "aptitude_total":        round(aptitude_total, 2),
        "coding_total":          round(coding_total, 2),
        "soft_skill_total":      round(soft_skill_total, 2),
        "technical_total":       round(technical_total, 2),
        "engagement_total":      round(engagement_total, 2),
    }
