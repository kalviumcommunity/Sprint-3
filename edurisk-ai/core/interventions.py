"""
interventions.py – CRUD operations for teacher intervention tracking.
Persists data as JSON in data/interventions.json.
"""
import os
import json
from datetime import datetime

INTERVENTIONS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'data', 'interventions.json'
)

INTERVENTION_TYPES = [
    'Extra Tutoring',
    'Parent-Teacher Meeting',
    'Counselor Referral',
    'Peer Mentoring',
    'Individualized Learning Plan',
    'Home Visit',
    'Attendance Incentive',
    'Behavioral Support',
    'Other',
]

STATUS_OPTIONS = ['Pending', 'In Progress', 'Resolved', 'Escalated']

STATUS_COLORS = {
    'Pending': '#ef4444',
    'In Progress': '#f59e0b',
    'Resolved': '#10b981',
    'Escalated': '#8b5cf6',
}


def _load_interventions() -> list:
    if os.path.exists(INTERVENTIONS_FILE):
        with open(INTERVENTIONS_FILE, 'r') as f:
            return json.load(f)
    return []


def _save_interventions(data: list):
    os.makedirs(os.path.dirname(INTERVENTIONS_FILE), exist_ok=True)
    with open(INTERVENTIONS_FILE, 'w') as f:
        json.dump(data, f, indent=2, default=str)


def log_intervention(student_name: str, student_id: str, risk_level: str,
                     intervention_type: str, notes: str, teacher: str = '') -> dict:
    """Log a new intervention record."""
    interventions = _load_interventions()
    record = {
        'id': len(interventions) + 1,
        'student_name': student_name,
        'student_id': student_id,
        'risk_level': risk_level,
        'type': intervention_type,
        'notes': notes,
        'teacher': teacher,
        'status': 'Pending',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
    }
    interventions.append(record)
    _save_interventions(interventions)
    return record


def get_interventions(status_filter=None, risk_filter=None) -> list:
    """Get all interventions, optionally filtered."""
    interventions = _load_interventions()
    if status_filter:
        interventions = [i for i in interventions if i['status'] in status_filter]
    if risk_filter:
        interventions = [i for i in interventions if i['risk_level'] in risk_filter]
    return sorted(interventions, key=lambda x: x['created_at'], reverse=True)


def update_status(intervention_id: int, new_status: str, notes: str = ''):
    """Update the status of an intervention."""
    interventions = _load_interventions()
    for item in interventions:
        if item['id'] == intervention_id:
            item['status'] = new_status
            item['updated_at'] = datetime.now().isoformat()
            if notes:
                item['notes'] = item.get('notes', '') + f'\n[{new_status}] {notes}'
            break
    _save_interventions(interventions)


def delete_intervention(intervention_id: int):
    """Delete an intervention record."""
    interventions = _load_interventions()
    interventions = [i for i in interventions if i['id'] != intervention_id]
    _save_interventions(interventions)


def get_intervention_stats() -> dict:
    """Get summary statistics for interventions."""
    interventions = _load_interventions()
    stats = {s: 0 for s in STATUS_OPTIONS}
    for item in interventions:
        stats[item.get('status', 'Pending')] = stats.get(item.get('status', 'Pending'), 0) + 1
    stats['total'] = len(interventions)
    return stats
