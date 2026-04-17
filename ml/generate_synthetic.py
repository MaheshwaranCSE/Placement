"""
STEP 2 — generate_synthetic.py
Uses SDV GaussianCopulaSynthesizer to generate 500 realistic student rows.
Learns correlations from seed_data.csv, then post-processes with all business logic.
"""

import pandas as pd
import numpy as np
import random
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata

random.seed(42)
np.random.seed(42)

# ── Load Seed Data ─────────────────────────────────────────────────────────────
df_seed = pd.read_csv("seed_data.csv")

# Drop student_id before SDV training (non-informative identity column)
df_model = df_seed.drop(columns=["student_id"])

print(f"✅ Seed data loaded: {df_model.shape}")
print(f"   Columns for SDV: {list(df_model.columns)}\n")

# ── Define SDV Metadata ────────────────────────────────────────────────────────
metadata = SingleTableMetadata()
metadata.detect_from_dataframe(df_model)

# Override column types explicitly
metadata.update_column("department",              sdtype="categorical")
# Departments: CSE, ECE, IT, MECH, CCE, EEE, AI & DS
metadata.update_column("cgpa",                    sdtype="numerical")
metadata.update_column("backlog_count",            sdtype="numerical")
metadata.update_column("attendance_percentage",    sdtype="numerical")

metadata.update_column("aptitude_quant_score",     sdtype="numerical")
metadata.update_column("aptitude_logical_score",   sdtype="numerical")
metadata.update_column("aptitude_verbal_score",    sdtype="numerical")

metadata.update_column("coding_easy_score",        sdtype="numerical")
metadata.update_column("coding_medium_score",      sdtype="numerical")
metadata.update_column("coding_hard_score",        sdtype="numerical")
metadata.update_column("coding_contest_rating",    sdtype="numerical")

metadata.update_column("communication_score",      sdtype="numerical")
metadata.update_column("presentation_skill",       sdtype="numerical")
metadata.update_column("confidence_score",         sdtype="numerical")
metadata.update_column("interview_mock_score",     sdtype="numerical")

metadata.update_column("core_subject_score",       sdtype="numerical")
metadata.update_column("project_score",            sdtype="numerical")
metadata.update_column("internship_experience",    sdtype="categorical")  # binary — categorical!
metadata.update_column("certification_count",      sdtype="numerical")

metadata.update_column("hackathon_participation",  sdtype="numerical")
metadata.update_column("linkedin_activity_score",  sdtype="numerical")
metadata.update_column("resume_score",             sdtype="numerical")
metadata.update_column("skill_assessment_score",   sdtype="numerical")

print("✅ Metadata defined!\n")

# ── Train SDV Synthesizer ──────────────────────────────────────────────────────
print("🔄 Training GaussianCopulaSynthesizer on seed data...")
synthesizer = GaussianCopulaSynthesizer(
    metadata,
    enforce_min_max_values=True,   # keeps scores in learned ranges
    enforce_rounding=True           # rounds integers properly
)
synthesizer.fit(df_model)
print("✅ SDV Model trained!\n")

# ── Generate 500 Rows ──────────────────────────────────────────────────────────
print("🔄 Generating 500 synthetic student rows...")
synthetic_df = synthesizer.sample(num_rows=500)

# ── Post-Processing: Clip & Round All Scores ───────────────────────────────────
score_cols_0_100 = [
    "aptitude_quant_score", "aptitude_logical_score", "aptitude_verbal_score",
    "coding_easy_score", "coding_medium_score", "coding_hard_score",
    "communication_score", "presentation_skill", "confidence_score",
    "interview_mock_score", "core_subject_score", "project_score",
    "linkedin_activity_score", "resume_score", "skill_assessment_score",
    "attendance_percentage"
]

for col in score_cols_0_100:
    synthetic_df[col] = synthetic_df[col].clip(0, 100).round().astype(int)

synthetic_df["cgpa"]                  = synthetic_df["cgpa"].clip(0.0, 10.0).round(1)
synthetic_df["backlog_count"]          = synthetic_df["backlog_count"].clip(0, 10).round().astype(int)
synthetic_df["coding_contest_rating"]  = synthetic_df["coding_contest_rating"].clip(0, 2500).round().astype(int)
synthetic_df["certification_count"]    = synthetic_df["certification_count"].clip(0, 10).round().astype(int)
synthetic_df["hackathon_participation"]= synthetic_df["hackathon_participation"].clip(0, 5).round().astype(int)

# Fix internship_experience — ensure it's exactly 0 or 1
synthetic_df["internship_experience"] = synthetic_df["internship_experience"].apply(
    lambda x: 1 if str(x) in ["1", "1.0", "True"] else 0
).astype(int)

# ── Calculate Derived Columns ──────────────────────────────────────────────────

