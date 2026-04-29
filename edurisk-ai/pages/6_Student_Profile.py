"""
6_Student_Profile.py – Individual student deep-dive with interactive Plotly
charts, risk gauge meter, and AI-powered recommendations.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.style import inject_custom_css, sidebar_branding, require_auth, icon
from core.session import get, is_ready
from core.recommendations import generate_recommendations
from visuals.charts import student_radar_chart, risk_gauge

inject_custom_css()
sidebar_branding()
require_auth()

st.markdown(f'<h1>{icon("person_search")} Student Profile</h1>', unsafe_allow_html=True)
st.caption("Search and explore individual student performance with AI-powered insights.")
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

# ═══════════════════════════════════════════
# SEARCH
# ═══════════════════════════════════════════
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
    st.info("Select a student above to view their detailed profile.")
    st.stop()

st.markdown("---")

# ═══════════════════════════════════════════
# STUDENT HERO CARD
# ═══════════════════════════════════════════
risk = student.get('final_risk', 'Unknown')
risk_score = student.get('risk_score', 0)
risk_styles = {
    'High Risk': ('#ef4444', 'linear-gradient(135deg, #fef2f2, #fecaca)', '#7f1d1d'),
    'Medium Risk': ('#f59e0b', 'linear-gradient(135deg, #fffbeb, #fef3c7)', '#78350f'),
    'Low Risk': ('#10b981', 'linear-gradient(135deg, #ecfdf5, #d1fae5)', '#065f46'),
}
r_color, r_bg, r_text = risk_styles.get(risk, ('#94a3b8', '#f1f5f9', '#334155'))

risk_icon = 'cancel' if risk == 'High Risk' else 'warning' if risk == 'Medium Risk' else 'check_circle'

st.markdown(f"""
<div style="background:{r_bg}; border-radius:16px; padding:24px 28px;
            border-left:5px solid {r_color}; margin-bottom:20px;
            box-shadow:0 4px 16px rgba(0,0,0,0.06);">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
        <div>
            <h2 style="margin:0 0 4px 0; color:#0f172a; font-size:1.6rem;">
                {student.get(name_col, 'Unknown')}</h2>
            <p style="color:#64748b; margin:0; font-size:0.92rem;">
                {f'ID: {student.get(id_col, "N/A")}' if id_col else ''}
                {f' &nbsp;•&nbsp; Class: {student.get(class_col, "N/A")}' if class_col else ''}
            </p>
        </div>
        <div style="text-align:right;">
            <div style="background:{r_color}; color:white; padding:8px 20px;
                        border-radius:24px; font-weight:700; font-size:1rem;
                        display:inline-block; box-shadow:0 2px 8px {r_color}40;">
                <span class="mat-icon" style="font-size:18px; color:white; margin-right:4px;
                      vertical-align:middle;">{risk_icon}</span>
                {risk}
            </div>
            <p style="color:{r_text}; margin:6px 0 0 0; font-size:0.82rem; font-weight:500;">
                Risk Score: {risk_score:.1f} / 100</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# METRICS ROW
# ═══════════════════════════════════════════
mc1, mc2, mc3, mc4 = st.columns(4)
mc1.metric("Average Score", f"{student.get('avg_percentage', 0):.1f}%")
att_val = student.get(att_col, 'N/A') if att_col else 'N/A'
mc2.metric("Attendance", f"{att_val}%" if att_val != 'N/A' else 'N/A')
mc3.metric("Z-Score", f"{student.get('z_score', 0):.2f}")
mc4.metric("Weak Subjects", f"{int(student.get('weak_subject_count', 0))}")

st.markdown("---")

# ═══════════════════════════════════════════
# RADAR + GAUGE
# ═══════════════════════════════════════════
col_radar, col_gauge = st.columns([3, 2])

with col_radar:
    st.markdown(f'#### {icon("radar")} Performance Radar', unsafe_allow_html=True)
    class_averages = {}
    for sub in subjects:
        pct_col = f"{sub}_pct"
        if pct_col in df.columns:
            class_averages[sub] = df[pct_col].mean()
    fig = student_radar_chart(student, subjects, class_averages)
    st.plotly_chart(fig, use_container_width=True)

