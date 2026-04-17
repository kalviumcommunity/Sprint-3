"""
1_Home.py – Welcome and overview page.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.style import inject_custom_css, sidebar_branding, require_auth, icon

inject_custom_css()
sidebar_branding()
require_auth()

st.markdown(f"""
<div style="text-align:center; padding: 32px 20px 16px 20px;">
    <h1 style="font-size:2rem;">
        {icon("waving_hand")} Welcome to EDURISK AI</h1>
    <p style="color:#64748b; font-size:0.95rem; max-width:600px; margin:0 auto;">
        An intelligent early-warning system that helps teachers identify
        at-risk students and take timely action.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown(f'### {icon("route")} How It Works', unsafe_allow_html=True)

steps = [
    ("cloud_upload", "Upload", "Upload your student data in CSV or XLSX format"),
    ("link", "Map Columns", "Confirm auto-detected column mappings"),
    ("check_circle", "Validate", "Review data quality and health score"),
    ("dashboard", "Dashboard", "Explore analytics, charts, and risk distribution"),
    ("person_search", "Student Profile", "Deep-dive into individual student performance"),
    ("download", "Reports", "Download processed data and risk reports"),
]

cols = st.columns(3)
for i, (ico, title, desc) in enumerate(steps):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="card" style="margin-bottom:14px; min-height:110px;">
            <span class="mat-icon" style="font-size:24px;">{ico}</span>
            <h4 style="margin:6px 0 4px 0; font-size:0.95rem;">{title}</h4>
            <p style="color:#64748b; font-size:0.82rem; margin:0;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

st.markdown(f'### {icon("table_chart")} Supported Data Format', unsafe_allow_html=True)
st.markdown("""
Your spreadsheet should contain columns like:

| Column | Examples |
|--------|----------|
| **Student ID** | `Roll_No`, `ID`, `roll` |
| **Name** | `Name`, `Student_Name` |
| **Class** | `Class`, `Grade`, `Std` |
| **Attendance** | `Attendance`, `Att`, `Present` |
| **Subject Marks** | `Maths`, `Science`, `English`, etc. |

The system auto-detects most formats. You will confirm mappings before analysis.
""")

st.info("Use the sidebar to navigate to **Upload** and begin.")
