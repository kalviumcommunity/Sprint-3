"""
EDURISK AI – Main entry point.
Professional landing page with login/signup and authenticated dashboard.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.session import init_session_defaults
from core.auth import login, signup, is_authenticated, logout
from core.style import icon

try:
    st.set_page_config(page_title="EDURISK AI", page_icon="E", layout="wide", initial_sidebar_state="expanded")
except st.errors.StreamlitAPIException:
    pass

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
<style>
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%); }
    section[data-testid="stSidebar"] { background: linear-gradient(180deg, #fff 0%, #f8fafc 100%); border-right: 1px solid #e2e8f0; }
    h1 { color: #0f172a !important; font-weight: 800 !important; }
    h2, h3 { color: #1e293b !important; }
    .mat-icon { font-family: 'Material Symbols Outlined'; font-size: 20px; vertical-align: middle; margin-right: 6px; color: #4f46e5; }
    .card { background: #fff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); transition: all 0.3s cubic-bezier(0.4,0,0.2,1); }
    .card:hover { box-shadow: 0 8px 24px rgba(0,0,0,0.08); transform: translateY(-2px); }
    div[data-testid="stMetric"] { background: #fff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 18px 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); transition: all 0.3s; }
    div[data-testid="stMetric"]:hover { box-shadow: 0 8px 24px rgba(79,70,229,0.1); transform: translateY(-2px); }
    div[data-testid="stMetric"] label { color: #64748b !important; font-weight: 500; text-transform: uppercase; font-size: 0.72rem; letter-spacing: 0.06em; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #0f172a !important; font-weight: 800; font-size: 1.7rem; }
    .stButton > button { background: linear-gradient(135deg, #4f46e5, #6366f1); color: white; border: none; border-radius: 10px; padding: 10px 24px; font-weight: 600; box-shadow: 0 2px 8px rgba(79,70,229,0.25); transition: all 0.3s; }
    .stButton > button:hover { background: linear-gradient(135deg, #4338ca, #4f46e5); box-shadow: 0 6px 20px rgba(79,70,229,0.35); transform: translateY(-1px); }
    .stTabs [data-baseweb="tab-list"] { gap: 4px; background: transparent; border-bottom: 2px solid #e2e8f0; }
    .stTabs [data-baseweb="tab"] { border-radius: 8px 8px 0 0; padding: 10px 18px; color: #64748b; font-weight: 500; }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #4f46e5, #6366f1) !important; color: white !important; }
    .stDownloadButton > button { background: linear-gradient(135deg, #059669, #10b981); color: white; border: none; border-radius: 10px; font-weight: 600; box-shadow: 0 2px 8px rgba(5,150,105,0.25); }
    [data-testid="stFileUploader"] { border: 2px dashed #cbd5e1; border-radius: 14px; padding: 16px; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    @keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    .fade-in { animation: fadeInUp 0.6s ease-out forwards; }
    .fade-in-delay { animation: fadeInUp 0.6s ease-out 0.2s forwards; opacity: 0; }
    .fade-in-delay2 { animation: fadeInUp 0.6s ease-out 0.4s forwards; opacity: 0; }
</style>
""", unsafe_allow_html=True)

init_session_defaults()

