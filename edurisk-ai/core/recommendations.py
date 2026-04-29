"""
recommendations.py – AI-powered intervention recommendations engine.
Generates personalized, actionable suggestions for each student based on
their risk factors, performance patterns, and peer comparisons.
"""
from core.config import SCORE_THRESHOLD, ATTENDANCE_THRESHOLD


def _attendance_recommendations(attendance):
    """Generate attendance-specific recommendations."""
    recs = []
    if attendance < 40:
        recs.append({
            'priority': 'critical',
            'icon': '🚨',
            'title': 'Immediate Parent Contact Required',
            'desc': f'Attendance is critically low at {attendance:.0f}%. '
                    'Schedule an urgent parent-teacher meeting to discuss '
                    'absenteeism and develop an attendance improvement plan.',
        })
        recs.append({
            'priority': 'critical',
            'icon': '🏠',
            'title': 'Home Visit Recommended',
            'desc': 'Consider a home visit to understand underlying causes '
                    '(health, family, transportation) behind chronic absenteeism.',
        })
    elif attendance < ATTENDANCE_THRESHOLD:
        recs.append({
            'priority': 'high',
            'icon': '📞',
            'title': 'Parent-Teacher Communication',
            'desc': f'Attendance at {attendance:.0f}% is below the {ATTENDANCE_THRESHOLD}% threshold. '
                    'Initiate regular communication with parents to monitor and encourage attendance.',
        })
        recs.append({
            'priority': 'medium',
            'icon': '🎯',
            'title': 'Attendance Incentive Program',
            'desc': 'Enroll student in a peer-based attendance incentive program '
                    'to boost motivation and daily participation.',
        })
    elif attendance < 75:
        recs.append({
            'priority': 'medium',
            'icon': '📊',
            'title': 'Monitor Attendance Trend',
            'desc': f'Attendance is {attendance:.0f}%. Track weekly to ensure '
                    'it doesn\'t decline further. Consider assigning an attendance buddy.',
        })
    return recs


def _academic_recommendations(avg_pct, weak_subjects, subjects, student_row):
    """Generate academic performance recommendations."""
    recs = []

    if avg_pct < 30:
        recs.append({
            'priority': 'critical',
            'icon': '📚',
            'title': 'Intensive Remedial Program',
            'desc': f'Average score is only {avg_pct:.1f}%. Enroll in a structured '
                    'remedial program with daily extra classes and simplified learning materials.',
        })
    elif avg_pct < SCORE_THRESHOLD:
        recs.append({
            'priority': 'high',
            'icon': '✏️',
            'title': 'After-School Tutoring',
            'desc': f'Average score ({avg_pct:.1f}%) is below {SCORE_THRESHOLD}%. '
                    'Schedule regular after-school tutoring sessions focusing on weak areas.',
        })

    # Subject-specific recommendations
    if weak_subjects:
        subject_names = ', '.join(weak_subjects[:3])
        recs.append({
            'priority': 'high',
            'icon': '🎓',
            'title': f'Targeted Subject Support: {subject_names}',
            'desc': f'Student is weak in {len(weak_subjects)} subject(s). '
                    f'Arrange subject-specific tutoring for {subject_names}.',
        })
        if len(weak_subjects) >= 3:
            recs.append({
                'priority': 'high',
                'icon': '🧩',
                'title': 'Learning Difficulty Assessment',
                'desc': 'Weakness across multiple subjects may indicate a learning '
                        'difficulty. Consider a diagnostic assessment by a school counselor.',
            })

    # Peer mentoring for borderline students
    if 35 <= avg_pct <= 50:
        recs.append({
            'priority': 'medium',
            'icon': '🤝',
            'title': 'Peer Mentoring Program',
            'desc': 'Pair with a high-performing classmate for collaborative study '
                    'sessions. Peer mentoring has shown 15-20% improvement in similar cases.',
        })

    return recs


def _behavioral_recommendations(z_score, risk_level):
    """Generate behavioral and engagement recommendations."""
    recs = []

    if z_score < -2:
        recs.append({
            'priority': 'high',
            'icon': '💬',
            'title': 'Counselor Referral',
            'desc': 'Performance is significantly below peers. '
                    'A counselor session can help identify non-academic factors '
                    '(stress, social issues, motivation) affecting performance.',
        })

    if risk_level == 'High Risk':
        recs.append({
            'priority': 'medium',
            'icon': '📝',
            'title': 'Individualized Learning Plan (ILP)',
            'desc': 'Create a personalized learning plan with weekly milestones, '
                    'modified assignments, and regular progress check-ins.',
        })
        recs.append({
            'priority': 'medium',
            'icon': '🔔',
            'title': 'Weekly Progress Check-in',
            'desc': 'Schedule a 5-minute weekly check-in to track progress, '
                    'provide encouragement, and adjust strategies as needed.',
        })

    return recs


def _positive_recommendations(avg_pct, z_score):
    """Recommendations for students who are doing well."""
    recs = []
    if avg_pct >= 80 and z_score >= 0.5:
        recs.append({
            'priority': 'info',
            'icon': '⭐',
            'title': 'Advanced Enrichment',
            'desc': 'Student is performing well above average. Consider '
                    'advanced assignments, leadership roles, or peer tutoring opportunities.',
        })
    elif avg_pct >= 60:
        recs.append({
            'priority': 'info',
            'icon': '✅',
            'title': 'Continue Monitoring',
            'desc': 'Performance is satisfactory. Maintain current support and '
                    'encourage participation in extracurricular academics.',
        })
    return recs


def generate_recommendations(student_row, mapping, subjects):
    """
    Generate a list of personalized recommendation dicts for a student.
    Each dict has: priority, icon, title, desc.
    Priority levels: 'critical', 'high', 'medium', 'info'
    """
    att_col = mapping.get('attendance')
    attendance = student_row.get(att_col, 75) if att_col else 75
    avg_pct = student_row.get('avg_percentage', 50)
    z_score = student_row.get('z_score', 0)
    risk_level = student_row.get('final_risk', 'Low Risk')
    weak_count = int(student_row.get('weak_subject_count', 0))

    # Identify weak subjects
    weak_subjects = []
    for sub in subjects:
        pct_col = f"{sub}_pct"
        val = student_row.get(pct_col, student_row.get(sub, 100))
        if val < SCORE_THRESHOLD:
            weak_subjects.append(sub)

    all_recs = []
    all_recs.extend(_attendance_recommendations(attendance))
    all_recs.extend(_academic_recommendations(avg_pct, weak_subjects, subjects, student_row))
    all_recs.extend(_behavioral_recommendations(z_score, risk_level))
    all_recs.extend(_positive_recommendations(avg_pct, z_score))

    # Sort by priority
    priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'info': 3}
    all_recs.sort(key=lambda r: priority_order.get(r['priority'], 99))

    return all_recs
