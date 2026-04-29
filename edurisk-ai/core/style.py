"""
style.py – Premium light-mode CSS with animations, gradients, Material Icons,
sidebar branding, workflow tracker, and auth guard.
"""
import streamlit as st


def inject_custom_css():
    """Inject premium light-mode CSS with Material Icons and micro-animations."""
    try:
        st.set_page_config(
            page_title="EDURISK AI",
            page_icon="E",
            layout="wide",
            initial_sidebar_state="expanded",
        )
    except st.errors.StreamlitAPIException:
        pass  # Already set by app.py or another page

    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
    <style>
        /* === GLOBAL === */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .stApp {
            background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
        }

        /* === SIDEBAR === */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
            border-right: 1px solid #ede9fe;
        }
        /* Move branding to top using order */
        section[data-testid="stSidebar"] > div:first-child {
            display: flex;
            flex-direction: column;
        }
        /* Branding - Order 1 */
        section[data-testid="stSidebar"] > div:first-child > div:has(#sidebar-top-branding) {
            order: 1 !important;
        }
        /* Multipage Nav - Order 2 */
        section[data-testid="stSidebarNav"] {
            order: 2 !important;
        }
        /* Everything else - Order 3 */
        section[data-testid="stSidebar"] > div:first-child > div:not(:has(#sidebar-top-branding)):not(:has([data-testid="stSidebarNav"])) {
            order: 3 !important;
        }
        
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
            padding-top: 4px;
        }
        /* Nav links */
        section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"] {
            color: #475569 !important;
            border-radius: 10px;
            padding: 8px 14px 8px 40px;
            margin: 2px 8px;
            transition: all 0.2s;
            font-weight: 500;
            font-size: 0.88rem;
            position: relative;
        }
        /* Material Icon before each nav link */
        section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"]::before {
            font-family: 'Material Symbols Outlined';
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 18px;
            color: #6366f1;
            font-weight: 400;
        }
        a[data-testid="stSidebarNavLink"][href*="Home"]::before { content: "home" !important; }
        a[data-testid="stSidebarNavLink"][href*="Upload"]::before { content: "cloud_upload" !important; }
        a[data-testid="stSidebarNavLink"][href*="Mapping"]::before { content: "link" !important; }
        a[data-testid="stSidebarNavLink"][href*="Validation"]::before { content: "verified" !important; }
        a[data-testid="stSidebarNavLink"][href*="Dashboard"]::before { content: "dashboard" !important; }
        a[data-testid="stSidebarNavLink"][href*="Student"]::before { content: "person_search" !important; }
        a[data-testid="stSidebarNavLink"][href*="Reports"]::before { content: "description" !important; }
        a[data-testid="stSidebarNavLink"][href*="Interventions"]::before { content: "track_changes" !important; }
        a[data-testid="stSidebarNavLink"][href*="Compare"]::before { content: "compare_arrows" !important; }
        /* The 'app' entry (main page) */
        a[data-testid="stSidebarNavLink"][href="/"]::before { content: "rocket_launch" !important; }
        section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"]:hover {
            background: #ede9fe !important;
            color: #4f46e5 !important;
        }
        section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"][aria-current="page"] {
            background: linear-gradient(135deg, #ede9fe, #e0e7ff) !important;
            color: #4338ca !important;
            font-weight: 700;
            border-left: 3px solid #6366f1;
        }
        /* Sidebar buttons */
        section[data-testid="stSidebar"] .stButton > button {
            background: transparent !important;
            color: #64748b !important;
            border: 1px solid #e2e8f0 !important;
            box-shadow: none !important;
            font-size: 0.82rem !important;
        }
        section[data-testid="stSidebar"] .stButton > button:hover {
            background: #fef2f2 !important;
            border-color: #fca5a5 !important;
            color: #ef4444 !important;
            box-shadow: none !important;
            transform: none !important;
        }

        /* === HEADINGS === */
        h1 { color: #0f172a !important; font-weight: 800 !important; letter-spacing: -0.02em; }
        h2, h3 { color: #1e293b !important; font-weight: 700 !important; }
        h4, h5 { color: #334155 !important; }

        /* === METRIC CARDS with hover lift === */
        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 18px 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        div[data-testid="stMetric"]:hover {
            box-shadow: 0 8px 24px rgba(79,70,229,0.1);
            transform: translateY(-2px);
            border-color: #c7d2fe;
        }
        div[data-testid="stMetric"] label {
            color: #64748b !important; font-weight: 500;
            text-transform: uppercase; font-size: 0.72rem; letter-spacing: 0.06em;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: #0f172a !important; font-weight: 800; font-size: 1.7rem;
        }

        /* === BUTTONS with gradient & hover === */
        .stButton > button {
            background: linear-gradient(135deg, #4f46e5, #6366f1);
            color: white; border: none;
            border-radius: 10px; padding: 10px 24px;
            font-weight: 600; font-size: 0.9rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 2px 8px rgba(79,70,229,0.25);
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #4338ca, #4f46e5);
            box-shadow: 0 6px 20px rgba(79,70,229,0.35);
            transform: translateY(-1px);
        }
        .stButton > button:active {
            transform: translateY(0);
        }

        /* === TABS === */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px; background: transparent;
            border-bottom: 2px solid #e2e8f0;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0; padding: 10px 18px;
            color: #64748b; font-weight: 500; font-size: 0.88rem;
            transition: all 0.2s;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #4f46e5, #6366f1) !important;
            color: white !important; border-radius: 8px 8px 0 0;
            box-shadow: 0 -2px 8px rgba(79,70,229,0.15);
        }

        /* === DOWNLOAD BUTTONS === */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #059669, #10b981);
            color: white; border: none;
            border-radius: 10px; padding: 10px 24px;
            font-weight: 600;
            box-shadow: 0 2px 8px rgba(5,150,105,0.25);
            transition: all 0.3s;
        }
        .stDownloadButton > button:hover {
            background: linear-gradient(135deg, #047857, #059669);
            box-shadow: 0 6px 20px rgba(5,150,105,0.3);
            transform: translateY(-1px);
        }

        /* === PROGRESS BAR === */
        .stProgress > div > div {
            background: linear-gradient(90deg, #4f46e5, #818cf8, #6366f1);
            border-radius: 8px;
            background-size: 200% 100%;
            animation: shimmer 2s ease infinite;
        }
        @keyframes shimmer {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }

        /* === FILE UPLOADER === */
        [data-testid="stFileUploader"] {
            border: 2px dashed #cbd5e1; border-radius: 14px; padding: 20px;
            transition: border-color 0.3s, background 0.3s;
        }
        [data-testid="stFileUploader"]:hover {
            border-color: #4f46e5;
            background: rgba(79,70,229,0.02);
        }

        /* === ALERTS === */
        .stAlert { border-radius: 10px; }

        /* === MATERIAL ICON === */
        .mat-icon {
            font-family: 'Material Symbols Outlined';
            font-size: 20px;
            vertical-align: middle;
            margin-right: 6px;
            color: #4f46e5;
        }
        .mat-icon.danger { color: #ef4444; }
        .mat-icon.warning { color: #f59e0b; }
        .mat-icon.success { color: #10b981; }
        .mat-icon.muted { color: #94a3b8; }

        /* === CARD with hover lift === */
        .card {
            background: #ffffff; border: 1px solid #e2e8f0;
            border-radius: 14px; padding: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .card:hover {
            box-shadow: 0 8px 24px rgba(0,0,0,0.08);
            transform: translateY(-2px);
        }

        /* === EXPANDER === */
        .streamlit-expanderHeader {
            font-weight: 600;
            border-radius: 10px;
        }

        /* === DATAFRAME === */
        [data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
        }

        /* === PULSING DOT animation === */
        .pulse-dot {
            width: 8px; height: 8px; border-radius: 50%;
            display: inline-block; margin-right: 6px;
            animation: pulse 2s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(0.8); }
        }

        /* === GRADIENT TEXT === */
        .gradient-text {
            background: linear-gradient(135deg, #4f46e5, #7c3aed, #0891b2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

    </style>
    """, unsafe_allow_html=True)


def icon(name, css_class=""):
    """Return an HTML span for a Material Symbols icon."""
    return f'<span class="mat-icon {css_class}">{name}</span>'


def sidebar_branding():
    """Render premium sidebar: logo, pipeline progress card, user card."""
    from core.session import init_session_defaults
    from core.auth import is_authenticated, get_current_user, logout

    init_session_defaults()

    with st.sidebar:
        # ── Logo + Brand ──
        st.markdown("""
        <div id="sidebar-top-branding" style="display:flex; align-items:center; gap:12px; padding:8px 4px 16px 4px;">
            <div style="background:linear-gradient(135deg, #4f46e5, #6366f1);
                        width:44px; height:44px; border-radius:14px;
                        display:flex; align-items:center; justify-content:center; flex-shrink:0;
                        box-shadow:0 4px 14px rgba(79,70,229,0.3);">
                <span class="mat-icon" style="font-size:24px; color:white !important; margin:0;">verified_user</span>
            </div>
            <div>
                <h2 style="margin:0; font-weight:900; font-size:1.15rem; color:#0f172a !important;
                           letter-spacing:-0.02em;">EDURISK AI</h2>
                <p style="color:#94a3b8 !important; font-size:0.65rem; letter-spacing:0.06em;
                          text-transform:uppercase; margin:0;">Early Warning System</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ── Pipeline Progress Card (bottom section) ──
        stages = [
            ('upload_complete', 'Data Upload'),
            ('mapping_complete', 'Column Mapping'),
            ('validation_complete', 'AI Risk Analysis'),
            ('processing_complete', 'Results Ready'),
        ]

        completed = sum(1 for key, _ in stages if st.session_state.get(key, False))
        progress_pct = int(completed / len(stages) * 100)

        # Build stepper using simple inline HTML (no nested divs)
        rows = ""
        for i, (key, label) in enumerate(stages):
            done = st.session_state.get(key, False)
            is_next = not done and (i == 0 or st.session_state.get(stages[i-1][0], False))
            is_last = i == len(stages) - 1

            if done:
                dot = '&#10004;'
                dot_style = "color:white; background:#4f46e5; width:20px; height:20px; border-radius:50%; display:inline-block; text-align:center; line-height:20px; font-size:12px;"
                txt_style = "color:#0f172a; font-weight:600;"
            elif is_next:
                dot = '&#9679;'
                dot_style = "color:#4f46e5; background:white; width:20px; height:20px; border-radius:50%; border:2.5px solid #4f46e5; display:inline-block; text-align:center; line-height:16px; font-size:10px;"
                txt_style = "color:#4f46e5; font-weight:700;"
            else:
                dot = '&nbsp;'
                dot_style = "background:white; width:20px; height:20px; border-radius:50%; border:2px solid #cbd5e1; display:inline-block;"
                txt_style = "color:#94a3b8; font-weight:400;"

            lc = "#4f46e5" if done else "#e2e8f0"
            line_row = f'<p style="margin:0 0 0 9px; line-height:1;"><span style="color:{lc};">&#124;</span></p>' if not is_last else ''

            rows += f'<p style="margin:0; padding:3px 0; display:flex; align-items:center; gap:10px;"><span style="{dot_style}">{dot}</span><span style="font-size:0.82rem; {txt_style}">{label}</span></p>{line_row}'

        st.markdown(f"""<div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:14px; padding:16px; margin-top:12px;"><p style="display:flex; justify-content:space-between; align-items:center; margin:0 0 12px 0;"><span style="color:#0f172a; font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em;">Pipeline Progress</span><span style="color:#4f46e5; font-size:0.85rem; font-weight:800;">{progress_pct}%</span></p>{rows}</div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

        # ── User Card ──
        user = get_current_user()
        if user:
            initials = user['name'][0].upper()
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:10px; padding:10px 4px;
                        border-top:1px solid #e2e8f0;">
                <div style="background:linear-gradient(135deg, #6366f1, #8b5cf6);
                            width:38px; height:38px; border-radius:50%;
                            display:flex; align-items:center; justify-content:center; flex-shrink:0;
                            box-shadow:0 2px 8px rgba(99,102,241,0.3);">
                    <span style="color:white !important; font-weight:700; font-size:0.9rem;">{initials}</span>
                </div>
                <div style="overflow:hidden; flex:1;">
                    <p style="color:#0f172a !important; font-size:0.85rem; font-weight:700; margin:0;
                              white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{user['name']}</p>
                    <p style="color:#94a3b8 !important; font-size:0.68rem; margin:0;">Teacher</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Sign Out", key="sidebar_logout", use_container_width=True):
                logout()
                st.rerun()


def require_auth():
    """Gate that blocks the page if the user is not logged in."""
    from core.auth import is_authenticated
    if not is_authenticated():
        st.warning("Please log in to access this page.")
        st.info("Go to the **app** page (main entry) to log in or sign up.")
        st.stop()
