import pandas as pd
import numpy as np

def validate_data(df, mapping, subjects, max_marks=100):
    issues = []
    
    missing = df.isnull().sum().sum()
    if missing > 0:
        issues.append(f"Warning: {missing} missing values detected.")
        
    dupes = df.duplicated().sum()
    if dupes > 0:
        issues.append(f"Warning: {dupes} duplicate rows found.")
        
    for sub in subjects:
        if pd.api.types.is_numeric_dtype(df[sub]):
            if df[sub].max() > max_marks:
                issues.append(f"Error: {sub} has marks > {max_marks}.")
            if df[sub].min() < 0:
                issues.append(f"Error: {sub} has negative marks.")
        else:
            issues.append(f"Warning: {sub} contains non-numeric text.")
            
    att_col = mapping.get('attendance')
    if att_col and att_col in df.columns:
        if pd.api.types.is_numeric_dtype(df[att_col]):
            if df[att_col].max() > 100:
                issues.append(f"Warning: Attendance > 100% detected.")
                
    health_score = max(0, 100 - (len(issues) * 15))
    return issues, health_score
