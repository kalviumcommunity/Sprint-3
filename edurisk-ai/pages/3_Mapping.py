"""
3_Mapping.py – Column mapping with auto-detection and manual override.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.style import inject_custom_css, sidebar_branding, require_auth, icon
from core.session import put, get, is_ready
from core.mapper import detect_columns

inject_custom_css()
sidebar_branding()
require_auth()

st.markdown(f'<h1>{icon("link")} Column Mapping</h1>', unsafe_allow_html=True)
st.caption("Review and confirm the auto-detected column assignments.")
st.markdown("---")

if not is_ready('upload_complete'):
    st.warning("Please upload a file first on the **Upload** page.")
    st.stop()

df = get('raw_df')
if df is None:
    st.error("No data found in session. Please re-upload.")
    st.stop()

columns = df.columns.tolist()
auto_mapping, auto_subjects = detect_columns(columns)

st.markdown(f'### {icon("auto_fix_high")} Auto-Detected Mapping', unsafe_allow_html=True)
st.markdown("""
<div class="card" style="padding:14px 18px; margin-bottom:18px;">
    <p style="color:#64748b; margin:0; font-size:0.83rem;">
        The system has matched your columns to expected fields.
        Review and adjust using the dropdowns below.</p>
</div>
""", unsafe_allow_html=True)

none_option = ["-- Not Available --"]
all_options = none_option + columns

st.markdown(f'#### {icon("badge")} Metadata Columns', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.selectbox("Student ID Column", all_options,
        index=all_options.index(auto_mapping['student_id']) if auto_mapping.get('student_id') in all_options else 0,
        key="map_student_id")
    st.selectbox("Class / Grade Column", all_options,
        index=all_options.index(auto_mapping['class']) if auto_mapping.get('class') in all_options else 0,
        key="map_class")

with col2:
    st.selectbox("Student Name Column", all_options,
        index=all_options.index(auto_mapping['name']) if auto_mapping.get('name') in all_options else 0,
        key="map_name")
    st.selectbox("Attendance Column", all_options,
        index=all_options.index(auto_mapping['attendance']) if auto_mapping.get('attendance') in all_options else 0,
        key="map_attendance")

confirmed_mapping = {}
for key, widget_key in [('student_id', 'map_student_id'), ('name', 'map_name'),
                         ('class', 'map_class'), ('attendance', 'map_attendance')]:
    val = st.session_state.get(widget_key, none_option[0])
    confirmed_mapping[key] = val if val != none_option[0] else None

mapped_cols = [v for v in confirmed_mapping.values() if v is not None]
remaining = [c for c in columns if c not in mapped_cols]

st.markdown(f'#### {icon("menu_book")} Subject Columns', unsafe_allow_html=True)
st.markdown("All unmapped columns are treated as subjects. Deselect any that are not:")

selected_subjects = st.multiselect("Subject Columns", remaining, default=remaining, key="map_subjects")

st.markdown("---")
st.markdown(f'### {icon("summarize")} Mapping Summary', unsafe_allow_html=True)

summary_data = {
    "Field": ["Student ID", "Name", "Class", "Attendance", "Subjects"],
    "Mapped To": [
        confirmed_mapping.get('student_id', '—'),
        confirmed_mapping.get('name', '—'),
        confirmed_mapping.get('class', '—'),
        confirmed_mapping.get('attendance', '—'),
        ", ".join(selected_subjects) if selected_subjects else '—',
    ],
}
st.table(summary_data)

if st.button("Confirm Mapping", type="primary", width="stretch"):
    if not selected_subjects:
        st.error("At least one subject column is required.")
    else:
        put('mapping', confirmed_mapping)
        put('subjects', selected_subjects)
        put('mapping_complete', True)
        st.success("Mapping confirmed. Navigate to **Validation**.")
        st.balloons()
