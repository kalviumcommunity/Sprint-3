"""
style.py – Shared light-mode CSS, Material Icons, sidebar branding, and auth guard.
"""
import streamlit as st


def inject_custom_css():
    """Inject clean light-mode CSS with Material Icons."""
    st.set_page_config(
        page_title="EDURISK AI",
        page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><text y='20' font-size='18'>E</text></svg>",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
    <style>
        /* === GLOBAL === */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .stApp { background: #f8fafc; }

        /* === SIDEBAR === */
        section[data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #e2e8f0;
        }

        /* === HEADINGS === */
        h1 { color: #0f172a !important; font-weight: 700 !important; }
        h2, h3 { color: #1e293b !important; font-weight: 600 !important; }
        h4, h5 { color: #334155 !important; }

        /* === METRIC CARDS === */
        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 18px 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            transition: box-shadow 0.2s;
        }
        div[data-testid="stMetric"]:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        div[data-testid="stMetric"] label {
            color: #64748b !important; font-weight: 500;
            text-transform: uppercase; font-size: 0.72rem; letter-spacing: 0.06em;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: #0f172a !important; font-weight: 700; font-size: 1.7rem;
        }

        /* === BUTTONS === */
        .stButton > button {
            background: #4f46e5; color: white; border: none;
            border-radius: 8px; padding: 10px 24px;
            font-weight: 600; font-size: 0.9rem;
            transition: background 0.2s, box-shadow 0.2s;
            box-shadow: 0 1px 3px rgba(79,70,229,0.3);
        }
        .stButton > button:hover {
            background: #4338ca;
            box-shadow: 0 4px 12px rgba(79,70,229,0.25);
        }

        /* === TABS === */
        .stTabs [data-baseweb="tab-list"] { gap: 4px; background: transparent; border-bottom: 2px solid #e2e8f0; }
        .stTabs [data-baseweb="tab"] {
            border-radius: 6px 6px 0 0; padding: 8px 16px;
            color: #64748b; font-weight: 500; font-size: 0.88rem;
        }
        .stTabs [aria-selected="true"] {
            background: #4f46e5 !important; color: white !important; border-radius: 6px 6px 0 0;
        }

        /* === DOWNLOAD BUTTONS === */
        .stDownloadButton > button {
            background: #059669; color: white; border: none;
            border-radius: 8px; padding: 10px 24px;
            font-weight: 600; box-shadow: 0 1px 3px rgba(5,150,105,0.3);
        }
        .stDownloadButton > button:hover {
            background: #047857;
        }

        /* === PROGRESS BAR === */
        .stProgress > div > div {
            background: linear-gradient(90deg, #4f46e5, #6366f1);
            border-radius: 6px;
        }

        /* === FILE UPLOADER === */
        [data-testid="stFileUploader"] {
            border: 2px dashed #cbd5e1; border-radius: 12px; padding: 16px;
        }
        [data-testid="stFileUploader"]:hover { border-color: #4f46e5; }

        /* === ALERTS === */
        .stAlert { border-radius: 8px; }

        /* === MATERIAL ICON HELPER === */
        .mat-icon {
            font-family: 'Material Symbols Outlined';
            font-size: 20px;
            vertical-align: middle;
            margin-right: 6px;
            color: #4f46e5;
        }
        .mat-icon.danger { color: #dc2626; }
        .mat-icon.warning { color: #d97706; }
        .mat-icon.success { color: #059669; }
        .mat-icon.muted { color: #94a3b8; }

        /* === CARD === */
        .card {
            background: #ffffff; border: 1px solid #e2e8f0;
            border-radius: 12px; padding: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }

        /* === HIDE BRANDING === */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


def icon(name, css_class=""):
    """Return an HTML span for a Material Symbols icon."""
    return f'<span class="mat-icon {css_class}">{name}</span>'


def sidebar_branding():
    """Render sidebar brand and workflow progress in light mode."""
    from core.session import init_session_defaults
    from core.auth import is_authenticated, get_current_user, logout

    init_session_defaults()

    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center; padding: 16px 0 8px 0;">
            <span class="mat-icon" style="font-size:36px; color:#4f46e5;">school</span>
            <h2 style="margin:4px 0 0 0; color:#0f172a; font-weight:800; font-size:1.4rem;">
                EDURISK AI</h2>
            <p style="color:#64748b; font-size:0.75rem; margin-top:2px;">
                Student Performance Early Warning System</p>
        </div>
        <hr style="border-color:#e2e8f0; margin:8px 0 16px 0;">
        """, unsafe_allow_html=True)

        # Show logged-in user
        user = get_current_user()
        if user:
            st.markdown(f"""
            <div style="background:#f1f5f9; padding:10px 14px; border-radius:8px; margin-bottom:12px;">
                <span class="mat-icon" style="font-size:16px;">person</span>
                <span style="color:#334155; font-size:0.82rem; font-weight:500;">{user['name']}</span>
                <br><span style="color:#94a3b8; font-size:0.7rem;">{user['email']}</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Logout", key="sidebar_logout"):
                logout()
                st.rerun()

        # Workflow progress
        stages = [
            ('upload_complete', 'cloud_upload', 'Upload'),
            ('mapping_complete', 'link', 'Mapping'),
            ('validation_complete', 'check_circle', 'Validation'),
            ('processing_complete', 'analytics', 'Analysis'),
        ]
        st.markdown("**Workflow**")
        for key, ico, label in stages:
            done = st.session_state.get(key, False)
            color = "#059669" if done else "#cbd5e1"
            check = "check_circle" if done else "radio_button_unchecked"
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:6px; padding:3px 0;">
                <span class="mat-icon" style="font-size:16px; color:{color};">{check}</span>
                <span style="color:{'#334155' if done else '#94a3b8'}; font-size:0.82rem;">{label}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("EDURISK AI v1.0")


def require_auth():
    """Gate that blocks the page if the user is not logged in."""
    from core.auth import is_authenticated
    if not is_authenticated():
        st.warning("Please log in to access this page.")
        st.info("Go to the **app** page (main entry) to log in or sign up.")
        st.stop()
