"""
1_Home.py – Welcome and overview page with animated workflow.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.style import inject_custom_css, sidebar_branding, require_auth, icon

inject_custom_css()
sidebar_branding()
require_auth()

# ── Hero ──
st.markdown(f"""
<div style="text-align:center; padding: 32px 20px 20px 20px;">
    <h1 style="font-size:2rem;">
        <span class="mat-icon" style="font-size:28px;">waving_hand</span>
        Welcome to <span style="background: linear-gradient(135deg, #4f46e5, #7c3aed);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;">EDURISK AI</span></h1>
    <p style="color:#64748b; font-size:0.95rem; max-width:600px; margin:0 auto;">
        An intelligent early-warning system that helps teachers identify
        at-risk students and take timely, data-driven action.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Animated Workflow Steps ──
st.markdown(f'### {icon("route")} How It Works', unsafe_allow_html=True)

steps = [
    ("cloud_upload", "Upload", "Upload your student data in CSV or XLSX format", "#4f46e5", "1"),
    ("link", "Map Columns", "Confirm auto-detected column mappings", "#7c3aed", "2"),
    ("check_circle", "Validate", "Review data quality and health score", "#0891b2", "3"),
    ("dashboard", "Dashboard", "Explore analytics, charts, and risk distribution", "#059669", "4"),
    ("person_search", "Student Profile", "Deep-dive into individual student performance", "#d97706", "5"),
    ("download", "Reports", "Download processed data and risk reports", "#ef4444", "6"),
    ("assignment", "Interventions", "Track actions taken for at-risk students", "#8b5cf6", "7"),
    ("compare_arrows", "Compare", "Compare datasets to track improvement over time", "#06b6d4", "8"),
]

# Display in rows of 4
for row_start in range(0, len(steps), 4):
    cols = st.columns(4)
    for j, col in enumerate(cols):
        idx = row_start + j
        if idx < len(steps):
            ico, title, desc, color, num = steps[idx]
            with col:
                st.markdown(f"""
                <div class="card" style="text-align:center; min-height:140px;
                            border-top:3px solid {color}; margin-bottom:12px;
                            position:relative;">
                    <div style="position:absolute; top:-12px; left:50%; transform:translateX(-50%);
                                background:{color}; color:white; width:24px; height:24px;
                                border-radius:50%; display:flex; align-items:center;
                                justify-content:center; font-size:0.75rem; font-weight:700;
                                box-shadow:0 2px 6px {color}40;">{num}</div>
                    <div style="margin-top:12px;">
                        <span class="mat-icon" style="font-size:28px; color:{color}; margin:0;">{ico}</span>
                    </div>
                    <h4 style="margin:8px 0 4px 0; font-size:0.92rem; color:#0f172a;">{title}</h4>
                    <p style="color:#64748b; font-size:0.78rem; margin:0; line-height:1.4;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)

st.markdown("---")

# ── Supported Data Format ──
st.markdown(f'### {icon("table_chart")} Supported Data Format', unsafe_allow_html=True)

st.markdown("""
<div class="card" style="padding:20px 24px;">
    <p style="color:#64748b; font-size:0.88rem; margin:0 0 12px 0;">
        Your spreadsheet should contain columns like:</p>
    <table style="width:100%; border-collapse:collapse; font-size:0.88rem;">
        <thead>
            <tr style="border-bottom:2px solid #e2e8f0;">
                <th style="text-align:left; padding:8px 12px; color:#334155;">Column</th>
                <th style="text-align:left; padding:8px 12px; color:#334155;">Examples</th>
                <th style="text-align:left; padding:8px 12px; color:#334155;">Required</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom:1px solid #f1f5f9;">
                <td style="padding:8px 12px; font-weight:600;">Student ID</td>
                <td style="padding:8px 12px; color:#64748b;"><code>Roll_No</code>, <code>ID</code></td>
                <td style="padding:8px 12px;"><span style="color:#10b981;">✓</span></td>
            </tr>
            <tr style="border-bottom:1px solid #f1f5f9;">
                <td style="padding:8px 12px; font-weight:600;">Name</td>
                <td style="padding:8px 12px; color:#64748b;"><code>Name</code>, <code>Student_Name</code></td>
                <td style="padding:8px 12px;"><span style="color:#10b981;">✓</span></td>
            </tr>
            <tr style="border-bottom:1px solid #f1f5f9;">
                <td style="padding:8px 12px; font-weight:600;">Class</td>
                <td style="padding:8px 12px; color:#64748b;"><code>Class</code>, <code>Grade</code></td>
                <td style="padding:8px 12px;"><span style="color:#f59e0b;">Optional</span></td>
            </tr>
            <tr style="border-bottom:1px solid #f1f5f9;">
                <td style="padding:8px 12px; font-weight:600;">Attendance</td>
                <td style="padding:8px 12px; color:#64748b;"><code>Attendance</code>, <code>Att</code></td>
                <td style="padding:8px 12px;"><span style="color:#f59e0b;">Optional</span></td>
            </tr>
            <tr>
                <td style="padding:8px 12px; font-weight:600;">Subject Marks</td>
                <td style="padding:8px 12px; color:#64748b;"><code>Maths</code>, <code>Science</code>, <code>English</code></td>
                <td style="padding:8px 12px;"><span style="color:#10b981;">✓ (1+)</span></td>
            </tr>
        </tbody>
    </table>
    <p style="color:#94a3b8; font-size:0.78rem; margin:12px 0 0 0;">
        The system auto-detects most formats. You will confirm mappings before analysis.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── CTA ──
st.markdown(f"""
<div style="background:linear-gradient(135deg, #eff6ff, #dbeafe);
            padding:18px 24px; border-radius:14px; border-left:4px solid #4f46e5;
            box-shadow:0 2px 8px rgba(79,70,229,0.08);">
    <span class="mat-icon" style="font-size:20px;">rocket_launch</span>
    <strong style="color:#1e3a5f;">Ready to start?</strong>
    <p style="color:#1e3a5f; margin:6px 0 0 0; font-size:0.88rem; opacity:0.85;">
        Use the sidebar to navigate to <b>Upload</b> and begin the analysis workflow.</p>
</div>
""", unsafe_allow_html=True)
