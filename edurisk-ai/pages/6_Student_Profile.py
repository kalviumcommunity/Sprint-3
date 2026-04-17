"""
6_Student_Profile.py – Individual student deep-dive.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.style import inject_custom_css, sidebar_branding, require_auth, icon
from core.session import get, is_ready
from visuals.charts import student_radar_chart

inject_custom_css()
sidebar_branding()
require_auth()

st.markdown(f'<h1>{icon("person_search")} Student Profile</h1>', unsafe_allow_html=True)
st.caption("Search and explore individual student performance in detail.")
st.markdown("---")

if not is_ready('processing_complete'):
    st.warning("Please complete the analysis pipeline on the **Validation** page first.")
    st.stop()

df = get('processed_df')
mapping = get('mapping')
subjects = get('subjects')

if df is None:
    st.error("Processed data not found.")
    st.stop()

name_col = mapping.get('name', 'name')
id_col = mapping.get('student_id')
att_col = mapping.get('attendance')
class_col = mapping.get('class')

# ── Search ──
st.markdown(f'### {icon("search")} Find a Student', unsafe_allow_html=True)
search_col1, search_col2 = st.columns(2)

with search_col1:
    if name_col and name_col in df.columns:
        names = sorted(df[name_col].astype(str).unique().tolist())
        selected_name = st.selectbox("Search by Name", ["-- Select --"] + names, key="profile_name")
    else:
        selected_name = "-- Select --"

with search_col2:
    if id_col and id_col in df.columns:
        ids = sorted(df[id_col].astype(str).unique().tolist())
        selected_id = st.selectbox("Search by ID", ["-- Select --"] + ids, key="profile_id")
    else:
        selected_id = "-- Select --"

student = None
if selected_name != "-- Select --" and name_col in df.columns:
    matches = df[df[name_col].astype(str) == selected_name]
    if len(matches) > 0:
        student = matches.iloc[0]
elif selected_id != "-- Select --" and id_col and id_col in df.columns:
    matches = df[df[id_col].astype(str) == selected_id]
    if len(matches) > 0:
        student = matches.iloc[0]

if student is None:
    st.info("Select a student above to view their profile.")
    st.stop()

st.markdown("---")

# ── Student Card ──
risk = student.get('final_risk', 'Unknown')
risk_styles = {
    'High Risk': ('#dc2626', 'error'),
    'Medium Risk': ('#d97706', 'warning'),
    'Low Risk': ('#059669', 'success'),
}
r_color, r_icon_cls = risk_styles.get(risk, ('#94a3b8', 'muted'))

st.markdown(f"""
<div class="card" style="border-left: 4px solid {r_color}; margin-bottom:20px;">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
        <div>
            <h2 style="margin:0 0 4px 0;">{student.get(name_col, 'Unknown')}</h2>
            <p style="color:#64748b; margin:0; font-size:0.9rem;">
                {f'ID: {student.get(id_col, "N/A")}' if id_col else ''}
                {f' | Class: {student.get(class_col, "N/A")}' if class_col else ''}
            </p>
        </div>
        <div style="text-align:right;">
            <p style="font-size:1.4rem; font-weight:700; color:{r_color}; margin:0;">
                <span class="mat-icon {r_icon_cls}" style="font-size:22px;">
                    {'cancel' if risk == 'High Risk' else 'warning' if risk == 'Medium Risk' else 'check_circle'}
                </span> {risk}
            </p>
            <p style="color:#64748b; margin:0; font-size:0.82rem;">
                Risk Score: {student.get('risk_score', 'N/A')}</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Metrics ──
mc1, mc2, mc3, mc4 = st.columns(4)
mc1.metric("Average Score", f"{student.get('avg_percentage', 0):.1f}%")
att_val = student.get(att_col, 'N/A') if att_col else 'N/A'
mc2.metric("Attendance", f"{att_val}%" if att_val != 'N/A' else 'N/A')
mc3.metric("Z-Score", f"{student.get('z_score', 0):.2f}")
mc4.metric("Weak Subjects", f"{int(student.get('weak_subject_count', 0))}")

st.markdown("---")

# ── Radar + Subject Breakdown ──
left, right = st.columns([1, 1])

with left:
    st.markdown(f'#### {icon("radar")} Performance Radar', unsafe_allow_html=True)
    class_averages = {}
    for sub in subjects:
        pct_col = f"{sub}_pct"
        if pct_col in df.columns:
            class_averages[sub] = df[pct_col].mean()
    fig = student_radar_chart(student, subjects, class_averages)
    st.pyplot(fig)

with right:
    st.markdown(f'#### {icon("menu_book")} Subject Breakdown', unsafe_allow_html=True)
    for sub in subjects:
        pct_col = f"{sub}_pct"
        val = student.get(pct_col, student.get(sub, 0))
        class_avg = class_averages.get(sub, 50)
        delta = val - class_avg

        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.markdown(f"**{sub}**")
            st.progress(min(val / 100, 1.0))
        with col_b:
            delta_text = f"+{delta:.1f}" if delta >= 0 else f"{delta:.1f}"
            color = "#059669" if delta >= 0 else "#dc2626"
            st.markdown(f"""
            <div style="text-align:center; padding-top:8px;">
                <span style="font-weight:700; font-size:1.05rem; color:#0f172a;">{val:.0f}%</span><br>
                <span style="color:{color}; font-size:0.78rem;">{delta_text} vs avg</span>
            </div>
            """, unsafe_allow_html=True)

# ── Explanations ──
st.markdown("---")
st.markdown(f'### {icon("lightbulb")} Risk Explanation', unsafe_allow_html=True)

explanations = student.get('explanations', [])
if isinstance(explanations, list):
    for reason in explanations:
        st.markdown(f"""
        <div style="background:#f8fafc; padding:10px 16px; border-radius:8px;
                    border-left:3px solid {r_color}; margin-bottom:6px;">
            <span style="color:#334155; font-size:0.9rem;">{reason}</span>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info(str(explanations))
