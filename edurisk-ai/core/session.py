"""
session.py – Streamlit session state management helpers.
Provides safe getters/setters to prevent KeyError crashes.
"""
import streamlit as st


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


def get(key, default=None):
    """Safe getter for session state."""
    return st.session_state.get(key, default)


def put(key, value):
    """Safe setter for session state."""
    st.session_state[key] = value


def is_ready(stage):
    """Check if a workflow stage has been completed."""
    return st.session_state.get(stage, False)
