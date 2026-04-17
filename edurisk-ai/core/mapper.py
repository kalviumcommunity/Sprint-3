import pandas as pd

def detect_columns(columns):
    """
    Auto-detects typical school columns using synonyms.
    Returns metadata mapping and a list of inferred subject columns.
    """
    mapping = {}
    synonyms = {
        'student_id': ['id', 'roll', 'roll_no', 'student_id', 'rollnumber', 's_id'],
        'name': ['name', 'student_name', 'full_name', 'student'],
        'class': ['class', 'grade', 'std', 'standard', 'batch'],
        'attendance': ['attendance', 'att', 'present', 'presence', 'att%'],
    }
    
    lower_cols = {col: str(col).lower().strip() for col in columns}
    
    for target, syns in synonyms.items():
        mapping[target] = None
        for original, lower in lower_cols.items():
            if lower in syns or any(s in lower for s in syns):
                mapping[target] = original
                break

    mapped_originals = [v for v in mapping.values() if v is not None]
    subjects = [c for c in columns if c not in mapped_originals]
    
    return mapping, subjects
