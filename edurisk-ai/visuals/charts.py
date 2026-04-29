"""
charts.py – Premium Plotly chart generators.
All functions return Plotly Figure objects for use with st.plotly_chart().
Includes unique chart types: gauges, sunbursts, treemaps, funnels, heatmaps.
Compatible with Plotly 6.x.
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

# ── Premium color palette ──
COLORS = {
    'primary': '#4f46e5',
    'primary_light': '#818cf8',
    'secondary': '#7c3aed',
    'accent': '#0891b2',
    'danger': '#ef4444',
    'warning': '#f59e0b',
    'success': '#10b981',
    'bg': '#ffffff',
    'card': '#f8fafc',
    'text': '#0f172a',
    'muted': '#94a3b8',
    'border': '#e2e8f0',
}

RISK_COLORS = {
    'High Risk': '#ef4444',
    'Medium Risk': '#f59e0b',
    'Low Risk': '#10b981',
}

SUBJECT_PALETTE = [
    '#4f46e5', '#7c3aed', '#0891b2', '#059669', '#d97706',
    '#ef4444', '#6366f1', '#8b5cf6', '#06b6d4', '#14b8a6',
]

LAYOUT_DEFAULTS = dict(
    font=dict(family='Inter, system-ui, sans-serif', color=COLORS['text']),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=40, r=40, t=60, b=40),
    hoverlabel=dict(
        bgcolor='white',
        font=dict(size=12, family='Inter, sans-serif'),
        bordercolor=COLORS['border'],
    ),
)


def _apply_layout(fig, **kwargs):
    """Apply consistent layout defaults."""
    fig.update_layout(**LAYOUT_DEFAULTS, **kwargs)
    return fig


# ═══════════════════════════════════════════════════════
# 1. SUBJECT AVERAGE BAR CHART
# ═══════════════════════════════════════════════════════
def subject_avg_bar_chart(df, subjects):
    """Stylish horizontal bar chart with color coding."""
    avgs, labels = [], []
    for sub in subjects:
        pct_col = f"{sub}_pct"
        if pct_col in df.columns:
            avgs.append(round(df[pct_col].mean(), 1))
            labels.append(sub)

    if not labels:
        return go.Figure().add_annotation(text="No subject data", showarrow=False)

    bar_colors = []
    for a in avgs:
        if a >= 70:
            bar_colors.append(COLORS['success'])
        elif a >= 50:
            bar_colors.append(COLORS['primary'])
        elif a >= 40:
            bar_colors.append(COLORS['warning'])
        else:
            bar_colors.append(COLORS['danger'])

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=labels, x=avgs,
        orientation='h',
        marker=dict(color=bar_colors, line=dict(width=0)),
        text=[f'{a}%' for a in avgs],
        textposition='outside',
        textfont=dict(size=13, color=COLORS['text'], family='Inter'),
        hovertemplate='<b>%{y}</b><br>Average: %{x:.1f}%<extra></extra>',
    ))

    fig.add_vline(x=40, line_dash="dot", line_color=COLORS['danger'],
                  annotation_text="Pass: 40%", annotation_position="top")

    _apply_layout(fig,
        title=dict(text='Subject-wise Average Performance', font=dict(size=16, color=COLORS['text'])),
        xaxis=dict(title='Average Score (%)', range=[0, max(avgs) + 15],
                   gridcolor=COLORS['border'], gridwidth=0.5, zeroline=False),
        yaxis=dict(autorange='reversed'),
        height=max(350, len(labels) * 55),
        barcornerradius=6,
    )
    return fig


# ═══════════════════════════════════════════════════════
# 2. RISK DISTRIBUTION – SUNBURST CHART
# ═══════════════════════════════════════════════════════
def risk_distribution_sunburst(df, mapping):
    """Sunburst chart: center=total, ring1=risk levels, ring2=classes."""
    class_col = mapping.get('class')

    if class_col and class_col in df.columns:
        labels, parents, values, colors = ['All Students'], [''], [len(df)], [COLORS['primary']]

        for risk in ['High Risk', 'Medium Risk', 'Low Risk']:
            risk_df = df[df['final_risk'] == risk]
            if len(risk_df) > 0:
                labels.append(risk)
                parents.append('All Students')
                values.append(len(risk_df))
                colors.append(RISK_COLORS[risk])

                for cls in sorted(df[class_col].astype(str).unique()):
                    count = len(risk_df[risk_df[class_col].astype(str) == cls])
                    if count > 0:
                        labels.append(f'{cls} ({risk[:1]})')
                        parents.append(risk)
                        values.append(count)
                        colors.append(RISK_COLORS[risk])

        fig = go.Figure(go.Sunburst(
            labels=labels, parents=parents, values=values,
            branchvalues='total',
            marker=dict(colors=colors, line=dict(width=2, color='white')),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percentRoot:.1%} of total<extra></extra>',
            textfont=dict(size=12),
        ))
    else:
        counts = df['final_risk'].value_counts()
        fig = go.Figure(go.Pie(
            labels=counts.index, values=counts.values,
            hole=0.55,
            marker=dict(colors=[RISK_COLORS.get(l, COLORS['muted']) for l in counts.index],
                        line=dict(width=2.5, color='white')),
            textfont=dict(size=13),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>',
        ))
        fig.add_annotation(text=f"<b>{len(df)}</b><br>Students",
                          font=dict(size=16, color=COLORS['text']),
                          showarrow=False)

    _apply_layout(fig,
        title=dict(text='Risk Distribution Breakdown', font=dict(size=16)),
        height=480,
    )
    return fig


# ═══════════════════════════════════════════════════════
# 3. RISK DONUT
# ═══════════════════════════════════════════════════════
def risk_distribution_pie(df):
    """Premium donut chart with center annotation."""
    counts = df['final_risk'].value_counts()
    fig = go.Figure(go.Pie(
        labels=counts.index, values=counts.values,
        hole=0.6,
        marker=dict(
            colors=[RISK_COLORS.get(l, COLORS['muted']) for l in counts.index],
            line=dict(width=3, color='white'),
        ),
        textinfo='label+percent',
        textfont=dict(size=12),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>',
        pull=[0.03 if l == 'High Risk' else 0 for l in counts.index],
    ))
    fig.add_annotation(
        text=f"<b>{len(df)}</b><br><span style='font-size:11px;color:{COLORS['muted']}'>Total</span>",
        font=dict(size=22, color=COLORS['text']),
        showarrow=False,
    )
    _apply_layout(fig,
        title=dict(text='Risk Distribution', font=dict(size=16)),
        height=420, showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.1, xanchor='center', x=0.5),
    )
    return fig


# ═══════════════════════════════════════════════════════
# 4. ATTENDANCE VS MARKS – BUBBLE SCATTER
# ═══════════════════════════════════════════════════════
def attendance_vs_marks_scatter(df, mapping):
    """Bubble scatter with size=risk_score, color=risk level."""
    att_col = mapping.get('attendance')
    if not att_col or att_col not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text="Attendance data not available", showarrow=False,
                          font=dict(size=14, color=COLORS['muted']))
        return _apply_layout(fig, height=400)

    name_col = mapping.get('name', 'name')

    fig = go.Figure()
    for risk, color in RISK_COLORS.items():
        subset = df[df['final_risk'] == risk]
        if len(subset) == 0:
            continue
        fig.add_trace(go.Scatter(
            x=subset[att_col],
            y=subset['avg_percentage'],
            mode='markers',
            name=risk,
            marker=dict(
                color=color, size=subset['risk_score'].clip(6, 25),
                opacity=0.7, line=dict(width=1, color='white'),
            ),
            text=subset[name_col] if name_col in subset.columns else None,
            hovertemplate=(
                '<b>%{text}</b><br>'
                'Attendance: %{x:.1f}%<br>'
                'Avg Score: %{y:.1f}%<br>'
                '<extra>%{fullData.name}</extra>'
            ),
        ))

    fig.add_hline(y=40, line_dash="dot", line_color=COLORS['danger'], opacity=0.5)
    fig.add_vline(x=60, line_dash="dot", line_color=COLORS['danger'], opacity=0.5)

    fig.add_annotation(x=30, y=80, text="Low Att / High Score", showarrow=False,
                      font=dict(size=9, color=COLORS['muted']), opacity=0.6)
    fig.add_annotation(x=85, y=20, text="High Att / Low Score", showarrow=False,
                      font=dict(size=9, color=COLORS['muted']), opacity=0.6)
    fig.add_annotation(x=30, y=20, text="⚠ Danger Zone", showarrow=False,
                      font=dict(size=10, color=COLORS['danger']), opacity=0.7)

    _apply_layout(fig,
        title=dict(text='Attendance vs Performance', font=dict(size=16)),
        xaxis=dict(title='Attendance (%)', gridcolor=COLORS['border'], gridwidth=0.5,
                   range=[0, 105]),
        yaxis=dict(title='Average Score (%)', gridcolor=COLORS['border'], gridwidth=0.5,
                   range=[0, 105]),
        height=500,
        legend=dict(orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5),
    )
    return fig


# ═══════════════════════════════════════════════════════
# 5. CLASS COMPARISON – GROUPED BAR
# ═══════════════════════════════════════════════════════
def class_comparison_chart(df, mapping, subjects):
    """Grouped bar chart comparing subjects across classes."""
    class_col = mapping.get('class')
    if not class_col or class_col not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text="Class data not available", showarrow=False,
                          font=dict(size=14, color=COLORS['muted']))
        return _apply_layout(fig, height=400)

    pct_cols = [f"{s}_pct" for s in subjects if f"{s}_pct" in df.columns]
    class_means = df.groupby(class_col)[pct_cols].mean()

    fig = go.Figure()
    for i, col in enumerate(pct_cols):
        label = col.replace('_pct', '')
        fig.add_trace(go.Bar(
            name=label,
            x=[str(c) for c in class_means.index],
            y=class_means[col].round(1),
            marker=dict(color=SUBJECT_PALETTE[i % len(SUBJECT_PALETTE)]),
            text=class_means[col].round(1),
            textposition='outside',
            textfont=dict(size=9),
            hovertemplate=f'<b>{label}</b><br>Class: %{{x}}<br>Avg: %{{y:.1f}}%<extra></extra>',
        ))

    _apply_layout(fig,
        title=dict(text='Class-wise Performance Comparison', font=dict(size=16)),
        barmode='group', bargap=0.2, bargroupgap=0.05,
        xaxis=dict(title='Class', gridcolor=COLORS['border']),
        yaxis=dict(title='Average Score (%)', gridcolor=COLORS['border'], gridwidth=0.5),
        height=480,
        legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5),
        barcornerradius=4,
    )
    return fig


# ═══════════════════════════════════════════════════════
# 6. STUDENT RADAR CHART (Interactive)
# ═══════════════════════════════════════════════════════
def student_radar_chart(student_row, subjects, class_averages):
    """Interactive radar comparing student vs class averages."""
    labels, student_vals, avg_vals = [], [], []
    for sub in subjects:
        pct_col = f"{sub}_pct"
        if pct_col in student_row.index:
            labels.append(sub)
            student_vals.append(round(student_row[pct_col], 1))
            avg_vals.append(round(class_averages.get(sub, 50), 1))

    if not labels:
        fig = go.Figure()
        fig.add_annotation(text="Not enough data", showarrow=False,
                          font=dict(size=14, color=COLORS['muted']))
        return _apply_layout(fig, height=400)

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=student_vals + [student_vals[0]],
        theta=labels + [labels[0]],
        fill='toself',
        fillcolor='rgba(79, 70, 229, 0.15)',
        line=dict(color=COLORS['primary'], width=2.5),
        marker=dict(size=7, color=COLORS['primary']),
        name='Student',
        hovertemplate='%{theta}: %{r:.1f}%<extra>Student</extra>',
    ))
    fig.add_trace(go.Scatterpolar(
        r=avg_vals + [avg_vals[0]],
        theta=labels + [labels[0]],
        fill='toself',
        fillcolor='rgba(249, 158, 11, 0.08)',
        line=dict(color=COLORS['warning'], width=2, dash='dot'),
        marker=dict(size=5, color=COLORS['warning']),
        name='Class Average',
        hovertemplate='%{theta}: %{r:.1f}%<extra>Class Avg</extra>',
    ))

    _apply_layout(fig,
        title=dict(text='Subject Performance vs Class Average', font=dict(size=15)),
        polar=dict(
            radialaxis=dict(range=[0, 100], showticklabels=True, tickfont=dict(size=9),
                           gridcolor=COLORS['border']),
            angularaxis=dict(tickfont=dict(size=11, color=COLORS['text']),
                           gridcolor=COLORS['border']),
            bgcolor='rgba(248,250,252,0.5)',
        ),
        height=440,
        legend=dict(orientation='h', yanchor='bottom', y=-0.12, xanchor='center', x=0.5),
    )
    return fig


# ═══════════════════════════════════════════════════════
# 7. RISK GAUGE METER
# ═══════════════════════════════════════════════════════
def risk_gauge(risk_score, risk_level):
    """Semicircle gauge meter showing risk score 0-100."""
    color = RISK_COLORS.get(risk_level, COLORS['muted'])

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        number=dict(font=dict(size=36, color=color), suffix=''),
        title=dict(text=f'<b>{risk_level}</b>', font=dict(size=14, color=color)),
        gauge=dict(
            axis=dict(range=[0, 100], tickwidth=1, tickcolor=COLORS['border'],
                     tickfont=dict(size=10)),
            bar=dict(color=color, thickness=0.75),
            bgcolor='white',
            borderwidth=0,
            steps=[
                dict(range=[0, 35], color='rgba(16, 185, 129, 0.12)'),
                dict(range=[35, 60], color='rgba(245, 158, 11, 0.12)'),
                dict(range=[60, 100], color='rgba(239, 68, 68, 0.12)'),
            ],
            threshold=dict(
                line=dict(color=COLORS['text'], width=2),
                thickness=0.8, value=risk_score,
            ),
        ),
    ))

    _apply_layout(fig, height=280, margin=dict(l=30, r=30, t=50, b=10))
    return fig


# ═══════════════════════════════════════════════════════
# 8. SUBJECT HEATMAP (Class x Subject)
# ═══════════════════════════════════════════════════════
def subject_heatmap(df, mapping, subjects):
    """Heatmap showing average scores per class per subject."""
    class_col = mapping.get('class')
    if not class_col or class_col not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text="Class data not available", showarrow=False)
        return _apply_layout(fig, height=400)

    pct_cols = [f"{s}_pct" for s in subjects if f"{s}_pct" in df.columns]
    if not pct_cols:
        fig = go.Figure()
        fig.add_annotation(text="No subject data", showarrow=False)
        return _apply_layout(fig, height=400)

    class_means = df.groupby(class_col)[pct_cols].mean().round(1)
    class_means.columns = [c.replace('_pct', '') for c in class_means.columns]

    fig = go.Figure(go.Heatmap(
        z=class_means.values,
        x=class_means.columns.tolist(),
        y=[str(c) for c in class_means.index],
        colorscale=[
            [0, '#ef4444'],
            [0.4, '#fbbf24'],
            [0.6, '#a3e635'],
            [1, '#10b981'],
        ],
        text=class_means.values,
        texttemplate='%{text:.1f}%',
        textfont=dict(size=11, color='white'),
        hovertemplate='Class: %{y}<br>Subject: %{x}<br>Average: %{z:.1f}%<extra></extra>',
        colorbar=dict(title=dict(text='Avg %', font=dict(size=11))),
    ))

    _apply_layout(fig,
        title=dict(text='Class × Subject Performance Heatmap', font=dict(size=16)),
        xaxis=dict(title='Subject', side='bottom'),
        yaxis=dict(title='Class', autorange='reversed'),
        height=max(350, len(class_means) * 50 + 120),
    )
    return fig


# ═══════════════════════════════════════════════════════
# 9. RISK FUNNEL CHART
# ═══════════════════════════════════════════════════════
def risk_funnel_chart(df):
    """Funnel chart showing risk level distribution."""
    total = len(df)
    high = len(df[df['final_risk'] == 'High Risk'])
    medium = len(df[df['final_risk'] == 'Medium Risk'])

    fig = go.Figure(go.Funnel(
        y=['All Students', 'At Risk (H+M)', 'High Risk', 'Medium Risk'],
        x=[total, high + medium, high, medium],
        textinfo='value+percent initial',
        textfont=dict(size=13),
        marker=dict(
            color=[COLORS['primary'], COLORS['warning'], COLORS['danger'], '#fbbf24'],
            line=dict(width=2, color='white'),
        ),
        connector=dict(line=dict(color=COLORS['border'], width=1)),
        hovertemplate='<b>%{y}</b><br>Count: %{x}<br>%{percentInitial:.1%} of total<extra></extra>',
    ))

    _apply_layout(fig,
        title=dict(text='Risk Pipeline Funnel', font=dict(size=16)),
        height=380,
    )
    return fig


# ═══════════════════════════════════════════════════════
# 10. PERFORMANCE DISTRIBUTION HISTOGRAM
# ═══════════════════════════════════════════════════════
def performance_distribution(df):
    """Histogram of average percentage with risk coloring."""
    fig = go.Figure()

    for risk in ['Low Risk', 'Medium Risk', 'High Risk']:
        subset = df[df['final_risk'] == risk]
        if len(subset) > 0:
            fig.add_trace(go.Histogram(
                x=subset['avg_percentage'],
                name=risk,
                marker=dict(color=RISK_COLORS[risk], line=dict(width=1, color='white')),
                opacity=0.8,
                nbinsx=20,
                hovertemplate='Score range: %{x}<br>Count: %{y}<extra>%{fullData.name}</extra>',
            ))

    fig.add_vline(x=40, line_dash="dot", line_color=COLORS['danger'],
                  annotation_text="Pass: 40%")

    _apply_layout(fig,
        title=dict(text='Score Distribution by Risk Level', font=dict(size=16)),
        barmode='overlay',
        xaxis=dict(title='Average Score (%)', gridcolor=COLORS['border']),
        yaxis=dict(title='Number of Students', gridcolor=COLORS['border']),
        height=400,
        legend=dict(orientation='h', yanchor='bottom', y=-0.18, xanchor='center', x=0.5),
    )
    return fig


# ═══════════════════════════════════════════════════════
# 11. TREEMAP – Subject Performance Breakdown
# ═══════════════════════════════════════════════════════
def subject_treemap(df, subjects):
    """Treemap showing relative subject performance."""
    valid_subjects = [sub for sub in subjects if f"{sub}_pct" in df.columns]

    if not valid_subjects:
        fig = go.Figure()
        fig.add_annotation(text="No subject data", showarrow=False)
        return _apply_layout(fig, height=380)

    labels = ['All Subjects']
    parents = ['']
    values = [0]
    colors = [COLORS['primary']]
    custom_text = ['']

    for sub in valid_subjects:
        pct_col = f"{sub}_pct"
        avg = df[pct_col].mean()
        labels.append(sub)
        parents.append('All Subjects')
        values.append(len(df))
        custom_text.append(f'{avg:.0f}%')

        if avg >= 70:
            colors.append(COLORS['success'])
        elif avg >= 50:
            colors.append(COLORS['primary'])
        elif avg >= 40:
            colors.append(COLORS['warning'])
        else:
            colors.append(COLORS['danger'])

    fig = go.Figure(go.Treemap(
        labels=labels, parents=parents, values=values,
        marker=dict(colors=colors, line=dict(width=2, color='white')),
        textinfo='label+text',
        text=custom_text,
        textfont=dict(size=15, color='white'),
        hovertemplate='<b>%{label}</b><br>%{text}<extra></extra>',
    ))

    _apply_layout(fig,
        title=dict(text='Subject Performance Overview', font=dict(size=16)),
        height=380,
    )
    return fig


# ═══════════════════════════════════════════════════════
# 12. COMPARISON BAR (Before/After)
# ═══════════════════════════════════════════════════════
def comparison_bar_chart(before_df, after_df, subjects, label_before='Before', label_after='After'):
    """Side-by-side comparison of two datasets."""
    fig = go.Figure()

    before_avgs, after_avgs, sub_labels = [], [], []
    for sub in subjects:
        pct_col = f"{sub}_pct"
        if pct_col in before_df.columns and pct_col in after_df.columns:
            sub_labels.append(sub)
            before_avgs.append(round(before_df[pct_col].mean(), 1))
            after_avgs.append(round(after_df[pct_col].mean(), 1))

    fig.add_trace(go.Bar(
        name=label_before, x=sub_labels, y=before_avgs,
        marker=dict(color='rgba(79, 70, 229, 0.5)'),
        text=before_avgs, textposition='outside',
    ))
    fig.add_trace(go.Bar(
        name=label_after, x=sub_labels, y=after_avgs,
        marker=dict(color=COLORS['primary']),
        text=after_avgs, textposition='outside',
    ))

    _apply_layout(fig,
        title=dict(text='Subject Performance: Before vs After', font=dict(size=16)),
        barmode='group',
        xaxis=dict(title='Subject'), yaxis=dict(title='Average Score (%)',
                                                 gridcolor=COLORS['border']),
        height=420,
        legend=dict(orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5),
        barcornerradius=4,
    )
    return fig


def comparison_delta_chart(deltas):
    """Waterfall-style chart showing improvement/decline per subject."""
    subjects = list(deltas.keys())
    values = list(deltas.values())
    colors = [COLORS['success'] if v >= 0 else COLORS['danger'] for v in values]

    fig = go.Figure(go.Bar(
        x=subjects, y=values,
        marker=dict(color=colors, line=dict(width=1, color='white')),
        text=[f'+{v:.1f}%' if v >= 0 else f'{v:.1f}%' for v in values],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Change: %{y:+.1f}%<extra></extra>',
    ))

    fig.add_hline(y=0, line_color=COLORS['text'], line_width=1)

    _apply_layout(fig,
        title=dict(text='Performance Change by Subject', font=dict(size=16)),
        xaxis=dict(title='Subject'),
        yaxis=dict(title='Change (%)', gridcolor=COLORS['border'], zeroline=False),
        height=400,
        barcornerradius=4,
    )
    return fig
