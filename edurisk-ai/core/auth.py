"""
auth.py – Teacher authentication with school secret ID validation.
Uses a simple JSON file for user storage with hashed passwords.
Login state is persisted to disk so it survives page refreshes.
"""
import os
import json
import hashlib
import streamlit as st

USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'users.json')

# School secret IDs — teachers must provide one of these during signup.
# In production, these would come from a database or admin panel.
VALID_SCHOOL_CODES = [
    'EDURISK2026',
    'SCHOOL001',
    'ADMIN123',
]


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def _load_users() -> dict:
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}


def _save_users(users: dict):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)


def signup(name: str, email: str, password: str, school_code: str) -> tuple[bool, str]:
    """
    Register a new teacher account.
    Returns (success: bool, message: str).
    """
    if not name or not email or not password or not school_code:
        return False, "All fields are required."

    if school_code.upper().strip() not in VALID_SCHOOL_CODES:
        return False, "Invalid School Secret ID. Please contact your school administrator."

    users = _load_users()
    if email.lower().strip() in users:
        return False, "An account with this email already exists."

    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    users[email.lower().strip()] = {
        'name': name.strip(),
        'email': email.lower().strip(),
        'password_hash': _hash_password(password),
        'school_code': school_code.upper().strip(),
    }
    _save_users(users)
    return True, "Account created successfully. Please log in."


def login(email: str, password: str) -> tuple[bool, str, dict | None]:
    """
    Authenticate a teacher.
    Returns (success: bool, message: str, user_data: dict | None).
    """
    if not email or not password:
        return False, "Email and password are required.", None

    users = _load_users()
    user = users.get(email.lower().strip())

    if not user:
        return False, "No account found with this email.", None

    if user['password_hash'] != _hash_password(password):
        return False, "Incorrect password.", None

    # Persist auth to session and disk
    st.session_state['authenticated'] = True
    st.session_state['current_user'] = user

    from core.session import _persist_auth
    _persist_auth()

    return True, f"Welcome back, {user['name']}!", user


def is_authenticated() -> bool:
    return st.session_state.get('authenticated', False)


def get_current_user() -> dict | None:
    return st.session_state.get('current_user', None)


def logout():
    st.session_state['authenticated'] = False
    st.session_state['current_user'] = None

    from core.session import _clear_persisted_auth
    _clear_persisted_auth()
