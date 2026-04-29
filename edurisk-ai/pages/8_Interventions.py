"""
8_Interventions.py – Teacher intervention tracker.
Log, monitor, and update actions taken for at-risk students.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.style import inject_custom_css, sidebar_branding, require_auth, icon
from core.session import get, is_ready
from core.interventions import (
    log_intervention, get_interventions, update_status,
    get_intervention_stats, INTERVENTION_TYPES, STATUS_OPTIONS, STATUS_COLORS,
)

inject_custom_css()
sidebar_branding()
require_auth()

st.markdown(f'<h1>{icon("assignment")} Intervention Tracker</h1>', unsafe_allow_html=True)
st.caption("Log, monitor, and track actions taken for at-risk students.")
st.markdown("---")

# ═══════════════════════════════════════════
# STATS OVERVIEW
# ═══════════════════════════════════════════
stats = get_intervention_stats()

st.markdown(f'### {icon("analytics")} Overview', unsafe_allow_html=True)
s1, s2, s3, s4, s5 = st.columns(5)
s1.metric("Total Logged", stats.get('total', 0))
s2.metric("🔴 Pending", stats.get('Pending', 0))
s3.metric("🟡 In Progress", stats.get('In Progress', 0))
s4.metric("🟢 Resolved", stats.get('Resolved', 0))
s5.metric("🟣 Escalated", stats.get('Escalated', 0))

st.markdown("---")

# ═══════════════════════════════════════════
# LOG NEW INTERVENTION
# ═══════════════════════════════════════════
st.markdown(f'### {icon("add_circle")} Log New Intervention', unsafe_allow_html=True)

# Get student list from processed data if available
student_names = []
student_ids = []
if is_ready('processing_complete'):
    df = get('processed_df')
    mapping = get('mapping')
    if df is not None and mapping:
        name_col = mapping.get('name', 'name')
        id_col = mapping.get('student_id')
        if name_col in df.columns:
            # Only show at-risk students at top
            risk_df = df[df['final_risk'].isin(['High Risk', 'Medium Risk'])].sort_values('risk_score', ascending=False)
            student_names = risk_df[name_col].astype(str).tolist()
            if id_col and id_col in df.columns:
                student_ids = risk_df[id_col].astype(str).tolist()

with st.form("log_intervention", clear_on_submit=True):
    form_cols = st.columns(2)
    with form_cols[0]:
        if student_names:
            sel_name = st.selectbox("Student Name", ["-- Select --"] + student_names)
        else:
            sel_name = st.text_input("Student Name", placeholder="Enter student name")

        sel_type = st.selectbox("Intervention Type", INTERVENTION_TYPES)

    with form_cols[1]:
        sel_id = ""
        if student_names and student_ids:
            idx = student_names.index(sel_name) if sel_name in student_names else -1
            sel_id = student_ids[idx] if idx >= 0 else ""
            st.text_input("Student ID", value=sel_id, disabled=True)
        else:
            sel_id = st.text_input("Student ID", placeholder="Optional")

        # Get risk level from data
        sel_risk = 'High Risk'
        if is_ready('processing_complete') and df is not None and sel_name != "-- Select --":
            name_col = mapping.get('name', 'name')
            match = df[df[name_col].astype(str) == sel_name]
            if len(match) > 0:
                sel_risk = match.iloc[0].get('final_risk', 'High Risk')
        st.text_input("Risk Level", value=sel_risk, disabled=True)

    sel_notes = st.text_area("Notes / Action Plan", placeholder="Describe the intervention plan...",
                              height=100)

    teacher = ''
    user = st.session_state.get('current_user')
    if user:
        teacher = user.get('name', '')

    submitted = st.form_submit_button("Log Intervention", type="primary",
                                       use_container_width=True)
    if submitted:
        if sel_name and sel_name != "-- Select --":
            record = log_intervention(sel_name, sel_id, sel_risk, sel_type, sel_notes, teacher)
            st.success(f"✅ Intervention logged for **{sel_name}** (ID: #{record['id']})")
            st.rerun()
        else:
            st.error("Please select or enter a student name.")

st.markdown("---")

# ═══════════════════════════════════════════
# INTERVENTION LOG
# ═══════════════════════════════════════════
st.markdown(f'### {icon("list_alt")} Intervention Log', unsafe_allow_html=True)

# Filters
filter_cols = st.columns(3)
with filter_cols[0]:
    status_filter = st.multiselect("Filter by Status", STATUS_OPTIONS,
                                    default=STATUS_OPTIONS, key="int_status_filter")
with filter_cols[1]:
    risk_filter = st.multiselect("Filter by Risk",
        ['High Risk', 'Medium Risk', 'Low Risk'],
        default=['High Risk', 'Medium Risk'], key="int_risk_filter")
with filter_cols[2]:
    st.markdown("<br>", unsafe_allow_html=True)

interventions = get_interventions(status_filter=status_filter, risk_filter=risk_filter)

if not interventions:
    st.info("No interventions logged yet. Use the form above to log your first intervention.")
else:
    for item in interventions:
        status = item.get('status', 'Pending')
        status_color = STATUS_COLORS.get(status, '#94a3b8')
        risk = item.get('risk_level', 'Unknown')
        risk_color = '#ef4444' if risk == 'High Risk' else '#f59e0b' if risk == 'Medium Risk' else '#10b981'

        with st.container():
            st.markdown(f"""
            <div style="background:#fff; border:1px solid #e2e8f0; border-radius:12px;
                        padding:16px 20px; margin-bottom:12px; border-left:4px solid {status_color};
                        box-shadow:0 1px 4px rgba(0,0,0,0.04);">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
                    <div>
                        <strong style="color:#0f172a; font-size:1rem;">
                            {item['student_name']}</strong>
                        <span style="color:#94a3b8; font-size:0.8rem; margin-left:8px;">
                            #{item['id']} • {item.get('student_id', '')}</span>
                    </div>
                    <div style="display:flex; gap:8px; align-items:center;">
                        <span style="background:{risk_color}20; color:{risk_color};
                                     padding:2px 10px; border-radius:12px;
                                     font-size:0.72rem; font-weight:600;">{risk}</span>
                        <span style="background:{status_color}; color:white;
                                     padding:3px 12px; border-radius:12px;
                                     font-size:0.72rem; font-weight:700;">{status}</span>
                    </div>
                </div>
                <div style="margin-top:8px;">
                    <span style="color:#4f46e5; font-size:0.82rem; font-weight:500;">
                        {item['type']}</span>
                    {f'<span style="color:#94a3b8; font-size:0.75rem;"> • By {item["teacher"]}</span>' if item.get('teacher') else ''}
                </div>
                <p style="color:#64748b; font-size:0.83rem; margin:6px 0 0 0;
                          white-space:pre-wrap;">{item.get('notes', '')[:200]}</p>
                <div style="margin-top:6px; color:#94a3b8; font-size:0.7rem;">
                    Created: {item.get('created_at', '')[:16]} &nbsp;•&nbsp;
                    Updated: {item.get('updated_at', '')[:16]}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Status update buttons
            btn_cols = st.columns(5)
            item_id = item['id']
            for j, new_status in enumerate(STATUS_OPTIONS):
                if new_status != status:
                    with btn_cols[j]:
                        if st.button(f"{new_status}", key=f"status_{item_id}_{new_status}",
                                    use_container_width=True):
                            update_status(item_id, new_status)
                            st.rerun()

    st.caption(f"Showing {len(interventions)} intervention(s)")
