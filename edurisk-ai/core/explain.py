"""
explain.py – Explainable AI module.
Generates human-readable explanations for each student's risk assessment.
"""
import pandas as pd
from core.config import SCORE_THRESHOLD, ATTENDANCE_THRESHOLD


def explain_risk(row, mapping, subjects, class_averages=None):
    """
    For a single student row, returns a list of plain-English explanations.
    """
    reasons = []
    att_col = mapping.get('attendance')
    attendance = row.get(att_col, 75) if att_col else 75

    # --- Attendance ---
    if attendance < ATTENDANCE_THRESHOLD:
        reasons.append(f"📉 Low attendance: {attendance:.0f}% (threshold: {ATTENDANCE_THRESHOLD}%)")

    # --- Overall performance ---
    avg = row.get('avg_percentage', 100)
    if avg < SCORE_THRESHOLD:
        reasons.append(f"📉 Average score is {avg:.1f}% (below {SCORE_THRESHOLD}% threshold)")

    # --- Subject-level weakness ---
    weak_subjects = []
    for sub in subjects:
        pct_col = f"{sub}_pct"
        val = row.get(pct_col, row.get(sub, 100))
        if val < SCORE_THRESHOLD:
            weak_subjects.append(sub)
        elif class_averages and sub in class_averages:
            if val < class_averages[sub]:
                reasons.append(f"⚠️ {sub}: {val:.1f}% is below class average ({class_averages[sub]:.1f}%)")

    if weak_subjects:
        reasons.append(f"🔴 Weak in {len(weak_subjects)} subject(s): {', '.join(weak_subjects)}")

    # --- Z-score ---
    z = row.get('z_score', 0)
    if z < -1:
        reasons.append(f"📊 Z-score of {z:.2f} — performance significantly below class mean")

    if not reasons:
        reasons.append("✅ No major concerns identified")

    return reasons


def generate_explanations(df, mapping, subjects):
    """
    Adds an 'explanations' column with a list of reasons for each student.
    """
    # Compute class averages for comparison
    class_averages = {}
    for sub in subjects:
        pct_col = f"{sub}_pct"
        if pct_col in df.columns:
            class_averages[sub] = df[pct_col].mean()

    explanations = []
    for _, row in df.iterrows():
        reasons = explain_risk(row, mapping, subjects, class_averages)
        explanations.append(reasons)

    df = df.copy()
    df['explanations'] = explanations
    return df
