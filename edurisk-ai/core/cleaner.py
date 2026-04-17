"""
cleaner.py – Data cleaning utilities.
Handles missing values, duplicates, and type coercion.
"""
import pandas as pd
import numpy as np


def clean_data(df, mapping, subjects):
    """
    Cleans the raw DataFrame:
      1. Drop fully-duplicate rows
      2. Coerce subject columns to numeric
      3. Fill missing marks with column median
      4. Fill missing attendance with column median
      5. Strip whitespace from string columns
    Returns the cleaned DataFrame.
    """
    df = df.copy()

    # --- Strip whitespace from object columns ---
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype(str).str.strip()

    # --- Remove duplicate rows ---
    df = df.drop_duplicates().reset_index(drop=True)

    # --- Coerce subject columns to numeric and fill NaN ---
    for sub in subjects:
        df[sub] = pd.to_numeric(df[sub], errors='coerce')
        median_val = df[sub].median()
        df[sub] = df[sub].fillna(median_val if not np.isnan(median_val) else 0)

    # --- Coerce and fill attendance ---
    att_col = mapping.get('attendance')
    if att_col and att_col in df.columns:
        df[att_col] = pd.to_numeric(df[att_col], errors='coerce')
        median_att = df[att_col].median()
        df[att_col] = df[att_col].fillna(median_att if not np.isnan(median_att) else 75)
        df[att_col] = df[att_col].clip(0, 100)

    return df
