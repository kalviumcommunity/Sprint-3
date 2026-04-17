"""
normalizer.py – Normalizes marks to percentages.
"""
import pandas as pd
import numpy as np


def normalize_marks(df, subjects, max_marks=100):
    """
    Converts raw marks to percentages.
    Formula: percentage = (marks / max_marks) * 100
    Clips results to [0, 100].
    """
    df = df.copy()
    for sub in subjects:
        col_name = f"{sub}_pct"
        df[col_name] = (df[sub] / max_marks) * 100
        df[col_name] = df[col_name].clip(0, 100)
    return df
