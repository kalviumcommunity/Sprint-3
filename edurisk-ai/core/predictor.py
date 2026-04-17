"""
predictor.py – Hybrid ML + rule-based risk prediction engine.
Combines scikit-learn model probabilities with hand-crafted rules.
"""
import os
import pickle
import numpy as np
import pandas as pd
from core.config import (
    ATTENDANCE_THRESHOLD,
    SCORE_THRESHOLD,
    WEAK_SUBJECT_THRESHOLD,
    Z_SCORE_THRESHOLD,
)

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'risk_model.pkl')


def _load_model():
    """Load the pre-trained model from disk."""
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)
    return None


def _rule_engine(row, att_col):
    """
    Deterministic rules that flag a student as at-risk.
    Returns (is_risky: bool, reasons: list[str]).
    """
    reasons = []
    attendance = row.get(att_col, 75) if att_col else 75

    if attendance < ATTENDANCE_THRESHOLD:
        reasons.append(f"Low attendance ({attendance:.0f}%)")
    if row.get('avg_percentage', 100) < SCORE_THRESHOLD:
        reasons.append(f"Average score below {SCORE_THRESHOLD}%")
    if row.get('weak_subject_count', 0) >= WEAK_SUBJECT_THRESHOLD:
        reasons.append(f"Weak in {int(row['weak_subject_count'])} subjects")
    if row.get('z_score', 0) < Z_SCORE_THRESHOLD:
        reasons.append("Performance significantly below class average")

    return len(reasons) > 0, reasons


def predict(df, mapping):
    """
    Hybrid prediction:
      1. Run rule engine on every row.
      2. Run ML model (if available) to get risk probability.
      3. Blend: if either flags risk → mark as risk; use ML probability
         to fine-tune the level (High / Medium / Low).
    Adds columns: ml_prob, final_risk, risk_reasons
    """
    df = df.copy()
    att_col = mapping.get('attendance')

    # --- Prepare ML features ---
    feature_cols = ['avg_percentage', 'z_score', 'weak_subject_count']
    if att_col and att_col in df.columns:
        feature_cols.append(att_col)

    model = _load_model()

    ml_probs = np.full(len(df), 0.5)
    if model is not None:
        try:
            X = df[feature_cols].fillna(0).values
            # Ensure we have the right number of features the model expects
            if hasattr(model, 'n_features_in_') and X.shape[1] != model.n_features_in_:
                # Pad or trim features to match
                expected = model.n_features_in_
                if X.shape[1] < expected:
                    X = np.hstack([X, np.zeros((X.shape[0], expected - X.shape[1]))])
                else:
                    X = X[:, :expected]
            ml_probs = model.predict_proba(X)[:, 1]
        except Exception:
            ml_probs = np.full(len(df), 0.5)

    df['ml_prob'] = ml_probs

    # --- Combine rules + ML ---
    final_risks = []
    all_reasons = []

    for idx, row in df.iterrows():
        rule_risk, reasons = _rule_engine(row, att_col)
        prob = row['ml_prob']

        if rule_risk:
            # Rules fired — use rule count + ML probability to set level
            if len(reasons) >= 3 or prob >= 0.75:
                level = 'High Risk'
            elif len(reasons) >= 2 or prob >= 0.55:
                level = 'High Risk'
            else:
                level = 'Medium Risk'
        elif prob >= 0.7:
            # No rules fired but ML is very confident — flag as Medium only
            level = 'Medium Risk'
            reasons.append("ML model flags elevated risk")
        elif prob >= 0.5:
            level = 'Medium Risk'
            reasons.append("ML model flags moderate risk")
        else:
            level = 'Low Risk'

        final_risks.append(level)
        all_reasons.append('; '.join(reasons) if reasons else 'No concerns')

    df['final_risk'] = final_risks
    df['risk_reasons'] = all_reasons

    return df

