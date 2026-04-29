"""
session.py – Streamlit session state management helpers.
Provides safe getters/setters to prevent KeyError crashes.
Includes file-based auth persistence so login survives page refreshes.
"""
import os
import json
import streamlit as st

_AUTH_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'data', '.auth_session.json'
)


def _load_persisted_auth():
    """Load auth state from disk if it exists."""
    if os.path.exists(_AUTH_FILE):
        try:
            with open(_AUTH_FILE, 'r') as f:
                data = json.load(f)
            return data.get('authenticated', False), data.get('current_user')
        except Exception:
            return False, None
    return False, None


def _persist_auth():
    """Save current auth state to disk."""
    try:
        os.makedirs(os.path.dirname(_AUTH_FILE), exist_ok=True)
        with open(_AUTH_FILE, 'w') as f:
            json.dump({
                'authenticated': st.session_state.get('authenticated', False),
                'current_user': st.session_state.get('current_user'),
            }, f)
    except Exception:
        pass


def _clear_persisted_auth():
    """Remove persisted auth file on logout."""
    if os.path.exists(_AUTH_FILE):
        try:
            os.remove(_AUTH_FILE)
        except Exception:
            pass


def init_session_defaults():
    """Initialise all session keys with safe defaults."""
    defaults = {
        'raw_df': None,
        'cleaned_df': None,
        'processed_df': None,
        'mapping': None,
        'subjects': None,
        'health_score': None,
        'validation_issues': None,
        'file_name': None,
        'upload_complete': False,
        'mapping_complete': False,
        'validation_complete': False,
        'processing_complete': False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Restore auth from disk if session lost it
    if not st.session_state.get('authenticated', False):
        is_auth, user = _load_persisted_auth()
        if is_auth and user:
            st.session_state['authenticated'] = True
            st.session_state['current_user'] = user


def get(key, default=None):
    """Safe getter for session state."""
    return st.session_state.get(key, default)


def put(key, value):
    """Safe setter for session state."""
    st.session_state[key] = value


def is_ready(stage):
    """Check if a workflow stage has been completed."""
    return st.session_state.get(stage, False)
