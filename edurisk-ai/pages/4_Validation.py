"""
4_Validation.py – Data validation and analysis pipeline.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.style import inject_custom_css, sidebar_branding, require_auth, icon
from core.session import put, get, is_ready
from core.validator import validate_data
from core.cleaner import clean_data
from core.normalizer import normalize_marks
from core.features import engineer_features
from core.predictor import predict
from core.explain import generate_explanations

inject_custom_css()
sidebar_branding()
require_auth()

st.markdown(f'<h1>{icon("check_circle")} Data Validation & Processing</h1>', unsafe_allow_html=True)
st.caption("Review data quality, then clean and analyse your dataset.")
st.markdown("---")

if not is_ready('mapping_complete'):
    st.warning("Please complete column mapping first on the **Mapping** page.")
    st.stop()

df = get('raw_df')
mapping = get('mapping')
subjects = get('subjects')

if df is None or mapping is None or subjects is None:
    st.error("Session data missing. Please restart from **Upload**.")
    st.stop()

# ── Validation ──
st.markdown(f'### {icon("fact_check")} Data Quality Report', unsafe_allow_html=True)

issues, health = validate_data(df, mapping, subjects)
put('validation_issues', issues)
put('health_score', health)

if health >= 80:
    colour, label = "#059669", "Excellent"
elif health >= 50:
    colour, label = "#d97706", "Fair"
else:
    colour, label = "#dc2626", "Poor"

col1, col2 = st.columns([1, 2])
with col1:
    st.markdown(f"""
    <div class="card" style="text-align:center; border: 2px solid {colour};">
        <p style="color:#64748b; font-size:0.75rem; text-transform:uppercase;
                  letter-spacing:0.08em; margin-bottom:6px;">Upload Health Score</p>
        <p style="font-size:2.8rem; font-weight:800; color:{colour}; margin:0;">{health}%</p>
        <p style="color:{colour}; font-weight:600; margin-top:4px;">{label}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if issues:
        for issue in issues:
            if issue.startswith("Error"):
                st.error(issue)
            else:
                st.warning(issue)
    else:
        st.success("No data quality issues detected.")

st.progress(health / 100)

# ── Stats ──
st.markdown(f'### {icon("bar_chart")} Dataset Stats', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Rows", f"{len(df):,}")
c2.metric("Missing Values", f"{df.isnull().sum().sum()}")
c3.metric("Duplicate Rows", f"{df.duplicated().sum()}")
c4.metric("Subjects", f"{len(subjects)}")

# ── Processing ──
st.markdown("---")
st.markdown(f'### {icon("settings")} Process & Analyse', unsafe_allow_html=True)
st.markdown("Click below to clean, normalise, and run ML predictions on your data.")

if st.button("Run Full Analysis Pipeline", type="primary", width="stretch"):
    progress = st.progress(0, text="Starting pipeline...")

    progress.progress(15, text="Cleaning data...")
    cleaned = clean_data(df, mapping, subjects)

    progress.progress(35, text="Normalising marks...")
    normalised = normalize_marks(cleaned, subjects)

    progress.progress(55, text="Engineering features...")
    featured = engineer_features(normalised, mapping, subjects)

    progress.progress(75, text="Running ML + rule engine...")
    predicted = predict(featured, mapping)

    progress.progress(90, text="Generating explanations...")
    final = generate_explanations(predicted, mapping, subjects)

    progress.progress(100, text="Pipeline complete.")

    put('cleaned_df', cleaned)
    put('processed_df', final)
    put('validation_complete', True)
    put('processing_complete', True)

    st.success("Analysis complete. Navigate to **Dashboard** to explore results.")
    st.balloons()

    st.markdown(f'### {icon("preview")} Quick Results', unsafe_allow_html=True)
    risk_counts = final['final_risk'].value_counts()
    rc1, rc2, rc3 = st.columns(3)
    rc1.metric("High Risk", risk_counts.get('High Risk', 0))
    rc2.metric("Medium Risk", risk_counts.get('Medium Risk', 0))
    rc3.metric("Low Risk", risk_counts.get('Low Risk', 0))
