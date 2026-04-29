"""
7_Reports.py – Export page with downloadable reports including PDF generation.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.style import inject_custom_css, sidebar_branding, require_auth, icon
from core.session import get, is_ready
from core.export import export_processed_csv, export_risk_list, generate_summary_report
from core.pdf_report import generate_pdf_report

inject_custom_css()
sidebar_branding()
require_auth()

st.markdown(f'<h1>{icon("download")} Reports & Export</h1>', unsafe_allow_html=True)
st.caption("Download processed data, risk lists, summary reports, and professional PDFs.")
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

# ═══════════════════════════════════════════
# SUMMARY METRICS
# ═══════════════════════════════════════════
st.markdown(f'### {icon("summarize")} Analysis Summary', unsafe_allow_html=True)

total = len(df)
high = len(df[df['final_risk'] == 'High Risk'])
medium = len(df[df['final_risk'] == 'Medium Risk'])
low = len(df[df['final_risk'] == 'Low Risk'])
avg_score = df['avg_percentage'].mean() if 'avg_percentage' in df.columns else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Students", total)
c2.metric("Avg Score", f"{avg_score:.1f}%")
c3.metric("High Risk", high)
c4.metric("Medium Risk", medium)
c5.metric("Low Risk", low)

st.markdown("---")

# ═══════════════════════════════════════════
# DOWNLOAD CARDS
# ═══════════════════════════════════════════
st.markdown(f'### {icon("file_download")} Download Reports', unsafe_allow_html=True)

dl1, dl2, dl3, dl4 = st.columns(4)

with dl1:
    st.markdown(f"""
    <div class="card" style="text-align:center; min-height:190px;
                border-top:3px solid #4f46e5;">
        <span class="mat-icon" style="font-size:32px; color:#4f46e5;">table_chart</span>
        <h4 style="margin:10px 0 6px 0; font-size:0.95rem;">Full Data</h4>
        <p style="color:#64748b; font-size:0.78rem;">
            Complete dataset with all derived features, scores, and predictions.</p>
    </div>
    """, unsafe_allow_html=True)
    csv_full = export_processed_csv(df)
    st.download_button("📥 Download CSV", data=csv_full,
        file_name="edurisk_processed_data.csv", mime="text/csv",
        use_container_width=True)

with dl2:
    st.markdown(f"""
    <div class="card" style="text-align:center; min-height:190px;
                border-top:3px solid #ef4444;">
        <span class="mat-icon danger" style="font-size:32px;">warning</span>
        <h4 style="margin:10px 0 6px 0; font-size:0.95rem;">Risk List</h4>
        <p style="color:#64748b; font-size:0.78rem;">
            Filtered list of High and Medium risk students with reasons.</p>
    </div>
    """, unsafe_allow_html=True)
    csv_risk = export_risk_list(df)
    st.download_button("📥 Download Risk CSV", data=csv_risk,
        file_name="edurisk_risk_list.csv", mime="text/csv",
        use_container_width=True)

with dl3:
    st.markdown(f"""
    <div class="card" style="text-align:center; min-height:190px;
                border-top:3px solid #10b981;">
        <span class="mat-icon success" style="font-size:32px;">description</span>
        <h4 style="margin:10px 0 6px 0; font-size:0.95rem;">Summary</h4>
        <p style="color:#64748b; font-size:0.78rem;">
            Human-readable text report with key findings and statistics.</p>
    </div>
    """, unsafe_allow_html=True)
    report_text = generate_summary_report(df, mapping, subjects)
    st.download_button("📥 Download TXT", data=report_text,
        file_name="edurisk_summary_report.txt", mime="text/plain",
        use_container_width=True)

with dl4:
    st.markdown(f"""
    <div class="card" style="text-align:center; min-height:190px;
                border-top:3px solid #7c3aed;">
        <span class="mat-icon" style="font-size:32px; color:#7c3aed;">picture_as_pdf</span>
        <h4 style="margin:10px 0 6px 0; font-size:0.95rem;">PDF Report</h4>
        <p style="color:#64748b; font-size:0.78rem;">
            Professional branded PDF with metrics, tables, and recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    with st.spinner("Generating PDF..."):
        pdf_bytes = generate_pdf_report(df, mapping, subjects)
    st.download_button("📥 Download PDF", data=pdf_bytes,
        file_name="edurisk_report.pdf", mime="application/pdf",
        use_container_width=True)

# ═══════════════════════════════════════════
# REPORT PREVIEW
# ═══════════════════════════════════════════
st.markdown("---")
st.markdown(f'### {icon("visibility")} Report Preview', unsafe_allow_html=True)
with st.expander("Click to preview the summary report", expanded=False):
    st.code(report_text, language="text")

# ═══════════════════════════════════════════
# AT-RISK TABLE
# ═══════════════════════════════════════════
st.markdown(f'### {icon("priority_high")} At-Risk Students', unsafe_allow_html=True)
risk_df = df[df['final_risk'].isin(['High Risk', 'Medium Risk'])].sort_values('risk_score', ascending=False)

name_col = mapping.get('name')
display_cols = [c for c in [name_col, mapping.get('class'), 'avg_percentage', 'risk_score', 'final_risk', 'risk_reasons']
                if c and c in risk_df.columns]

if display_cols and len(risk_df) > 0:
    st.dataframe(
        risk_df[display_cols].reset_index(drop=True),
        use_container_width=True, height=400,
        column_config={
            'avg_percentage': st.column_config.ProgressColumn("Avg %", min_value=0, max_value=100, format="%.1f%%"),
            'risk_score': st.column_config.ProgressColumn("Risk Score", min_value=0, max_value=100, format="%.1f"),
        },
    )
    st.caption(f"{len(risk_df)} students flagged for intervention")
else:
    st.success("No students flagged as at-risk.")
