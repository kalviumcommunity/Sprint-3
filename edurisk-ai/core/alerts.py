"""
alerts.py – Critical alert generator.
Scans processed data for urgent situations that need immediate teacher attention.
Returns prioritized, actionable alerts displayed as banners.
"""


def generate_alerts(df, mapping, subjects):
    """
    Returns a list of alert dicts sorted by severity.
    Each dict: {severity, icon, title, detail, count}
    severity: 'critical' | 'warning'
    """
    alerts = []
    total = len(df)
    if total == 0:
        return alerts

    att_col = mapping.get('attendance')
    class_col = mapping.get('class')

    # ── Critical attendance ──
    if att_col and att_col in df.columns:
        critical_att = df[df[att_col] < 40]
        if len(critical_att) > 0:
            alerts.append({
                'severity': 'critical',
                'icon': '🚨',
                'title': 'Critical Attendance Alert',
                'detail': f'{len(critical_att)} student(s) have attendance below 40%. '
                          f'Immediate follow-up required.',
                'count': len(critical_att),
            })

        low_att = df[(df[att_col] >= 40) & (df[att_col] < 60)]
        if len(low_att) > 0:
            alerts.append({
                'severity': 'warning',
                'icon': '⚠️',
                'title': 'Low Attendance Warning',
                'detail': f'{len(low_att)} student(s) have attendance between 40-60%.',
                'count': len(low_att),
            })

    # ── Failing in all subjects ──
    pct_cols = [f"{sub}_pct" for sub in subjects if f"{sub}_pct" in df.columns]
    if pct_cols:
        all_failing = df[(df[pct_cols] < 40).all(axis=1)]
        if len(all_failing) > 0:
            alerts.append({
                'severity': 'critical',
                'icon': '🔴',
                'title': 'Students Failing All Subjects',
                'detail': f'{len(all_failing)} student(s) scored below 40% in every subject. '
                          f'Emergency academic intervention needed.',
                'count': len(all_failing),
            })

    # ── High-risk concentration ──
    if class_col and class_col in df.columns:
        class_groups = df.groupby(class_col)
        for cls_name, cls_df in class_groups:
            cls_high = (cls_df['final_risk'] == 'High Risk').sum()
            cls_total = len(cls_df)
            if cls_total > 0 and cls_high / cls_total > 0.5:
                alerts.append({
                    'severity': 'critical',
                    'icon': '🏫',
                    'title': f'Class {cls_name}: Majority at High Risk',
                    'detail': f'{cls_high} of {cls_total} students ({cls_high/cls_total*100:.0f}%) '
                              f'in Class {cls_name} are at High Risk.',
                    'count': cls_high,
                })

    # ── Extreme z-scores ──
    if 'z_score' in df.columns:
        extreme = df[df['z_score'] < -2]
        if len(extreme) > 0:
            alerts.append({
                'severity': 'warning',
                'icon': '📉',
                'title': 'Extreme Underperformers',
                'detail': f'{len(extreme)} student(s) have z-scores below -2, '
                          f'indicating performance far below the class average.',
                'count': len(extreme),
            })

    # Sort: critical first
    severity_order = {'critical': 0, 'warning': 1}
    alerts.sort(key=lambda a: severity_order.get(a['severity'], 99))

    return alerts