# 1. aptitude_total = average of 3 sections (0–100)
synthetic_df["aptitude_total"] = (
    synthetic_df["aptitude_quant_score"] +
    synthetic_df["aptitude_logical_score"] +
    synthetic_df["aptitude_verbal_score"]
) / 3

# 2. coding_total = weighted (easy 20%, medium 35%, hard 45%) normalized to 0–100
#    coding_contest_rating normalized to 0–100 first, blended in
synthetic_df["coding_contest_normalized"] = (synthetic_df["coding_contest_rating"] / 2500) * 100

synthetic_df["coding_total"] = (
    (synthetic_df["coding_easy_score"]       * 0.20) +
    (synthetic_df["coding_medium_score"]     * 0.35) +
    (synthetic_df["coding_hard_score"]       * 0.45)
).clip(0, 100)

# 3. soft_skill_total = average of 4 columns (0–100)
synthetic_df["soft_skill_total"] = (
    synthetic_df["communication_score"] +
    synthetic_df["presentation_skill"] +
    synthetic_df["confidence_score"] +
    synthetic_df["interview_mock_score"]
) / 4

# 4. technical_total = weighted (core+project avg 70%, internship 20%, certifications 10%)
cert_normalized = (synthetic_df["certification_count"] / 10) * 100
internship_score = synthetic_df["internship_experience"] * 100  # 0 or 100

synthetic_df["technical_total"] = (
    ((synthetic_df["core_subject_score"] + synthetic_df["project_score"]) / 2) * 0.70 +
    internship_score * 0.20 +
    cert_normalized * 0.10
).clip(0, 100)

# 5. engagement_total = hackathon normalized + others averaged (0–100)
hackathon_normalized = (synthetic_df["hackathon_participation"] / 5) * 100

synthetic_df["engagement_total"] = (
    hackathon_normalized * 0.25 +
    synthetic_df["linkedin_activity_score"] * 0.25 +
    synthetic_df["resume_score"] * 0.25 +
    synthetic_df["skill_assessment_score"] * 0.25
).clip(0, 100)

# 6. placement_assessment_score = Final weighted formula
synthetic_df["placement_assessment_score"] = (
    (0.20 * synthetic_df["aptitude_total"]) +
    (0.25 * synthetic_df["coding_total"]) +
    (0.20 * synthetic_df["soft_skill_total"]) +
    (0.20 * synthetic_df["technical_total"]) +
    (0.15 * synthetic_df["engagement_total"])
).clip(0, 100).round(2)

# ── Assign placement_status: Priority Override System ─────────────────────────
def assign_placement_status(row):
    # Step 1: Backlog Hard Override (highest priority)
    if row["backlog_count"] > 2:
        return "At Risk"

    # Step 2: Score-based base label
    score = row["placement_assessment_score"]
    if score >= 70:
        base_label = "Ready"
    elif score >= 45:
        base_label = "Moderate"
    else:
        base_label = "At Risk"

    # Step 3: Academic Constraint label
    cgpa = row["cgpa"]
    if cgpa >= 8.0:
        academic_label = "Ready"
    elif cgpa >= 7.1:
        academic_label = "Moderate"
    else:
        academic_label = "At Risk"

    # Step 4: Take the WORSE of the two (academic can only downgrade, not upgrade)
    priority = {"Ready": 2, "Moderate": 1, "At Risk": 0}
    final = min(base_label, academic_label, key=lambda x: priority[x])

    return final

synthetic_df["placement_status"] = synthetic_df.apply(assign_placement_status, axis=1)

# ── Add student_id ─────────────────────────────────────────────────────────────
synthetic_df.insert(0, "student_id", [f"STU{i:04d}" for i in range(1, 501)])

# ── Drop helper column (not needed in final dataset) ──────────────────────────
synthetic_df.drop(columns=["coding_contest_normalized"], inplace=True)

# ── Save Raw Synthetic (before any further processing) ─────────────────────────
synthetic_df.to_csv("student_data_raw.csv", index=False)

# ── Print Summary ──────────────────────────────────────────────────────────────
print(f"\n✅ Synthetic dataset generated: {len(synthetic_df)} rows")
print(f"   Total columns: {len(synthetic_df.columns)}")
print(f"\n📊 Placement Status Distribution:")
print(synthetic_df["placement_status"].value_counts())
print(f"\n📈 Score Statistics:")
print(synthetic_df[[
    "aptitude_total", "coding_total", "soft_skill_total",
    "technical_total", "engagement_total", "placement_assessment_score"
]].describe().round(2))
print(f"\n🏫 Department Distribution:")
print(synthetic_df["department"].value_counts())
print(f"\n🎓 CGPA Stats:")
print(synthetic_df["cgpa"].describe().round(2))
print("\n✅ student_data_raw.csv saved!")
