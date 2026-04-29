"""
5_Dashboard.py – Premium analytics dashboard with interactive Plotly charts,
auto-generated insights, critical alerts, and top/bottom performers.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.style import inject_custom_css, sidebar_branding, require_auth, icon
from core.session import get, is_ready
from core.insights import generate_insights
from core.alerts import generate_alerts
from visuals.charts import (
    subject_avg_bar_chart, risk_distribution_pie, risk_distribution_sunburst,
    attendance_vs_marks_scatter, class_comparison_chart,
    subject_heatmap, risk_funnel_chart, performance_distribution,
    subject_treemap,
)

inject_custom_css()
sidebar_branding()
require_auth()

st.markdown(f'<h1>{icon("dashboard")} Analytics Dashboard</h1>', unsafe_allow_html=True)
st.caption("Comprehensive overview of student performance, risk distribution, and actionable insights.")
st.markdown("---")

if not is_ready('processing_complete'):
    st.warning("Please complete the analysis pipeline on the **Validation** page first.")
    st.stop()

df = get('processed_df')
mapping = get('mapping')
subjects = get('subjects')

if df is None:
    st.error("Processed data not found. Please re-run the pipeline.")
    st.stop()

# ═══════════════════════════════════════════
# CRITICAL ALERTS BANNER
# ═══════════════════════════════════════════
alerts = generate_alerts(df, mapping, subjects)
if alerts:
    critical = [a for a in alerts if a['severity'] == 'critical']
    warnings = [a for a in alerts if a['severity'] == 'warning']

    if critical:
        with st.expander(f"🚨 **{len(critical)} Critical Alert(s) — Click to review**", expanded=True):
            for alert in critical:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg, #fef2f2, #fee2e2);
                            padding:14px 18px; border-radius:10px;
                            border-left:4px solid #ef4444; margin-bottom:10px;">
                    <span style="font-size:1.1rem;">{alert['icon']}</span>
                    <strong style="color:#991b1b;">{alert['title']}</strong>
                    <p style="color:#7f1d1d; margin:4px 0 0 0; font-size:0.88rem;">{alert['detail']}</p>
                </div>
                """, unsafe_allow_html=True)

    if warnings:
        with st.expander(f"⚠️ {len(warnings)} Warning(s)"):
            for alert in warnings:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg, #fffbeb, #fef3c7);
                            padding:12px 16px; border-radius:10px;
                            border-left:4px solid #f59e0b; margin-bottom:8px;">
                    <span>{alert['icon']}</span>
                    <strong style="color:#92400e;">{alert['title']}</strong>
                    <p style="color:#78350f; margin:4px 0 0 0; font-size:0.85rem;">{alert['detail']}</p>
                </div>
                """, unsafe_allow_html=True)

st.markdown("")

# ═══════════════════════════════════════════
# TOP KPI METRICS
# ═══════════════════════════════════════════
st.markdown(f'### {icon("trending_up")} Key Performance Indicators', unsafe_allow_html=True)
m1, m2, m3, m4, m5 = st.columns(5)

total = len(df)
high_risk = len(df[df['final_risk'] == 'High Risk'])
medium_risk = len(df[df['final_risk'] == 'Medium Risk'])
avg_score = df['avg_percentage'].mean()

m1.metric("Total Students", f"{total:,}")
m2.metric("High Risk", f"{high_risk}", delta=f"{high_risk/total*100:.1f}%" if total > 0 else "0%",
          delta_color="inverse")
m3.metric("Medium Risk", f"{medium_risk}", delta=f"{medium_risk/total*100:.1f}%" if total > 0 else "0%",
          delta_color="inverse")
m4.metric("Avg Score", f"{avg_score:.1f}%")

# Weakest subject
weakest_sub, lowest_avg = None, 100
for sub in subjects:
    pct_col = f"{sub}_pct"
    if pct_col in df.columns:
        avg = df[pct_col].mean()
        if avg < lowest_avg:
            lowest_avg = avg
            weakest_sub = sub
m5.metric("Weakest Subject", weakest_sub or "N/A",
          delta=f"{lowest_avg:.1f}%" if weakest_sub else None, delta_color="inverse")

st.markdown("---")

# ═══════════════════════════════════════════
# VISUAL ANALYTICS – TAB LAYOUT
# ═══════════════════════════════════════════
st.markdown(f'### {icon("insert_chart")} Visual Analytics', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Subject Performance", "🎯 Risk Distribution", "💬 Attendance Impact",
    "🏫 Class Comparison", "🔥 Heatmap", "📈 Distribution"
])

with tab1:
    col_bar, col_tree = st.columns([3, 2])
    with col_bar:
        fig = subject_avg_bar_chart(df, subjects)
        st.plotly_chart(fig, use_container_width=True)
    with col_tree:
        fig = subject_treemap(df, subjects)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    col_pie, col_funnel = st.columns(2)
    with col_pie:
        fig = risk_distribution_sunburst(df, mapping)
        st.plotly_chart(fig, use_container_width=True)
    with col_funnel:
        fig = risk_funnel_chart(df)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    fig = attendance_vs_marks_scatter(df, mapping)
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    fig = class_comparison_chart(df, mapping, subjects)
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    fig = subject_heatmap(df, mapping, subjects)
    st.plotly_chart(fig, use_container_width=True)

with tab6:
    fig = performance_distribution(df)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════
# TOP & BOTTOM PERFORMERS
# ═══════════════════════════════════════════
st.markdown(f'### {icon("emoji_events")} Top & Bottom Performers', unsafe_allow_html=True)

name_col = mapping.get('name', 'name')
class_col = mapping.get('class')

col_top, col_bottom = st.columns(2)

with col_top:
    st.markdown("""
    <div style="background:linear-gradient(135deg, #ecfdf5, #d1fae5);
                padding:14px 18px; border-radius:12px; margin-bottom:12px;
                border-left:4px solid #10b981;">
        <h4 style="margin:0; color:#065f46; font-size:1rem;">🏆 Top 5 Performers</h4>
    </div>
    """, unsafe_allow_html=True)
    top5 = df.nlargest(5, 'avg_percentage')
    for rank, (_, row) in enumerate(top5.iterrows(), 1):
        medal = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣'][rank - 1]
        name = row.get(name_col, 'Unknown')
        avg = row.get('avg_percentage', 0)
        cls = f" | {row.get(class_col, '')}" if class_col and class_col in row.index else ""
        st.markdown(f"""
        <div style="background:#fff; padding:10px 14px; border-radius:8px;
                    border:1px solid #d1fae5; margin-bottom:6px;
                    display:flex; align-items:center; gap:10px;">
            <span style="font-size:1.3rem;">{medal}</span>
            <div>
                <strong style="color:#0f172a;">{name}</strong>
                <span style="color:#64748b; font-size:0.82rem;">{cls}</span>
                <span style="float:right; font-weight:700; color:#059669;">{avg:.1f}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_bottom:
    st.markdown("""
    <div style="background:linear-gradient(135deg, #fef2f2, #fecaca);
                padding:14px 18px; border-radius:12px; margin-bottom:12px;
                border-left:4px solid #ef4444;">
        <h4 style="margin:0; color:#991b1b; font-size:1rem;">⚠️ Bottom 5 (Need Attention)</h4>
    </div>
    """, unsafe_allow_html=True)
    bottom5 = df.nsmallest(5, 'avg_percentage')
    for rank, (_, row) in enumerate(bottom5.iterrows(), 1):
        name = row.get(name_col, 'Unknown')
        avg = row.get('avg_percentage', 0)
        cls = f" | {row.get(class_col, '')}" if class_col and class_col in row.index else ""
        risk = row.get('final_risk', 'Unknown')
        risk_color = '#ef4444' if risk == 'High Risk' else '#f59e0b' if risk == 'Medium Risk' else '#10b981'
        st.markdown(f"""
        <div style="background:#fff; padding:10px 14px; border-radius:8px;
                    border:1px solid #fecaca; margin-bottom:6px;">
            <strong style="color:#0f172a;">{name}</strong>
            <span style="color:#64748b; font-size:0.82rem;">{cls}</span>
            <div style="display:flex; justify-content:space-between; margin-top:3px;">
                <span style="font-weight:700; color:#ef4444;">{avg:.1f}%</span>
                <span style="background:{risk_color}; color:white; padding:2px 8px;
                             border-radius:12px; font-size:0.72rem; font-weight:600;">{risk}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════
# AI-GENERATED INSIGHTS
# ═══════════════════════════════════════════
st.markdown(f'### {icon("psychology")} AI-Generated Insights', unsafe_allow_html=True)

insights = generate_insights(df, mapping, subjects)

severity_styles = {
    'critical': ('linear-gradient(135deg, #fef2f2, #fee2e2)', '#ef4444', '#7f1d1d'),
    'warning': ('linear-gradient(135deg, #fffbeb, #fef3c7)', '#f59e0b', '#78350f'),
    'info': ('linear-gradient(135deg, #eff6ff, #dbeafe)', '#3b82f6', '#1e3a5f'),
    'positive': ('linear-gradient(135deg, #ecfdf5, #d1fae5)', '#10b981', '#065f46'),
}

cols = st.columns(2)
for i, insight in enumerate(insights):
    bg, border, text_color = severity_styles.get(insight['severity'],
                                                  severity_styles['info'])
    with cols[i % 2]:
        st.markdown(f"""
        <div style="background:{bg}; padding:16px 18px; border-radius:12px;
                    border-left:4px solid {border}; margin-bottom:12px;">
            <div style="display:flex; align-items:center; gap:6px;">
                <span style="font-size:1.2rem;">{insight['icon']}</span>
                <strong style="color:{text_color}; font-size:0.95rem;">{insight['title']}</strong>
            </div>
            <p style="color:{text_color}; margin:6px 0 0 0; font-size:0.84rem;
                      opacity:0.85;">{insight['detail']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════
# STUDENT RISK TABLE
# ═══════════════════════════════════════════
st.markdown(f'### {icon("table_view")} Student Risk Overview', unsafe_allow_html=True)

fcol1, fcol2, fcol3 = st.columns(3)
with fcol1:
    risk_filter = st.multiselect("Filter by Risk Level",
        ['High Risk', 'Medium Risk', 'Low Risk'],
        default=['High Risk', 'Medium Risk', 'Low Risk'])
with fcol2:
    if class_col and class_col in df.columns:
        classes = ['All'] + sorted(df[class_col].astype(str).unique().tolist())
        selected_class = st.selectbox("Filter by Class", classes)
    else:
        selected_class = 'All'
with fcol3:
    sort_by = st.selectbox("Sort by", ['risk_score', 'avg_percentage', 'final_risk'], index=0)

filtered = df[df['final_risk'].isin(risk_filter)]
if selected_class != 'All' and class_col and class_col in filtered.columns:
    filtered = filtered[filtered[class_col].astype(str) == selected_class]

ascending = sort_by == 'avg_percentage'
filtered = filtered.sort_values(sort_by, ascending=ascending)

display_cols = [c for c in [name_col, class_col, 'avg_percentage', 'risk_score', 'final_risk', 'risk_reasons']
                if c and c in filtered.columns]

if display_cols:
    st.dataframe(
        filtered[display_cols].reset_index(drop=True),
        use_container_width=True, height=450,
        column_config={
            'avg_percentage': st.column_config.ProgressColumn("Avg %", min_value=0, max_value=100, format="%.1f%%"),
            'risk_score': st.column_config.ProgressColumn("Risk Score", min_value=0, max_value=100, format="%.1f"),
        },
    )
    st.caption(f"Showing {len(filtered)} of {len(df)} students")
else:
    st.info("No displayable columns found.")
