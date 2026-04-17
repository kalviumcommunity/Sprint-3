# 🎓 EDURISK AI — Demo Script for Judges

## Pre-requisites (already done)
```bash
pip install -r requirements.txt
python models/train.py
streamlit run app.py
```

---

## Demo Flow (3-5 minutes)

### 1. Landing Page (30 sec)
- Show the **EDURISK AI** branding and feature cards
- Explain: *"This converts messy school spreadsheets into actionable early-warning insights"*
- Point out the sidebar workflow progress tracker

### 2. Upload (30 sec)
- Click **Upload** in sidebar
- Click **"Download Sample CSV"** to show template support
- Upload `data/samples/sample_data.csv` (200 students, 5 subjects)
- Show the instant preview: **200 rows, 9 columns, 1800 data points**

### 3. Mapping (30 sec)
- Click **Mapping** in sidebar
- Show auto-detection: Roll_No, Name, Class, Attendance found automatically
- Subjects (Maths, Science, English, Hindi, Social_Studies) auto-detected
- Click **"Confirm Mapping"** — balloons!

### 4. Validation (45 sec)
- Click **Validation** in sidebar
- Show **85% Health Score** — "Excellent" with green border
- Point out: "17 missing values detected, 0 duplicates, 5 subjects"
- Click **"Run Full Analysis Pipeline"**
- Watch the animated progress bar through 5 stages
- Point out the Quick Results: High Risk / Medium Risk / Low Risk split

### 5. Dashboard (60 sec) ← **KEY DEMO MOMENT**
- Click **Dashboard** in sidebar
- Show top metrics: Total Students, High Risk count, Avg Score, Weakest Subject
- Click through chart tabs:
  - **Subject Averages** — bar chart with colour-coded scores
  - **Risk Distribution** — donut chart showing risk breakdown
  - **Attendance vs Marks** — scatter plot coloured by risk level
  - **Class Comparison** — grouped bars across 8A, 8B, 9A, 9B, 10A, 10B
- Scroll to **Student Risk Overview** table
- Filter by "High Risk" only to show intervention list
- Show the progress bar columns for visual impact

### 6. Student Profile (45 sec)
- Click **Student Profile** in sidebar
- Search for a high-risk student
- Show the **student card** with red "High Risk" badge
- Show metrics: Average Score, Attendance, Z-Score, Weak Subjects
- Point out the **Performance Radar** (student vs class average)
- Point out **Subject Breakdown** with +/- delta indicators
- Scroll to **Risk Explanation** — show the emoji-tagged, teacher-friendly reasons

### 7. Reports (30 sec)
- Click **Reports** in sidebar
- Show three download cards: Processed Data, Risk List, Summary Report
- Click **"Preview Summary Report"** expander
- Highlight the auto-generated text report with recommendations

---

## Key Talking Points

1. **No code needed** — teachers just upload a spreadsheet
2. **Smart detection** — auto-maps columns using synonym matching
3. **Hybrid AI** — rule engine + Random Forest for accurate, explainable predictions
4. **Explainable** — every risk flag has teacher-friendly reasons, no black boxes
5. **Actionable** — downloadable reports for intervention planning
6. **Production-ready** — modular architecture, session state management, error handling