# ════════════════════════════════════════════
# AUTH GATE
# ════════════════════════════════════════════
if not is_authenticated():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 20px 0;">
            <div style="background:linear-gradient(135deg, #4f46e5, #7c3aed); width:56px; height:56px; border-radius:16px; display:inline-flex; align-items:center; justify-content:center; box-shadow:0 4px 12px rgba(79,70,229,0.3);">
                <span class="mat-icon" style="font-size:28px; color:white; margin:0;">school</span>
            </div>
            <h2 style="margin:10px 0 0; color:#0f172a; font-weight:900; font-size:1.4rem;">EDURISK AI</h2>
            <p style="color:#64748b; font-size:0.72rem; margin-top:2px;">Student Performance Early Warning System</p>
        </div>
        <hr style="border-color:#e2e8f0;">
        <p style="color:#64748b; font-size:0.8rem; padding:0 8px;">
            <span class="mat-icon" style="font-size:16px;">info</span>
            Teachers need a <b>School Secret ID</b> to sign up. Contact your school administrator.
        </p>
        """, unsafe_allow_html=True)

    # ── Split layout: Left info + Right form ──
    col_info, col_spacer, col_form = st.columns([5, 1, 4])

    with col_info:
        st.markdown("""
        <div class="fade-in" style="padding: 60px 0 0 20px;">
            <div style="background:linear-gradient(135deg, #4f46e5, #7c3aed); width:64px; height:64px; border-radius:18px;
                        display:inline-flex; align-items:center; justify-content:center;
                        box-shadow:0 6px 20px rgba(79,70,229,0.3); animation: float 3s ease-in-out infinite;">
                <span class="mat-icon" style="font-size:32px; color:white; margin:0;">school</span>
            </div>
            <h1 style="font-size:2.8rem; margin:20px 0 8px; letter-spacing:-0.03em; line-height:1.1;">
                EDURISK
                <span style="background:linear-gradient(135deg, #4f46e5, #7c3aed); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">AI</span>
            </h1>
            <p style="color:#64748b; font-size:1.05rem; max-width:440px; line-height:1.6; margin-bottom:32px;">
                Transform raw school data into actionable early-warning insights.
                Identify at-risk students and take timely, data-driven action.</p>
        </div>
        """, unsafe_allow_html=True)

        # Stats badges
        st.markdown("""
        <div class="fade-in-delay" style="display:flex; gap:16px; flex-wrap:wrap; padding-left:20px;">
            <div style="background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:14px 20px; min-width:120px;">
                <p style="color:#4f46e5; font-size:1.4rem; font-weight:800; margin:0;">12+</p>
                <p style="color:#64748b; font-size:0.75rem; margin:0;">Interactive Charts</p>
            </div>
            <div style="background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:14px 20px; min-width:120px;">
                <p style="color:#7c3aed; font-size:1.4rem; font-weight:800; margin:0;">AI</p>
                <p style="color:#64748b; font-size:0.75rem; margin:0;">Powered Insights</p>
            </div>
            <div style="background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:14px 20px; min-width:120px;">
                <p style="color:#059669; font-size:1.4rem; font-weight:800; margin:0;">PDF</p>
                <p style="color:#64748b; font-size:0.75rem; margin:0;">Report Export</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Trust badges
        st.markdown("""
        <div class="fade-in-delay2" style="padding:28px 0 0 20px; display:flex; gap:24px; align-items:center;">
            <div style="display:flex; align-items:center; gap:6px;">
                <span class="mat-icon" style="font-size:16px; color:#10b981;">lock</span>
                <span style="color:#64748b; font-size:0.78rem;">Data stays local</span>
            </div>
            <div style="display:flex; align-items:center; gap:6px;">
                <span class="mat-icon" style="font-size:16px; color:#10b981;">verified_user</span>
                <span style="color:#64748b; font-size:0.78rem;">School-verified access</span>
            </div>
            <div style="display:flex; align-items:center; gap:6px;">
                <span class="mat-icon" style="font-size:16px; color:#10b981;">speed</span>
                <span style="color:#64748b; font-size:0.78rem;">Instant analysis</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_form:
        st.markdown("""
        <div class="fade-in-delay" style="background:#fff; border:1px solid #e2e8f0; border-radius:20px; padding:36px 32px; margin-top:40px; box-shadow:0 4px 24px rgba(0,0,0,0.06);">
            <h3 style="text-align:center; margin:0 0 4px; font-size:1.2rem; color:#0f172a;">Welcome back</h3>
            <p style="text-align:center; color:#94a3b8; font-size:0.85rem; margin-bottom:12px;">Sign in to your account</p>
            
            <!-- Demo Credentials Box -->
            <div style="background:#f1f5f9; border-radius:12px; padding:12px; border:1px dashed #cbd5e1; margin-bottom:20px;">
                <p style="margin:0; color:#475569; font-size:0.75rem; font-weight:600; text-transform:uppercase; letter-spacing:0.05em; text-align:center;">Demo Credentials</p>
                <div style="display:flex; justify-content:space-between; margin-top:8px; font-family:monospace; font-size:0.85rem; color:#4f46e5;">
                    <span>Email:</span>
                    <strong>teacher@school.edu</strong>
                </div>
                <div style="display:flex; justify-content:space-between; margin-top:4px; font-family:monospace; font-size:0.85rem; color:#4f46e5;">
                    <span>Pass:</span>
                    <strong>password123</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

        with tab_login:
            with st.form("login_form"):
                login_email = st.text_input("Email", value="teacher@school.edu")
                login_password = st.text_input("Password", type="password", value="password123")
                submitted = st.form_submit_button("Sign In", type="primary", use_container_width=True)
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
                signup_name = st.text_input("Full Name", placeholder="e.g. Ms. Priya Sharma")
                signup_email = st.text_input("Email ", placeholder="teacher@school.edu")
                signup_password = st.text_input("Password ", type="password", placeholder="Min 6 characters")
                signup_code = st.text_input("School Secret ID", placeholder="Provided by admin")
                submitted = st.form_submit_button("Create Account", type="primary", use_container_width=True)
                if submitted:
                    success, msg = signup(signup_name, signup_email, signup_password, signup_code)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)

    st.stop()

