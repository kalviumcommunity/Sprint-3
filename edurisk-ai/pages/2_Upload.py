"""
2_Upload.py – File upload page.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.style import inject_custom_css, sidebar_branding, require_auth, icon
from core.session import put, get
from core.loader import load_data

inject_custom_css()
sidebar_branding()
require_auth()

st.markdown(f'<h1>{icon("cloud_upload")} Upload Student Data</h1>', unsafe_allow_html=True)
st.caption("Upload a CSV or XLSX file containing student marks and attendance data.")
st.markdown("---")

SAMPLE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'samples', 'sample_data.csv')

col_a, col_b = st.columns([3, 1])
with col_b:
    if os.path.exists(SAMPLE_PATH):
        with open(SAMPLE_PATH, 'rb') as f:
            st.download_button(
                label="Download Sample",
                data=f,
                file_name="edurisk_sample_data.csv",
                mime="text/csv",
            )
    else:
        st.warning("Sample not found. Run `python models/train.py`.")

with col_a:
    st.markdown(f"""
    <div class="card" style="padding:14px 18px; margin-bottom:16px;">
        <p style="color:#64748b; margin:0; font-size:0.85rem;">
            {icon("folder")} <b style="color:#334155;">Formats:</b> .csv, .xlsx
            &nbsp;&nbsp;{icon("checklist")} <b style="color:#334155;">Required:</b> Student ID, Name, Marks
            &nbsp;&nbsp;{icon("add_chart")} <b style="color:#334155;">Optional:</b> Attendance, Class
        </p>
    </div>
    """, unsafe_allow_html=True)

uploaded = st.file_uploader(
    "Drag and drop or browse your file",
    type=['csv', 'xlsx', 'xls'],
    key="file_uploader",
)

if uploaded is not None:
    try:
        with st.spinner("Reading file..."):
            df = load_data(uploaded)

        put('raw_df', df)
        put('file_name', uploaded.name)
        put('upload_complete', True)

        st.success(f"**{uploaded.name}** loaded successfully.")

        st.markdown(f'### {icon("preview")} Quick Preview', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Rows", f"{len(df):,}")
        c2.metric("Columns", f"{len(df.columns)}")
        c3.metric("Data Points", f"{df.size:,}")

        st.markdown("#### First 10 Rows")
        st.dataframe(df.head(10), width="stretch", height=350)

        st.markdown("#### Detected Columns")
        st.code(", ".join(df.columns.tolist()))

        st.info("File uploaded. Navigate to **Mapping** to confirm column assignments.")

    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    if get('upload_complete'):
        st.success(f"Previously uploaded: **{get('file_name')}**")
        st.info("Navigate to **Mapping** to continue.")
