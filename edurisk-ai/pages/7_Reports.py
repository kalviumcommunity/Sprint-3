"""
7_Reports.py – Export page for downloadable reports.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.style import inject_custom_css, sidebar_branding, require_auth, icon
from core.session import get, is_ready
from core.export import export_processed_csv, export_risk_list, generate_summary_report

inject_custom_css()
sidebar_branding()
require_auth()

st.markdown(f'<h1>{icon("download")} Reports & Export</h1>', unsafe_allow_html=True)
st.caption("Download processed data, risk lists, and summary reports.")
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

# ── Summary ──
st.markdown(f'### {icon("summarize")} Analysis Summary', unsafe_allow_html=True)

total = len(df)
high = len(df[df['final_risk'] == 'High Risk'])
medium = len(df[df['final_risk'] == 'Medium Risk'])
low = len(df[df['final_risk'] == 'Low Risk'])

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Students", total)
c2.metric("High Risk", high)
c3.metric("Medium Risk", medium)
c4.metric("Low Risk", low)

st.markdown("---")

# ── Downloads ──
st.markdown(f'### {icon("file_download")} Download Reports', unsafe_allow_html=True)

dl1, dl2, dl3 = st.columns(3)

with dl1:
    st.markdown(f"""
    <div class="card" style="text-align:center; min-height:170px;">
        <span class="mat-icon" style="font-size:28px;">table_chart</span>
        <h4 style="margin:8px 0 4px 0;">Full Processed Data</h4>
        <p style="color:#64748b; font-size:0.78rem;">
            Complete dataset with all derived features, scores, and predictions.</p>
    </div>
    """, unsafe_allow_html=True)
    csv_full = export_processed_csv(df)
    st.download_button("Download Processed CSV", data=csv_full,
        file_name="edurisk_processed_data.csv", mime="text/csv", width="stretch")

with dl2:
    st.markdown(f"""
    <div class="card" style="text-align:center; min-height:170px; border-color:#fecaca;">
        <span class="mat-icon danger" style="font-size:28px;">warning</span>
        <h4 style="margin:8px 0 4px 0;">At-Risk Student List</h4>
        <p style="color:#64748b; font-size:0.78rem;">
            Filtered list of High and Medium risk students with reasons.</p>
    </div>
    """, unsafe_allow_html=True)
    csv_risk = export_risk_list(df)
    st.download_button("Download Risk List CSV", data=csv_risk,
        file_name="edurisk_risk_list.csv", mime="text/csv", width="stretch")

with dl3:
    st.markdown(f"""
    <div class="card" style="text-align:center; min-height:170px; border-color:#bbf7d0;">
        <span class="mat-icon success" style="font-size:28px;">description</span>
        <h4 style="margin:8px 0 4px 0;">Summary Report</h4>
        <p style="color:#64748b; font-size:0.78rem;">
            Human-readable text report with key findings.</p>
    </div>
    """, unsafe_allow_html=True)
    report_text = generate_summary_report(df, mapping, subjects)
    st.download_button("Download Summary Report", data=report_text,
        file_name="edurisk_summary_report.txt", mime="text/plain", width="stretch")

# ── Preview ──
st.markdown("---")
st.markdown(f'### {icon("visibility")} Report Preview', unsafe_allow_html=True)
with st.expander("Click to preview the summary report", expanded=False):
    st.code(report_text, language="text")

# ── At-risk table ──
st.markdown(f'### {icon("priority_high")} At-Risk Students', unsafe_allow_html=True)
risk_df = df[df['final_risk'].isin(['High Risk', 'Medium Risk'])].sort_values('risk_score', ascending=False)

name_col = mapping.get('name')
display_cols = [c for c in [name_col, mapping.get('class'), 'avg_percentage', 'risk_score', 'final_risk', 'risk_reasons']
                if c and c in risk_df.columns]

if display_cols and len(risk_df) > 0:
    st.dataframe(risk_df[display_cols].reset_index(drop=True), width="stretch", height=400)
    st.caption(f"{len(risk_df)} students flagged for intervention")
else:
    st.success("No students flagged as at-risk.")
