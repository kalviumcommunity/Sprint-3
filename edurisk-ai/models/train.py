"""
train.py – Generates synthetic training data, trains risk-classification
models (Logistic Regression, Decision Tree, Random Forest), compares them,
saves the best one as risk_model.pkl, and writes a sample CSV to data/samples/.
"""
import os
import pickle
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report

np.random.seed(42)

# ── paths ──
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_OUT = os.path.join(BASE_DIR, 'models', 'risk_model.pkl')
SAMPLE_OUT = os.path.join(BASE_DIR, 'data', 'samples', 'sample_data.csv')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')

SUBJECTS = ['Maths', 'Science', 'English', 'Hindi', 'Social_Studies']
CLASSES = ['8A', '8B', '9A', '9B', '10A', '10B']
FIRST_NAMES = [
    'Aarav', 'Vivaan', 'Aditya', 'Vihaan', 'Arjun', 'Sai', 'Reyansh',
    'Ayaan', 'Krishna', 'Ishaan', 'Ananya', 'Diya', 'Myra', 'Sara',
    'Aanya', 'Aadhya', 'Saanvi', 'Ira', 'Kiara', 'Priya', 'Riya',
    'Neha', 'Kavya', 'Tanvi', 'Meera', 'Rohan', 'Karan', 'Rahul',
    'Amit', 'Sneha', 'Pooja', 'Raj', 'Vikram', 'Siddharth', 'Nisha',
    'Lakshmi', 'Gaurav', 'Manish', 'Deepa', 'Harini', 'Suresh',
    'Mahesh', 'Divya', 'Bhavya', 'Chetan', 'Arun', 'Varun', 'Swathi',
    'Keerthi', 'Naveen',
]
LAST_NAMES = [
    'Sharma', 'Verma', 'Patel', 'Gupta', 'Singh', 'Kumar', 'Reddy',
    'Nair', 'Joshi', 'Mehta', 'Rao', 'Iyer', 'Das', 'Pillai', 'Menon',
    'Chopra', 'Bhat', 'Desai', 'Kapoor', 'Malhotra',
]

N_STUDENTS = 200


def _generate_synthetic_data():
    """Creates a realistic synthetic school dataset."""
    records = []
    for i in range(1, N_STUDENTS + 1):
        name = f"{np.random.choice(FIRST_NAMES)} {np.random.choice(LAST_NAMES)}"
        cls = np.random.choice(CLASSES)

        # Create correlated student profiles
        ability = np.random.beta(2, 2) * 100  # base ability 0-100
        attendance = np.clip(ability + np.random.normal(0, 15), 20, 100).round(1)

        marks = {}
        for sub in SUBJECTS:
            noise = np.random.normal(0, 12)
            m = np.clip(ability + noise, 0, 100).round(0)
            marks[sub] = int(m)

        records.append({
            'Roll_No': f"STU{i:04d}",
            'Name': name,
            'Class': cls,
            'Attendance': attendance,
            **marks,
        })

    df = pd.DataFrame(records)

    # Introduce some realistic messiness
    # A few missing values
    for col in SUBJECTS:
        idx = np.random.choice(df.index, size=3, replace=False)
        df.loc[idx, col] = np.nan

    idx_att = np.random.choice(df.index, size=2, replace=False)
    df.loc[idx_att, 'Attendance'] = np.nan

    return df


def _prepare_features(df):
    """Engineer features for model training."""
    df = df.copy()
    for sub in SUBJECTS:
        df[sub] = pd.to_numeric(df[sub], errors='coerce')
        df[sub] = df[sub].fillna(df[sub].median())

    df['Attendance'] = pd.to_numeric(df['Attendance'], errors='coerce')
    df['Attendance'] = df['Attendance'].fillna(df['Attendance'].median())

    pct_cols = []
    for sub in SUBJECTS:
        col = f"{sub}_pct"
        df[col] = (df[sub] / 100) * 100  # already out of 100
        pct_cols.append(col)

    df['avg_percentage'] = df[pct_cols].mean(axis=1)

    mean_avg = df['avg_percentage'].mean()
    std_avg = df['avg_percentage'].std()
    df['z_score'] = (df['avg_percentage'] - mean_avg) / std_avg if std_avg > 0 else 0

    df['weak_subject_count'] = 0
    for col in pct_cols:
        df['weak_subject_count'] += (df[col] < 40).astype(int)

    # Create target label
    df['risk'] = 0
    df.loc[df['avg_percentage'] < 40, 'risk'] = 1
    df.loc[df['Attendance'] < 60, 'risk'] = 1
    df.loc[df['weak_subject_count'] >= 2, 'risk'] = 1
    df.loc[df['z_score'] < -1, 'risk'] = 1

    return df


def train_models():
    """Train and compare models, save the best one."""
    print("=" * 50)
    print("  EDURISK AI -- Model Training Pipeline")
    print("=" * 50)

    # Generate data
    print("\n[1/4] Generating synthetic data...")
    raw_df = _generate_synthetic_data()

    # Save sample
    os.makedirs(os.path.dirname(SAMPLE_OUT), exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(RAW_DIR, exist_ok=True)
    raw_df.to_csv(SAMPLE_OUT, index=False)
    print(f"  [OK] Sample data saved -> {SAMPLE_OUT}")

    # Feature engineering
    print("\n[2/4] Engineering features...")
    df = _prepare_features(raw_df)
    feature_cols = ['avg_percentage', 'Attendance', 'z_score', 'weak_subject_count']
    X = df[feature_cols].values
    y = df['risk'].values
    print(f"  [OK] Features: {feature_cols}")
    print(f"  [OK] Samples: {len(X)} | Positive (at-risk): {y.sum()} | Negative: {(1-y).sum()}")

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Compare models
    print("\n[3/4] Training and comparing models...")
    models = {
        'Logistic Regression': LogisticRegression(max_iter=500, random_state=42),
        'Decision Tree': DecisionTreeClassifier(max_depth=5, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42),
    }

    best_name, best_model, best_score = None, None, 0
    for name, model in models.items():
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
        model.fit(X_train, y_train)
        test_acc = accuracy_score(y_test, model.predict(X_test))
        print(f"  {name:25s}  CV={cv_scores.mean():.3f} +/- {cv_scores.std():.3f}  Test={test_acc:.3f}")
        if test_acc > best_score:
            best_name, best_model, best_score = name, model, test_acc

    print(f"\n  [BEST] {best_name} (accuracy={best_score:.3f})")

    # Save model
    print("\n[4/4] Saving model...")
    os.makedirs(os.path.dirname(MODEL_OUT), exist_ok=True)
    with open(MODEL_OUT, 'wb') as f:
        pickle.dump(best_model, f)
    print(f"  [OK] Model saved -> {MODEL_OUT}")

    print("\n[DONE] Training pipeline complete!\n")


if __name__ == '__main__':
    train_models()
