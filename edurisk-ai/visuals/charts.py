"""
charts.py – Matplotlib chart generators (light theme).
All functions return a Matplotlib Figure object for use with st.pyplot().
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ── Light-mode palette ──
COLORS = {
    'primary': '#4f46e5',
    'secondary': '#7c3aed',
    'accent': '#0891b2',
    'danger': '#dc2626',
    'warning': '#d97706',
    'success': '#059669',
    'bg': '#ffffff',
    'card': '#f8fafc',
    'text': '#0f172a',
    'muted': '#94a3b8',
    'border': '#e2e8f0',
}

RISK_COLORS = {
    'High Risk': '#dc2626',
    'Medium Risk': '#d97706',
    'Low Risk': '#059669',
}

plt.rcParams.update({
    'figure.facecolor': COLORS['bg'],
    'axes.facecolor': COLORS['card'],
    'axes.edgecolor': COLORS['border'],
    'axes.labelcolor': COLORS['text'],
    'text.color': COLORS['text'],
    'xtick.color': COLORS['muted'],
    'ytick.color': COLORS['muted'],
    'font.family': 'sans-serif',
})


def subject_avg_bar_chart(df, subjects):
    """Bar chart of average percentage per subject."""
    avgs, labels = [], []
    for sub in subjects:
        pct_col = f"{sub}_pct"
        if pct_col in df.columns:
            avgs.append(df[pct_col].mean())
            labels.append(sub)

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(labels, avgs, color=[COLORS['primary'] if a >= 50 else COLORS['danger'] for a in avgs],
                  edgecolor='none', width=0.55, zorder=3)

    for bar, val in zip(bars, avgs):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f'{val:.1f}%', ha='center', va='bottom', fontsize=10, color=COLORS['text'], fontweight='500')

    ax.set_ylabel('Average Score (%)', fontsize=11, color=COLORS['text'])
    ax.set_title('Subject-wise Average Scores', fontsize=13, fontweight='600', pad=14, color=COLORS['text'])
    ax.set_ylim(0, 110)
    ax.grid(axis='y', alpha=0.3, color=COLORS['border'])
    ax.set_axisbelow(True)
    plt.xticks(rotation=25, ha='right')
    plt.tight_layout()
    return fig


def risk_distribution_pie(df):
    """Donut chart showing risk level distribution."""
    counts = df['final_risk'].value_counts()
    labels = counts.index.tolist()
    sizes = counts.values.tolist()
    colors = [RISK_COLORS.get(l, COLORS['muted']) for l in labels]

    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, autopct='%1.1f%%',
        startangle=140, pctdistance=0.75,
        wedgeprops=dict(width=0.42, edgecolor=COLORS['bg'], linewidth=2.5),
        textprops=dict(color=COLORS['text'], fontsize=11),
    )
    for t in autotexts:
        t.set_fontsize(10)
        t.set_fontweight('600')
        t.set_color(COLORS['text'])

    ax.set_title('Risk Distribution', fontsize=13, fontweight='600', pad=18, color=COLORS['text'])
    plt.tight_layout()
    return fig


def attendance_vs_marks_scatter(df, mapping):
    """Scatter plot: attendance vs average percentage, coloured by risk."""
    att_col = mapping.get('attendance')
    if not att_col or att_col not in df.columns:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.text(0.5, 0.5, 'Attendance data not available', transform=ax.transAxes,
                ha='center', va='center', fontsize=13, color=COLORS['muted'])
        return fig

    fig, ax = plt.subplots(figsize=(10, 6))

    for risk, color in RISK_COLORS.items():
        subset = df[df['final_risk'] == risk]
        ax.scatter(subset[att_col], subset['avg_percentage'],
                   c=color, label=risk, alpha=0.65, edgecolors='white', linewidths=0.5, s=55, zorder=3)

    ax.set_xlabel('Attendance (%)', fontsize=11)
    ax.set_ylabel('Average Score (%)', fontsize=11)
    ax.set_title('Attendance vs Performance', fontsize=13, fontweight='600', pad=14, color=COLORS['text'])
    ax.legend(framealpha=0.8, fontsize=10, edgecolor=COLORS['border'])
    ax.grid(alpha=0.25, color=COLORS['border'])
    ax.set_axisbelow(True)
    plt.tight_layout()
    return fig


def class_comparison_chart(df, mapping, subjects):
    """Grouped bar chart comparing average scores across classes."""
    class_col = mapping.get('class')
    if not class_col or class_col not in df.columns:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.text(0.5, 0.5, 'Class data not available', transform=ax.transAxes,
                ha='center', va='center', fontsize=13, color=COLORS['muted'])
        return fig

    pct_cols = [f"{s}_pct" for s in subjects if f"{s}_pct" in df.columns]
    if not pct_cols:
        pct_cols = subjects

    class_means = df.groupby(class_col)[pct_cols].mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(class_means.index))
    width = 0.8 / max(len(pct_cols), 1)
    palette = ['#4f46e5', '#7c3aed', '#0891b2', '#059669', '#d97706', '#dc2626', '#6366f1']

    for i, col in enumerate(pct_cols):
        offset = (i - len(pct_cols) / 2 + 0.5) * width
        label = col.replace('_pct', '')
        ax.bar(x + offset, class_means[col], width * 0.88,
               label=label, color=palette[i % len(palette)], zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels([str(c) for c in class_means.index], fontsize=10)
    ax.set_ylabel('Average Score (%)', fontsize=11)
    ax.set_title('Class-wise Performance Comparison', fontsize=13, fontweight='600', pad=14, color=COLORS['text'])
    ax.legend(fontsize=9, ncol=3, framealpha=0.8, edgecolor=COLORS['border'])
    ax.grid(axis='y', alpha=0.25, color=COLORS['border'])
    ax.set_axisbelow(True)
    plt.tight_layout()
    return fig


def student_radar_chart(student_row, subjects, class_averages):
    """Radar chart comparing a student's marks against class averages."""
    labels, student_vals, avg_vals = [], [], []
    for sub in subjects:
        pct_col = f"{sub}_pct"
        if pct_col in student_row.index:
            labels.append(sub)
            student_vals.append(student_row[pct_col])
            avg_vals.append(class_averages.get(sub, 50))

    if not labels:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, 'Not enough data', ha='center', va='center',
                transform=ax.transAxes, fontsize=13, color=COLORS['muted'])
        return fig

    N = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]
    student_vals += student_vals[:1]
    avg_vals += avg_vals[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    ax.set_facecolor('#fafbfc')
    fig.set_facecolor(COLORS['bg'])

    ax.plot(angles, student_vals, 'o-', color=COLORS['primary'], linewidth=2, label='Student', markersize=5)
    ax.fill(angles, student_vals, alpha=0.12, color=COLORS['primary'])
    ax.plot(angles, avg_vals, 'o--', color=COLORS['warning'], linewidth=2, label='Class Avg', markersize=4)
    ax.fill(angles, avg_vals, alpha=0.06, color=COLORS['warning'])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10, color=COLORS['text'])
    ax.set_ylim(0, 100)
    ax.set_title('Subject Performance vs Class Average', fontsize=12, fontweight='600',
                 pad=22, color=COLORS['text'])
    ax.legend(loc='lower right', fontsize=10, framealpha=0.9, edgecolor=COLORS['border'])
    ax.tick_params(colors=COLORS['muted'])
    ax.spines['polar'].set_color(COLORS['border'])
    ax.yaxis.grid(color=COLORS['border'], alpha=0.4)
    ax.xaxis.grid(color=COLORS['border'], alpha=0.4)
    plt.tight_layout()
    return fig
