"""
insights.py – Auto-generated data insights engine.
Finds interesting patterns, anomalies, and correlations in the dataset
and returns them as digestible, teacher-friendly insight strings.
"""
import pandas as pd
import numpy as np


def generate_insights(df, mapping, subjects):
    """
    Analyse the processed DataFrame and return a list of insight dicts.
    Each dict: {icon, title, detail, severity}
    severity: 'critical' | 'warning' | 'info' | 'positive'
    """
    insights = []
    total = len(df)
    if total == 0:
        return insights

    # ── Risk distribution insights ──
    high = len(df[df['final_risk'] == 'High Risk'])
    medium = len(df[df['final_risk'] == 'Medium Risk'])
    high_pct = high / total * 100

    if high_pct > 30:
        insights.append({
            'icon': '🚨', 'severity': 'critical',
            'title': 'Alarming Risk Level',
            'detail': f'{high_pct:.0f}% of students ({high}) are at High Risk. '
                      f'This is significantly above normal thresholds and requires school-wide intervention.',
        })
    elif high_pct > 15:
        insights.append({
            'icon': '⚠️', 'severity': 'warning',
            'title': 'Elevated Risk Cohort',
            'detail': f'{high} students ({high_pct:.0f}%) are at High Risk. '
                      f'Consider targeted class-level interventions.',
        })
    else:
        insights.append({
            'icon': '✅', 'severity': 'positive',
            'title': 'Healthy Risk Distribution',
            'detail': f'Only {high_pct:.0f}% of students are at High Risk — '
                      f'the cohort is generally performing well.',
        })

    # ── Class-level hotspot ──
    class_col = mapping.get('class')
    if class_col and class_col in df.columns:
        class_risk = df[df['final_risk'] == 'High Risk'].groupby(class_col).size()
        class_total = df.groupby(class_col).size()
        class_risk_pct = (class_risk / class_total * 100).dropna().sort_values(ascending=False)

        if len(class_risk_pct) > 0:
            worst_class = class_risk_pct.index[0]
            worst_pct = class_risk_pct.iloc[0]
            if worst_pct > 40:
                insights.append({
                    'icon': '🏫', 'severity': 'critical',
                    'title': f'Class {worst_class} is a Hotspot',
                    'detail': f'{worst_pct:.0f}% of students in Class {worst_class} '
                              f'are at High Risk — investigate class-specific factors.',
                })
            elif worst_pct > 20:
                insights.append({
                    'icon': '🏫', 'severity': 'warning',
                    'title': f'Class {worst_class} Needs Attention',
                    'detail': f'{worst_pct:.0f}% high-risk students in Class {worst_class}.',
                })

    # ── Subject-level insights ──
    subject_avgs = {}
    for sub in subjects:
        pct_col = f"{sub}_pct"
        if pct_col in df.columns:
            subject_avgs[sub] = df[pct_col].mean()

    if subject_avgs:
        weakest = min(subject_avgs, key=subject_avgs.get)
        strongest = max(subject_avgs, key=subject_avgs.get)
        insights.append({
            'icon': '📉', 'severity': 'warning',
            'title': f'{weakest} Needs Curriculum Review',
            'detail': f'{weakest} has the lowest class average at {subject_avgs[weakest]:.1f}%. '
                      f'Consider reviewing teaching methods or allocating more instructional time.',
        })
        insights.append({
            'icon': '🏆', 'severity': 'positive',
            'title': f'{strongest} is the Strongest Subject',
            'detail': f'{strongest} leads with a {subject_avgs[strongest]:.1f}% average. '
                      f'Replicate successful teaching strategies to other subjects.',
        })

        # Subject with highest failure rate
        for sub in subjects:
            pct_col = f"{sub}_pct"
            if pct_col in df.columns:
                fail_rate = (df[pct_col] < 40).mean() * 100
                if fail_rate > 30:
                    insights.append({
                        'icon': '🔴', 'severity': 'critical',
                        'title': f'{sub}: {fail_rate:.0f}% Failure Rate',
                        'detail': f'{fail_rate:.0f}% of students scored below 40% in {sub}. '
                                  f'This indicates a systemic issue requiring attention.',
                    })

    # ── Attendance correlation ──
    att_col = mapping.get('attendance')
    if att_col and att_col in df.columns:
        low_att = df[df[att_col] < 60]
        if len(low_att) > 0:
            low_att_risk_pct = (low_att['final_risk'] == 'High Risk').mean() * 100
            insights.append({
                'icon': '📊', 'severity': 'info',
                'title': 'Attendance-Risk Correlation',
                'detail': f'{low_att_risk_pct:.0f}% of students with attendance below 60% '
                          f'are at High Risk — reinforcing the attendance-performance link.',
            })

        avg_att = df[att_col].mean()
        if avg_att < 70:
            insights.append({
                'icon': '📋', 'severity': 'warning',
                'title': 'Low Overall Attendance',
                'detail': f'Average attendance is {avg_att:.1f}%. '
                          f'School-wide attendance drives may be needed.',
            })

    # ── Gender gap (if detectable) ──
    # ── Performance spread ──
    if 'avg_percentage' in df.columns:
        spread = df['avg_percentage'].std()
        if spread > 25:
            insights.append({
                'icon': '📈', 'severity': 'info',
                'title': 'High Performance Disparity',
                'detail': f'Standard deviation of {spread:.1f}% indicates a wide '
                          f'performance gap. Consider differentiated instruction strategies.',
            })

    return insights
