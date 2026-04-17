"""
5_Dashboard.py – Analytics dashboard with charts and risk table.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.style import inject_custom_css, sidebar_branding, require_auth, icon
from core.session import get, is_ready
from visuals.charts import (
    subject_avg_bar_chart, risk_distribution_pie,
    attendance_vs_marks_scatter, class_comparison_chart,
)

inject_custom_css()
sidebar_branding()
require_auth()

st.markdown(f'<h1>{icon("dashboard")} Analytics Dashboard</h1>', unsafe_allow_html=True)
st.caption("Comprehensive overview of student performance and risk distribution.")
st.markdown("---")

if not is_ready('processing_complete'):
    st.warning("Please complete the analysis pipeline on the **Validation** page first.")
    st.stop()

df = get('processed_df')
mapping = get('mapping')
subjects = get('subjects')

if df is None:
    st.error("Processed data not found. Please re-run the pipeline.")
    st.stop()

# ── TOP METRICS ──
st.markdown(f'### {icon("trending_up")} Key Metrics', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)

m1.metric("Total Students", f"{len(df):,}")
high_risk = len(df[df['final_risk'] == 'High Risk'])
m2.metric("High Risk", f"{high_risk}", delta=f"{high_risk/len(df)*100:.1f}%" if len(df) > 0 else "0%",
          delta_color="inverse")
m3.metric("Avg Score", f"{df['avg_percentage'].mean():.1f}%")

weakest_sub, lowest_avg = None, 100
for sub in subjects:
    pct_col = f"{sub}_pct"
    if pct_col in df.columns:
        avg = df[pct_col].mean()
        if avg < lowest_avg:
            lowest_avg = avg
            weakest_sub = sub
m4.metric("Weakest Subject", weakest_sub or "N/A", delta=f"{lowest_avg:.1f}%" if weakest_sub else None,
          delta_color="inverse")

st.markdown("---")

# ── CHARTS ──
st.markdown(f'### {icon("insert_chart")} Visual Analytics', unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(["Subject Averages", "Risk Distribution", "Attendance vs Marks", "Class Comparison"])

with tab1:
    fig = subject_avg_bar_chart(df, subjects)
    st.pyplot(fig)
with tab2:
    fig = risk_distribution_pie(df)
    st.pyplot(fig)
with tab3:
    fig = attendance_vs_marks_scatter(df, mapping)
    st.pyplot(fig)
with tab4:
    fig = class_comparison_chart(df, mapping, subjects)
    st.pyplot(fig)

st.markdown("---")

# ── RISK TABLE ──
st.markdown(f'### {icon("table_view")} Student Risk Overview', unsafe_allow_html=True)

fcol1, fcol2, fcol3 = st.columns(3)
with fcol1:
    risk_filter = st.multiselect("Filter by Risk Level",
        ['High Risk', 'Medium Risk', 'Low Risk'],
        default=['High Risk', 'Medium Risk', 'Low Risk'])
with fcol2:
    class_col = mapping.get('class')
    if class_col and class_col in df.columns:
        classes = ['All'] + sorted(df[class_col].astype(str).unique().tolist())
        selected_class = st.selectbox("Filter by Class", classes)
    else:
        selected_class = 'All'
with fcol3:
    sort_by = st.selectbox("Sort by", ['risk_score', 'avg_percentage', 'final_risk'], index=0)

filtered = df[df['final_risk'].isin(risk_filter)]
if selected_class != 'All' and class_col and class_col in filtered.columns:
    filtered = filtered[filtered[class_col].astype(str) == selected_class]

ascending = sort_by == 'avg_percentage'
filtered = filtered.sort_values(sort_by, ascending=ascending)

name_col = mapping.get('name', 'name')
display_cols = [c for c in [name_col, class_col, 'avg_percentage', 'risk_score', 'final_risk', 'risk_reasons']
                if c and c in filtered.columns]

if display_cols:
    st.dataframe(
        filtered[display_cols].reset_index(drop=True),
        width="stretch", height=450,
        column_config={
            'avg_percentage': st.column_config.ProgressColumn("Avg %", min_value=0, max_value=100, format="%.1f%%"),
            'risk_score': st.column_config.ProgressColumn("Risk Score", min_value=0, max_value=100, format="%.1f"),
        },
    )
    st.caption(f"Showing {len(filtered)} of {len(df)} students")
else:
    st.info("No displayable columns found.")
