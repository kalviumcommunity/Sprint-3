"""
9_Compare.py – Batch comparison page.
Upload a second dataset and compare student performance over time.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.style import inject_custom_css, sidebar_branding, require_auth, icon
from core.session import get, is_ready
from core.loader import load_data
from core.mapper import detect_columns
from core.cleaner import clean_data
from core.normalizer import normalize_marks
from core.features import engineer_features
from core.predictor import predict
from visuals.charts import comparison_bar_chart, comparison_delta_chart

inject_custom_css()
sidebar_branding()
require_auth()

st.markdown(f'<h1>{icon("compare_arrows")} Batch Comparison</h1>', unsafe_allow_html=True)
st.caption("Compare two datasets to track student performance improvement or decline over time.")
st.markdown("---")

if not is_ready('processing_complete'):
    st.warning("Please complete the initial analysis pipeline on the **Validation** page first.")
    st.stop()

before_df = get('processed_df')
mapping = get('mapping')
subjects = get('subjects')

if before_df is None or mapping is None or subjects is None:
    st.error("Initial data not found. Please restart from Upload.")
    st.stop()

st.markdown(f"""
<div style="background:linear-gradient(135deg, #eff6ff, #dbeafe);
            padding:18px 22px; border-radius:12px; border-left:4px solid #3b82f6;
            margin-bottom:20px;">
    <strong style="color:#1e3a5f; font-size:0.95rem;">
        {icon("info")} How it works</strong>
    <p style="color:#1e3a5f; font-size:0.85rem; margin:6px 0 0 0; opacity:0.85;">
        Upload a <b>second dataset</b> (e.g., next term's data) with the same format.
        The system will automatically process it using the same pipeline and show you
        how students have improved or declined.</p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# CURRENT DATASET SUMMARY
# ═══════════════════════════════════════════
st.markdown(f'### {icon("history")} Current Dataset (Before)', unsafe_allow_html=True)

b1, b2, b3, b4 = st.columns(4)
b1.metric("Students", f"{len(before_df):,}")
b2.metric("Avg Score", f"{before_df['avg_percentage'].mean():.1f}%")
high_before = len(before_df[before_df['final_risk'] == 'High Risk'])
b3.metric("High Risk", high_before)
b4.metric("File", get('file_name', 'Original'))

st.markdown("---")

# ═══════════════════════════════════════════
# UPLOAD SECOND DATASET
# ═══════════════════════════════════════════
st.markdown(f'### {icon("cloud_upload")} Upload Comparison Dataset (After)', unsafe_allow_html=True)

# Offer sample Term 2 file for testing
sample_term2 = os.path.join(os.path.dirname(__file__), '..', 'data', 'samples', 'sample_data_term2.csv')
if os.path.exists(sample_term2):
    with open(sample_term2, 'rb') as f:
        st.download_button(
            "📥 Download Sample Term 2 CSV (for testing)",
            data=f.read(),
            file_name="sample_data_term2.csv",
            mime="text/csv",
        )

uploaded = st.file_uploader("Upload second dataset", type=['csv', 'xlsx', 'xls'],
                             key="compare_upload")

if uploaded is not None:
    try:
        with st.spinner("Processing comparison dataset..."):
            # Load and process
            after_raw = load_data(uploaded)

            # Use same mapping
            after_cleaned = clean_data(after_raw, mapping, subjects)
            after_norm = normalize_marks(after_cleaned, subjects)
            after_featured = engineer_features(after_norm, mapping, subjects)
            after_df = predict(after_featured, mapping)

        st.success(f"**{uploaded.name}** processed successfully!")

        # ═══════════════════════════════════════════
        # COMPARISON METRICS
        # ═══════════════════════════════════════════
        st.markdown("---")
        st.markdown(f'### {icon("compare")} Comparison Results', unsafe_allow_html=True)

        avg_before = before_df['avg_percentage'].mean()
        avg_after = after_df['avg_percentage'].mean()
        avg_delta = avg_after - avg_before

        high_after = len(after_df[after_df['final_risk'] == 'High Risk'])
        high_delta = high_after - high_before

        med_before = len(before_df[before_df['final_risk'] == 'Medium Risk'])
        med_after = len(after_df[after_df['final_risk'] == 'Medium Risk'])

        c1, c2, c3, c4 = st.columns(4)

        # Avg score change
        delta_color = "#10b981" if avg_delta >= 0 else "#ef4444"
        delta_icon = "trending_up" if avg_delta >= 0 else "trending_down"
        c1.markdown(f"""
        <div class="card" style="text-align:center; border-top:3px solid {delta_color};">
            <span class="mat-icon" style="font-size:24px; color:{delta_color};">{delta_icon}</span>
            <p style="color:#64748b; font-size:0.75rem; text-transform:uppercase; margin:6px 0 2px 0;">Avg Score Change</p>
            <p style="font-size:1.6rem; font-weight:800; color:{delta_color}; margin:0;">
                {'+' if avg_delta >= 0 else ''}{avg_delta:.1f}%</p>
            <p style="color:#94a3b8; font-size:0.75rem; margin:2px 0 0 0;">
                {avg_before:.1f}% → {avg_after:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

        # High risk change
        hr_color = "#10b981" if high_delta <= 0 else "#ef4444"
        c2.markdown(f"""
        <div class="card" style="text-align:center; border-top:3px solid {hr_color};">
            <span class="mat-icon" style="font-size:24px; color:{hr_color};">
                {'trending_down' if high_delta <= 0 else 'trending_up'}</span>
            <p style="color:#64748b; font-size:0.75rem; text-transform:uppercase; margin:6px 0 2px 0;">High Risk Change</p>
            <p style="font-size:1.6rem; font-weight:800; color:{hr_color}; margin:0;">
                {'+' if high_delta > 0 else ''}{high_delta}</p>
            <p style="color:#94a3b8; font-size:0.75rem; margin:2px 0 0 0;">
                {high_before} → {high_after}</p>
        </div>
        """, unsafe_allow_html=True)

        c3.metric("Before Students", f"{len(before_df):,}")
        c4.metric("After Students", f"{len(after_df):,}")

        st.markdown("---")

        # ═══════════════════════════════════════════
        # COMPARISON CHARTS
        # ═══════════════════════════════════════════
        st.markdown(f'### {icon("insert_chart")} Visual Comparison', unsafe_allow_html=True)

        tab_bar, tab_delta = st.tabs(["📊 Side by Side", "📈 Change Analysis"])

        with tab_bar:
            fig = comparison_bar_chart(before_df, after_df, subjects,
                                       label_before=get('file_name', 'Before'),
                                       label_after=uploaded.name)
            st.plotly_chart(fig, use_container_width=True)

        with tab_delta:
            deltas = {}
            for sub in subjects:
                pct_col = f"{sub}_pct"
                if pct_col in before_df.columns and pct_col in after_df.columns:
                    deltas[sub] = after_df[pct_col].mean() - before_df[pct_col].mean()
            if deltas:
                fig = comparison_delta_chart(deltas)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No comparable subjects found.")

        st.markdown("---")

        # ═══════════════════════════════════════════
        # STUDENT-LEVEL CHANGES
        # ═══════════════════════════════════════════
        st.markdown(f'### {icon("people")} Student-Level Analysis', unsafe_allow_html=True)

        # Match students by ID
        id_col = mapping.get('student_id')
        name_col = mapping.get('name', 'name')

        if id_col and id_col in before_df.columns and id_col in after_df.columns:
            merged = before_df[[id_col, name_col, 'avg_percentage', 'final_risk']].merge(
                after_df[[id_col, 'avg_percentage', 'final_risk']],
                on=id_col, suffixes=('_before', '_after'),
                how='inner'
            )
            merged['delta'] = merged['avg_percentage_after'] - merged['avg_percentage_before']
            merged['status'] = merged['delta'].apply(
                lambda d: '📈 Improved' if d > 2 else '📉 Declined' if d < -2 else '➡️ Stable'
            )

            improved = (merged['delta'] > 2).sum()
            declined = (merged['delta'] < -2).sum()
            stable = len(merged) - improved - declined

            summary_cols = st.columns(3)
            summary_cols[0].markdown(f"""
            <div class="card" style="text-align:center; border-top:3px solid #10b981;">
                <p style="font-size:2rem; font-weight:800; color:#10b981; margin:0;">{improved}</p>
                <p style="color:#64748b; font-size:0.82rem;">📈 Improved</p>
            </div>
            """, unsafe_allow_html=True)
            summary_cols[1].markdown(f"""
            <div class="card" style="text-align:center; border-top:3px solid #f59e0b;">
                <p style="font-size:2rem; font-weight:800; color:#f59e0b; margin:0;">{stable}</p>
                <p style="color:#64748b; font-size:0.82rem;">➡️ Stable</p>
            </div>
            """, unsafe_allow_html=True)
            summary_cols[2].markdown(f"""
            <div class="card" style="text-align:center; border-top:3px solid #ef4444;">
                <p style="font-size:2rem; font-weight:800; color:#ef4444; margin:0;">{declined}</p>
                <p style="color:#64748b; font-size:0.82rem;">📉 Declined</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            display = merged[[name_col, 'avg_percentage_before', 'avg_percentage_after', 'delta',
                             'final_risk_before', 'final_risk_after', 'status']].sort_values('delta')
            display.columns = ['Name', 'Before %', 'After %', 'Change', 'Risk Before', 'Risk After', 'Status']

            st.dataframe(display.reset_index(drop=True), use_container_width=True, height=400,
                        column_config={
                            'Before %': st.column_config.NumberColumn(format="%.1f%%"),
                            'After %': st.column_config.NumberColumn(format="%.1f%%"),
                            'Change': st.column_config.NumberColumn(format="%+.1f%%"),
                        })
        else:
            st.info("Student ID matching not available. Showing aggregate comparison only.")

    except Exception as e:
        st.error(f"Error processing comparison file: {e}")
else:
    st.markdown(f"""
    <div class="card" style="text-align:center; padding:40px; border:2px dashed #cbd5e1;">
        <span class="mat-icon" style="font-size:48px; color:#cbd5e1;">cloud_upload</span>
        <h4 style="color:#94a3b8; margin:12px 0 4px 0;">Upload a comparison dataset</h4>
        <p style="color:#cbd5e1; font-size:0.85rem;">
            Upload a second CSV/XLSX with the same format to see how performance has changed.</p>
    </div>
    """, unsafe_allow_html=True)
