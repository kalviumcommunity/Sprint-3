"""
EDURISK AI – Main entry point.
Shows login/signup if not authenticated, otherwise the landing page.
"""
import streamlit as st
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.session import init_session_defaults
from core.auth import login, signup, is_authenticated, logout
from core.style import icon

# ── Page config ──
st.set_page_config(
    page_title="EDURISK AI",
    page_icon="E",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Light-mode CSS ──
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
<style>
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: #f8fafc; }
    section[data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #e2e8f0; }
    h1 { color: #0f172a !important; font-weight: 700 !important; }
    h2, h3 { color: #1e293b !important; }
    .mat-icon { font-family: 'Material Symbols Outlined'; font-size: 20px;
                vertical-align: middle; margin-right: 6px; color: #4f46e5; }
    .card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;
            padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    div[data-testid="stMetric"] { background: #ffffff; border: 1px solid #e2e8f0;
        border-radius: 12px; padding: 18px 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
    div[data-testid="stMetric"] label { color: #64748b !important; font-weight: 500;
        text-transform: uppercase; font-size: 0.72rem; letter-spacing: 0.06em; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #0f172a !important; font-weight: 700; font-size: 1.7rem; }
    .stButton > button { background: #4f46e5; color: white; border: none;
        border-radius: 8px; padding: 10px 24px; font-weight: 600;
        box-shadow: 0 1px 3px rgba(79,70,229,0.3); }
    .stButton > button:hover { background: #4338ca; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

init_session_defaults()

# ════════════════════════════════════════════
# AUTH GATE
# ════════════════════════════════════════════
if not is_authenticated():

    # Sidebar info for unauthenticated users
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 20px 0;">
            <span class="mat-icon" style="font-size:36px; color:#4f46e5;">school</span>
            <h2 style="margin:4px 0 0 0; color:#0f172a; font-weight:800; font-size:1.4rem;">
                EDURISK AI</h2>
            <p style="color:#64748b; font-size:0.75rem; margin-top:2px;">
                Student Performance Early Warning System</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("""
        <div style="padding: 0 8px;">
            <p style="color:#64748b; font-size:0.8rem;">
                <span class="mat-icon" style="font-size:16px;">info</span>
                Teachers need a <b>School Secret ID</b> to sign up.
                Contact your school administrator to get one.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Main area — Login / Signup
    col_spacer_l, col_form, col_spacer_r = st.columns([1, 2, 1])

    with col_form:
        st.markdown("""
        <div style="text-align:center; margin: 40px 0 32px 0;">
            <span class="mat-icon" style="font-size:48px; color:#4f46e5;">school</span>
            <h1 style="font-size:2rem; margin:8px 0 4px 0;">EDURISK AI</h1>
            <p style="color:#64748b; font-size:0.95rem;">
                Sign in to access the early warning dashboard</p>
        </div>
        """, unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

        with tab_login:
            with st.form("login_form"):
                st.markdown(f'{icon("email")} **Email**', unsafe_allow_html=True)
                login_email = st.text_input("Email", label_visibility="collapsed", placeholder="teacher@school.edu")
                st.markdown(f'{icon("lock")} **Password**', unsafe_allow_html=True)
                login_password = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Enter password")
                submitted = st.form_submit_button("Sign In", type="primary")

                if submitted:
                    success, msg, user = login(login_email, login_password)
                    if success:
                        st.session_state['authenticated'] = True
                        st.session_state['current_user'] = user
                        st.rerun()
                    else:
                        st.error(msg)

        with tab_signup:
            with st.form("signup_form"):
                st.markdown(f'{icon("person")} **Full Name**', unsafe_allow_html=True)
                signup_name = st.text_input("Name", label_visibility="collapsed", placeholder="e.g. Ms. Priya Sharma")
                st.markdown(f'{icon("email")} **Email**', unsafe_allow_html=True)
                signup_email = st.text_input("Email ", label_visibility="collapsed", placeholder="teacher@school.edu")
                st.markdown(f'{icon("lock")} **Password**', unsafe_allow_html=True)
                signup_password = st.text_input("Password ", type="password", label_visibility="collapsed", placeholder="Min 6 characters")
                st.markdown(f'{icon("key")} **School Secret ID**', unsafe_allow_html=True)
                signup_code = st.text_input("School Code", label_visibility="collapsed", placeholder="Provided by your school admin")
                submitted = st.form_submit_button("Create Account", type="primary")

                if submitted:
                    success, msg = signup(signup_name, signup_email, signup_password, signup_code)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)

            st.markdown("""
            <div style="background:#f1f5f9; padding:12px 16px; border-radius:8px; margin-top:8px;">
                <span class="mat-icon" style="font-size:16px; color:#d97706;">vpn_key</span>
                <span style="color:#64748b; font-size:0.8rem;">
                    The School Secret ID is provided by your institution.
                    This ensures only authorised staff can access student data.</span>
            </div>
            """, unsafe_allow_html=True)

    st.stop()

# ════════════════════════════════════════════
# AUTHENTICATED — LANDING PAGE
# ════════════════════════════════════════════
from core.style import sidebar_branding
sidebar_branding()

user = st.session_state.get('current_user', {})
teacher_name = user.get('name', 'Teacher')

st.markdown(f"""
<div style="text-align:center; padding: 48px 20px 24px 20px;">
    <span class="mat-icon" style="font-size:56px; color:#4f46e5;">school</span>
    <h1 style="font-size:2.4rem; font-weight:800; color:#0f172a; margin:12px 0 4px 0;">
        EDURISK AI</h1>
    <p style="color:#64748b; font-size:1.05rem; max-width:560px; margin:0 auto;">
        Transform school spreadsheets into actionable early-warning insights.
        Identify at-risk students before it's too late.</p>
    <p style="color:#4f46e5; font-size:0.9rem; margin-top:16px; font-weight:500;">
        Welcome, {teacher_name}</p>
</div>
""", unsafe_allow_html=True)

# Feature cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="card" style="text-align:center; min-height:180px;">
        <span class="mat-icon" style="font-size:32px;">analytics</span>
        <h3 style="font-size:1rem; margin:10px 0 6px 0;">Smart Analytics</h3>
        <p style="color:#64748b; font-size:0.83rem;">
            Auto-detect columns, validate data quality, and generate
            performance dashboards instantly.</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="card" style="text-align:center; min-height:180px;">
        <span class="mat-icon" style="font-size:32px;">psychology</span>
        <h3 style="font-size:1rem; margin:10px 0 6px 0;">ML-Powered Predictions</h3>
        <p style="color:#64748b; font-size:0.83rem;">
            Hybrid rule + ML engine combines expert knowledge with
            trained models for accurate risk scoring.</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="card" style="text-align:center; min-height:180px;">
        <span class="mat-icon" style="font-size:32px;">visibility</span>
        <h3 style="font-size:1rem; margin:10px 0 6px 0;">Explainable AI</h3>
        <p style="color:#64748b; font-size:0.83rem;">
            Every risk flag comes with clear, teacher-friendly explanations.
            No black boxes, just actionable insights.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.info("Use the sidebar to navigate through the workflow pages. Start by going to **Upload**.")