# ════════════════════════════════════════════
# AUTHENTICATED LANDING
# ════════════════════════════════════════════
from core.style import sidebar_branding
sidebar_branding()

user = st.session_state.get('current_user', {})
teacher_name = user.get('name', 'Teacher')

# ── Compact hero ──
hero_left, hero_right = st.columns([3, 2])
with hero_left:
    st.markdown(f"""
    <div style="padding:28px 0 8px 0;">
        <p style="color:#4f46e5; font-size:0.8rem; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; margin:0;">
            Welcome back</p>
        <h1 style="font-size:2rem; margin:6px 0; letter-spacing:-0.03em;">
            Hello, {teacher_name} 👋</h1>
        <p style="color:#64748b; font-size:0.92rem; max-width:480px;">
            Your intelligent early-warning dashboard is ready.
            Upload data or explore your latest analysis below.</p>
    </div>
    """, unsafe_allow_html=True)

with hero_right:
    if st.session_state.get('processing_complete'):
        from core.session import get
        proc_df = get('processed_df')
        if proc_df is not None:
            high = len(proc_df[proc_df['final_risk'] == 'High Risk'])
            st.markdown(f"""
            <div style="background:linear-gradient(135deg, #4f46e5, #7c3aed); border-radius:16px; padding:24px; margin-top:20px;
                        color:white; box-shadow:0 6px 20px rgba(79,70,229,0.25);">
                <p style="opacity:0.8; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.06em; margin:0;">Latest Analysis</p>
                <div style="display:flex; justify-content:space-between; margin-top:12px;">
                    <div>
                        <p style="font-size:2rem; font-weight:800; margin:0;">{len(proc_df)}</p>
                        <p style="opacity:0.7; font-size:0.78rem; margin:0;">Students</p>
                    </div>
                    <div>
                        <p style="font-size:2rem; font-weight:800; margin:0;">{high}</p>
                        <p style="opacity:0.7; font-size:0.78rem; margin:0;">At Risk</p>
                    </div>
                    <div>
                        <p style="font-size:2rem; font-weight:800; margin:0;">{proc_df['avg_percentage'].mean():.0f}%</p>
                        <p style="opacity:0.7; font-size:0.78rem; margin:0;">Avg Score</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")

# ── Quick Actions ──
st.markdown("### Quick Actions")

actions = [
    ("cloud_upload", "Upload Data", "Load a new student spreadsheet", "#4f46e5"),
    ("dashboard", "Dashboard", "View analytics & risk charts", "#7c3aed"),
    ("person_search", "Student Profiles", "Explore individual student performance", "#0891b2"),
    ("download", "Reports & Export", "Download PDF & CSV reports", "#059669"),
]

row1_l, row1_r = st.columns(2)
row2_l, row2_r = st.columns(2)
slots = [row1_l, row1_r, row2_l, row2_r]

for col, (ico, title, desc, color) in zip(slots, actions):
    with col:
        st.markdown(f"""
        <div class="card" style="display:flex; align-items:center; gap:16px; border-left:4px solid {color}; padding:18px 20px; margin-bottom:6px;">
            <div style="background:{color}10; min-width:48px; height:48px; border-radius:14px;
                        display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                <span class="mat-icon" style="font-size:24px; color:{color}; margin:0;">{ico}</span>
            </div>
            <div>
                <h4 style="margin:0 0 2px; font-size:0.95rem; color:#0f172a;">{title}</h4>
                <p style="color:#94a3b8; font-size:0.8rem; margin:0;">{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ── Platform capabilities ──
st.markdown("### Platform Capabilities")

cap_left, cap_right = st.columns(2)

with cap_left:
    capabilities_l = [
        ("analytics", "Smart Analytics", "Auto-detect columns, validate quality, generate dashboards instantly"),
        ("psychology", "ML Risk Prediction", "Hybrid rule + ML engine for accurate, explainable risk scoring"),
        ("auto_awesome", "AI Recommendations", "Personalized intervention suggestions for every at-risk student"),
    ]
    for ico, title, desc in capabilities_l:
        st.markdown(f"""
        <div style="display:flex; gap:14px; align-items:flex-start; padding:12px 0; border-bottom:1px solid #f1f5f9;">
            <div style="background:#4f46e510; min-width:40px; height:40px; border-radius:10px;
                        display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                <span class="mat-icon" style="font-size:20px; color:#4f46e5; margin:0;">{ico}</span>
            </div>
            <div>
                <strong style="color:#0f172a; font-size:0.9rem;">{title}</strong>
                <p style="color:#64748b; font-size:0.8rem; margin:4px 0 0;">{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

with cap_right:
    capabilities_r = [
        ("assignment", "Intervention Tracker", "Log, monitor, and track teacher actions with status workflows"),
        ("compare_arrows", "Batch Comparison", "Compare datasets across terms to measure improvement over time"),
        ("picture_as_pdf", "PDF Reports", "Professional branded reports ready to print and share"),
    ]
    for ico, title, desc in capabilities_r:
        st.markdown(f"""
        <div style="display:flex; gap:14px; align-items:flex-start; padding:12px 0; border-bottom:1px solid #f1f5f9;">
            <div style="background:#7c3aed10; min-width:40px; height:40px; border-radius:10px;
                        display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                <span class="mat-icon" style="font-size:20px; color:#7c3aed; margin:0;">{ico}</span>
            </div>
            <div>
                <strong style="color:#0f172a; font-size:0.9rem;">{title}</strong>
                <p style="color:#64748b; font-size:0.8rem; margin:4px 0 0;">{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer CTA ──
st.markdown("""
<div style="background:linear-gradient(135deg, #eff6ff, #dbeafe); padding:18px 24px; border-radius:14px;
            border-left:4px solid #4f46e5; margin-top:20px; box-shadow:0 2px 8px rgba(79,70,229,0.08);">
    <span class="mat-icon" style="font-size:20px;">rocket_launch</span>
    <strong style="color:#1e3a5f;">Get Started</strong>
    <p style="color:#1e3a5f; margin:6px 0 0; font-size:0.88rem; opacity:0.85;">
        Navigate to <b>Upload</b> in the sidebar to load your student data and begin the analysis.</p>
</div>
""", unsafe_allow_html=True)
