# 🎓 EDURISK AI — Student Performance Early Warning System

> An intelligent academic analytics platform that converts messy school spreadsheets into actionable early-warning insights for teachers.

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-ff4b4b?style=flat-square&logo=streamlit)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?style=flat-square&logo=scikit-learn)

---

## ✨ Features

- **Smart Column Detection** — Auto-maps student ID, name, class, attendance, and subject columns
- **Data Quality Engine** — Validates uploads with a health score and actionable warnings
- **ML Risk Prediction** — Hybrid rule-engine + Random Forest model for accurate risk classification
- **Explainable AI** — Every risk flag includes teacher-friendly reasons
- **Interactive Dashboard** — Subject averages, risk distribution, attendance correlations, class comparisons
- **Student Profiles** — Radar charts, subject breakdowns, and per-student deep dives
- **Export Reports** — Download processed CSVs, risk lists, and summary text reports

---

## 🚀 Quick Start

### 1. Clone / Navigate to project

```bash
cd edurisk-ai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Train the ML model & generate sample data

```bash
python models/train.py
```

This creates:
- `models/risk_model.pkl` — Trained Random Forest classifier
- `data/samples/sample_data.csv` — 200-student synthetic dataset for demo

### 4. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## 📂 Project Structure

```
edurisk-ai/
├── app.py                    # Main Streamlit entry point
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── pages/                    # Streamlit multi-page structure
│   ├── 1_Home.py
│   ├── 2_Upload.py
│   ├── 3_Mapping.py
│   ├── 4_Validation.py
│   ├── 5_Dashboard.py
│   ├── 6_Student_Profile.py
│   └── 7_Reports.py
│
├── core/                     # Business logic modules
│   ├── config.py             # Constants & thresholds
│   ├── loader.py             # CSV/XLSX file reader
│   ├── mapper.py             # Column synonym detection
│   ├── validator.py          # Data quality checks
│   ├── cleaner.py            # Missing values & duplicates
│   ├── normalizer.py         # Marks → percentages
│   ├── features.py           # Feature engineering
│   ├── predictor.py          # Hybrid ML + rule engine
│   ├── explain.py            # Explainable AI reasons
│   ├── export.py             # CSV/text report generation
│   └── session.py            # Streamlit state management
│
├── visuals/
│   └── charts.py             # Matplotlib chart generators
│
├── models/
│   ├── train.py              # Model training pipeline
│   └── risk_model.pkl        # Trained model (generated)
│
└── data/
    ├── samples/
    │   └── sample_data.csv   # Demo dataset (generated)
    ├── raw/
    └── processed/
```

---

## 🎯 Demo Walkthrough (for Judges)

1. **Open the app** → Welcome page shows product overview
2. **Upload** → Use the sample CSV or your own spreadsheet
3. **Mapping** → Columns auto-detected; confirm with one click
4. **Validation** → Health score displayed; click "Run Full Analysis"
5. **Dashboard** → Explore charts, filter by risk level or class
6. **Student Profile** → Search any student; see radar chart & reasons
7. **Reports** → Download processed CSV, risk list, or summary report

---

## 🧠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Data | Pandas, NumPy |
| ML | scikit-learn (Random Forest, Logistic Regression, Decision Tree) |
| Visualization | Matplotlib |
| Export | CSV, Text |

---

## 📊 Risk Classification

### Rule Engine
- Attendance < 60% → At Risk
- Average Score < 40% → At Risk
- Weak in ≥ 2 subjects → At Risk
- Z-Score < -1 → At Risk

### ML Model
- Trained on synthetic data with engineered features
- Best model selected via cross-validation (typically Random Forest)
- Outputs probability of risk

### Hybrid Output
Rule flags and ML probability are combined to produce:
- 🟢 **Low Risk** — Student performing well
- 🟡 **Medium Risk** — Some concerns, monitor closely
- 🔴 **High Risk** — Immediate intervention needed

---

## 📝 License

Built for hackathon evaluation. © 2026 EDURISK AI.

<!-- Account Created During Testing
Field	Value
Email	priya@school.edu
Password	teacher123
Name	Ms. Priya Sharma
Valid School Secret IDs (for new signups)
Code	Description
EDURISK2026	Default demo code
SCHOOL001	Alternate code
ADMIN123	Alternate code -->