with col_gauge:
    st.markdown(f'#### {icon("speed")} Risk Assessment', unsafe_allow_html=True)
    fig = risk_gauge(risk_score, risk)
    st.plotly_chart(fig, use_container_width=True)

    # Mini legend
    st.markdown("""
    <div style="display:flex; gap:12px; justify-content:center; margin-top:8px;">
        <span style="font-size:0.75rem;">
            <span style="background:#10b981; width:10px; height:10px; border-radius:50%;
                         display:inline-block;"></span> Low (0-35)</span>
        <span style="font-size:0.75rem;">
            <span style="background:#f59e0b; width:10px; height:10px; border-radius:50%;
                         display:inline-block;"></span> Medium (35-60)</span>
        <span style="font-size:0.75rem;">
            <span style="background:#ef4444; width:10px; height:10px; border-radius:50%;
                         display:inline-block;"></span> High (60-100)</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════
# SUBJECT BREAKDOWN
# ═══════════════════════════════════════════
st.markdown(f'### {icon("menu_book")} Subject Breakdown', unsafe_allow_html=True)

subject_cols = st.columns(min(len(subjects), 3))
for i, sub in enumerate(subjects):
    pct_col = f"{sub}_pct"
    val = student.get(pct_col, student.get(sub, 0))
    class_avg = class_averages.get(sub, 50)
    delta = val - class_avg

    with subject_cols[i % len(subject_cols)]:
        if val >= 70:
            card_border = '#10b981'
            grade_label = 'Excellent'
        elif val >= 50:
            card_border = '#4f46e5'
            grade_label = 'Good'
        elif val >= 40:
            card_border = '#f59e0b'
            grade_label = 'Pass'
        else:
            card_border = '#ef4444'
            grade_label = 'Fail'

        delta_text = f"+{delta:.1f}" if delta >= 0 else f"{delta:.1f}"
        delta_color = "#10b981" if delta >= 0 else "#ef4444"
        delta_arrow = "↑" if delta >= 0 else "↓"

        st.markdown(f"""
        <div style="background:#fff; border:1px solid #e2e8f0; border-radius:12px;
                    padding:16px; margin-bottom:12px; border-top:3px solid {card_border};
                    box-shadow:0 1px 4px rgba(0,0,0,0.04);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <strong style="color:#0f172a; font-size:0.95rem;">{sub}</strong>
                <span style="background:{card_border}15; color:{card_border};
                             padding:2px 10px; border-radius:12px;
                             font-size:0.72rem; font-weight:600;">{grade_label}</span>
            </div>
            <div style="margin-top:10px;">
                <span style="font-size:1.8rem; font-weight:800; color:#0f172a;">{val:.0f}%</span>
            </div>
            <div style="margin-top:6px; font-size:0.8rem;">
                <span style="color:{delta_color}; font-weight:600;">{delta_arrow} {delta_text}%</span>
                <span style="color:#94a3b8;"> vs class avg ({class_avg:.0f}%)</span>
            </div>
            <div style="background:#e2e8f0; border-radius:6px; height:6px; margin-top:8px; overflow:hidden;">
                <div style="background:{card_border}; height:100%; width:{min(val, 100)}%;
                            border-radius:6px; transition:width 0.5s;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════
# RISK EXPLANATIONS
# ═══════════════════════════════════════════
st.markdown(f'### {icon("lightbulb")} Risk Explanation', unsafe_allow_html=True)

explanations = student.get('explanations', [])
if isinstance(explanations, list):
    for reason in explanations:
        st.markdown(f"""
        <div style="background:#f8fafc; padding:12px 16px; border-radius:10px;
                    border-left:3px solid {r_color}; margin-bottom:8px;
                    box-shadow:0 1px 3px rgba(0,0,0,0.04);">
            <span style="color:#334155; font-size:0.9rem;">{reason}</span>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info(str(explanations))

st.markdown("---")

# ═══════════════════════════════════════════
# AI RECOMMENDATIONS
# ═══════════════════════════════════════════
st.markdown(f'### {icon("auto_awesome")} AI-Powered Recommendations', unsafe_allow_html=True)

recommendations = generate_recommendations(student, mapping, subjects)

priority_styles = {
    'critical': ('linear-gradient(135deg, #fef2f2, #fecaca)', '#ef4444', '#7f1d1d'),
    'high': ('linear-gradient(135deg, #fff7ed, #fed7aa)', '#f97316', '#7c2d12'),
    'medium': ('linear-gradient(135deg, #eff6ff, #dbeafe)', '#3b82f6', '#1e3a5f'),
    'info': ('linear-gradient(135deg, #ecfdf5, #d1fae5)', '#10b981', '#065f46'),
}

if recommendations:
    for rec in recommendations:
        bg, border, text_color = priority_styles.get(rec['priority'], priority_styles['info'])
        priority_label = rec['priority'].upper()
        st.markdown(f"""
        <div style="background:{bg}; padding:16px 20px; border-radius:12px;
                    border-left:4px solid {border}; margin-bottom:10px;
                    box-shadow:0 1px 4px rgba(0,0,0,0.04);">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                <span style="font-size:1.2rem;">{rec['icon']}</span>
                <strong style="color:{text_color}; font-size:0.95rem;">{rec['title']}</strong>
                <span style="background:{border}; color:white; padding:1px 8px;
                             border-radius:10px; font-size:0.65rem; font-weight:700;
                             margin-left:auto;">{priority_label}</span>
            </div>
            <p style="color:{text_color}; margin:4px 0 0 26px; font-size:0.85rem;
                      opacity:0.85; line-height:1.5;">{rec['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.success("No specific recommendations — student is performing well.")
