"""
features.py – Feature engineering pipeline.
Creates derived columns used by the ML engine and dashboard.
"""
import pandas as pd
import numpy as np
from core.config import SCORE_THRESHOLD


def engineer_features(df, mapping, subjects, max_marks=100):
    """
    Adds derived feature columns to the DataFrame:
      - avg_percentage   : mean of all subject percentages
      - z_score          : standardised distance from mean avg_percentage
      - weak_subject_count : number of subjects below SCORE_THRESHOLD %
      - risk_score       : composite 0-100 risk number
      - risk_level       : Low / Medium / High (rule-based baseline)
    """
    df = df.copy()

    # --- Percentage columns (if not already added) ---
    pct_cols = []
    for sub in subjects:
        col_name = f"{sub}_pct"
        if col_name not in df.columns:
            df[col_name] = (df[sub] / max_marks) * 100
            df[col_name] = df[col_name].clip(0, 100)
        pct_cols.append(col_name)

    # --- Average percentage ---
    if pct_cols:
        df['avg_percentage'] = df[pct_cols].mean(axis=1).round(2)
    else:
        df['avg_percentage'] = 0.0

    # --- Z-score ---
    mean_avg = df['avg_percentage'].mean()
    std_avg = df['avg_percentage'].std()
    if std_avg and std_avg > 0:
        df['z_score'] = ((df['avg_percentage'] - mean_avg) / std_avg).round(3)
    else:
        df['z_score'] = 0.0

    # --- Weak subject count ---
    df['weak_subject_count'] = 0
    for col in pct_cols:
        df['weak_subject_count'] += (df[col] < SCORE_THRESHOLD).astype(int)

    # --- Attendance (safe access) ---
    att_col = mapping.get('attendance')
    attendance = df[att_col] if (att_col and att_col in df.columns) else pd.Series(75, index=df.index)

    # --- Composite risk_score (0-100, higher = riskier) ---
    score = 0.0
    score += (100 - df['avg_percentage']) * 0.40               # 40% weight
    score += (100 - attendance) * 0.30                          # 30% weight
    score += df['weak_subject_count'] * 8                       # 8 points per weak subject
    score += (-df['z_score']).clip(lower=0) * 10                # z-score penalty
    df['risk_score'] = score.clip(0, 100).round(1)

    # --- Rule-based risk level ---
    conditions = [
        df['risk_score'] >= 60,
        df['risk_score'] >= 35,
    ]
    choices = ['High Risk', 'Medium Risk']
    df['risk_level'] = np.select(conditions, choices, default='Low Risk')

    return df
