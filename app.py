import hashlib
import streamlit as st

from agent import run_applypilot
from mission import generate_application_mission
from browser_agent import inspect_and_open_application

st.set_page_config(
    page_title="ApplyPilot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Hide Streamlit's native developer/toolbar controls for normal viewers.
# ApplyPilot provides its own product UI instead.
st.set_option("client.toolbarMode", "minimal")

# ------------------------------------------------------------------
# PREMIUM DARK UI
# ------------------------------------------------------------------
st.markdown(
    """
    <style>
    :root {
        --bg: #07111f;
        --panel: #0d1a2b;
        --panel2: #101f33;
        --border: #20334d;
        --text: #edf4ff;
        --muted: #91a4bd;
        --accent: #7c5cff;
        --accent2: #22d3ee;
        --good: #35d07f;
        --warn: #f4b942;
        --danger: #ff5d73;
    }
    .stApp { background: linear-gradient(135deg, #07111f 0%, #0a1526 48%, #11152b 100%); color: var(--text); }
    [data-testid="stHeader"] { background: rgba(7,17,31,.82); }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #081322 0%, #0d1829 100%); border-right: 1px solid var(--border); }
    [data-testid="stSidebar"] * { color: #e9f1ff; }
    .block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 1450px; }
    .hero { padding: 1.8rem 2rem; border: 1px solid #243956; border-radius: 24px; background: radial-gradient(circle at 85% 15%, rgba(124,92,255,.22), transparent 34%), linear-gradient(135deg, #0e1d31, #0b1627); box-shadow: 0 18px 60px rgba(0,0,0,.24); }
    .brand { font-size: 2.65rem; font-weight: 850; letter-spacing: -1.5px; }
    .brand span { color: #9d8aff; }
    .tagline { color: #a9bad0; font-size: 1.03rem; margin-top: .25rem; }
    .live-pill { display:inline-block; padding:.35rem .7rem; border-radius:999px; background:rgba(53,208,127,.12); border:1px solid rgba(53,208,127,.3); color:#7bf0ad; font-weight:700; font-size:.78rem; }
    .stage { min-height: 104px; padding: 1rem; border-radius: 16px; border: 1px solid var(--border); background: rgba(13,26,43,.86); }
    .stage.active { border-color: #7c5cff; box-shadow: inset 0 0 0 1px rgba(124,92,255,.18), 0 8px 28px rgba(124,92,255,.08); }
    .stage.done { border-color: rgba(53,208,127,.35); }
    .stage-num { font-size:.72rem; color:#7f94af; font-weight:800; letter-spacing:.8px; }
    .stage-title { font-weight:800; margin-top:.25rem; font-size:1.02rem; }
    .stage-desc { color:#91a4bd; font-size:.78rem; margin-top:.2rem; }
    .section-label { color:#8ea4bf; font-size:.76rem; font-weight:800; letter-spacing:1.2px; text-transform:uppercase; margin-bottom:.3rem; }
    .search-hero { padding:1.3rem 1.4rem; border:1px solid #2a4161; border-radius:18px; background:linear-gradient(135deg, rgba(124,92,255,.12), rgba(34,211,238,.05)); }
    .search-target { font-size:1.25rem; font-weight:750; color:#f5f8ff; }
    .stat-card { padding:1rem 1.1rem; border:1px solid var(--border); border-radius:16px; background:rgba(13,26,43,.82); }
    .op-card { padding:1.25rem; border:1px solid #233954; border-radius:20px; background:linear-gradient(145deg,#0d1b2e,#0b1727); margin-bottom:1rem; box-shadow:0 10px 28px rgba(0,0,0,.14); }
    .op-rank { color:#8f7cff; font-weight:850; font-size:.75rem; letter-spacing:1px; }
    .op-title { font-size:1.18rem; font-weight:800; color:#f4f8ff; margin:.2rem 0 .45rem; }
    .company { color:#aabbd1; font-weight:650; }
    .chip { display:inline-block; padding:.28rem .55rem; border-radius:999px; margin:.15rem .18rem .15rem 0; font-size:.72rem; border:1px solid #29415f; background:#102238; color:#cfe0f4; }
    .score { font-size:2rem; font-weight:850; color:#9e8cff; text-align:center; }
    .score-label { text-align:center; color:#8196af; font-size:.72rem; text-transform:uppercase; letter-spacing:.8px; }
    .mission-box { padding:1.25rem; border:1px solid #2b4160; border-radius:18px; background:#0d1b2e; }
    .action-box { padding:1.3rem; border:1px solid #2b4160; border-radius:20px; background:radial-gradient(circle at 80% 10%,rgba(124,92,255,.12),transparent 35%),#0d1a2b; }
    .status-ready { border-left:4px solid #35d07f; background:rgba(53,208,127,.08); }
    .status-warn { border-left:4px solid #f4b942; background:rgba(244,185,66,.08); }
    .status-danger { border-left:4px solid #ff5d73; background:rgba(255,93,115,.08); }
    .status-info { border-left:4px solid #22d3ee; background:rgba(34,211,238,.07); }
    .field-row { padding:.55rem .1rem; border-bottom:1px solid #1d3047; color:#d9e5f3; }
    .muted { color:#8fa2ba; }
    .small { font-size:.78rem; color:#8fa2ba; }
    div[data-testid="stMetricValue"] { color:#f1f5ff; }
    /* Dark-theme Streamlit form controls */
    .stTextInput > div > div, .stTextArea > div > div,
    [data-baseweb="input"], [data-baseweb="textarea"] { background:#101f33 !important; border-color:#2a4161 !important; }
    .stTextInput input, .stTextArea textarea, [data-baseweb="input"] input, [data-baseweb="textarea"] textarea { background:#101f33 !important; color:#f4f8ff !important; -webkit-text-fill-color:#f4f8ff !important; caret-color:#22d3ee !important; }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder { color:#7186a1 !important; -webkit-text-fill-color:#7186a1 !important; }
    .stTextInput label, .stTextArea label, [data-testid="stWidgetLabel"] p { color:#cbd8e8 !important; }
    [data-testid="stSidebar"] input, [data-testid="stSidebar"] textarea { background:#0f1d30 !important; color:#f4f8ff !important; -webkit-text-fill-color:#f4f8ff !important; }
    .profile-popover { padding:.8rem 1rem; border:1px solid #496589; border-radius:16px; background:linear-gradient(145deg,#132743,#0d1b2f); color:#f4f8ff !important; }
    .profile-popover, .profile-popover * { color:#f4f8ff !important; -webkit-text-fill-color:#f4f8ff !important; }
    .profile-popover .small { color:#b9cbe0 !important; -webkit-text-fill-color:#b9cbe0 !important; }
    /* Streamlit popover panel: force all profile text to high contrast. */
    [data-baseweb="popover"], [data-baseweb="popover"] > div { background:#0d1b2f !important; color:#f4f8ff !important; }
    [data-baseweb="popover"] p, [data-baseweb="popover"] span, [data-baseweb="popover"] div,
    [data-baseweb="popover"] label, [data-baseweb="popover"] strong, [data-baseweb="popover"] b {
        color:#f4f8ff !important; -webkit-text-fill-color:#f4f8ff !important;
    }
    [data-baseweb="popover"] .small { color:#b9cbe0 !important; -webkit-text-fill-color:#b9cbe0 !important; }
    .topbar-sub { color:#8fa2ba; font-size:.82rem; margin-top:.15rem; }
    /* ================================================================
       HIGH-CONTRAST CONTROLS
       Streamlit defaults are intentionally overridden so every control
       remains readable on the dark ApplyPilot background.
       ================================================================ */
    .stButton > button,
    .stLinkButton > a,
    [data-testid="stPopover"] > button,
    [data-testid="stPopoverButton"] {
        border: 1px solid #405477 !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, #263653 0%, #1b2941 100%) !important;
        color: #f8fbff !important;
        -webkit-text-fill-color: #f8fbff !important;
        font-weight: 800 !important;
        box-shadow: 0 5px 16px rgba(0,0,0,.18) !important;
        min-height: 42px !important;
    }
    .stButton > button:hover,
    .stLinkButton > a:hover,
    [data-testid="stPopover"] > button:hover,
    [data-testid="stPopoverButton"]:hover {
        border-color: #9b8cff !important;
        background: linear-gradient(135deg, #35476b 0%, #293955 100%) !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        box-shadow: 0 8px 24px rgba(124,92,255,.22) !important;
        transform: translateY(-1px);
    }
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #7c5cff 0%, #a855f7 100%) !important;
        border-color: #a78bfa !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        box-shadow: 0 8px 26px rgba(124,92,255,.30) !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(135deg, #8b72ff 0%, #c06cff 100%) !important;
        color: #ffffff !important;
    }
    .stButton > button:disabled,
    .stLinkButton > a[aria-disabled="true"] {
        background: #18263a !important;
        border-color: #334965 !important;
        color: #7f94ad !important;
        -webkit-text-fill-color: #7f94ad !important;
        opacity: 1 !important;
        box-shadow: none !important;
    }
    .stLinkButton > a {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-decoration: none !important;
    }
    /* Popover/profile trigger */
    [data-testid="stPopover"] > button,
    [data-testid="stPopoverButton"] {
        background: linear-gradient(135deg, #1f2d49 0%, #293657 100%) !important;
        border-color: #4a5f86 !important;
    }
    [data-testid="stPopover"] > button *,
    [data-testid="stPopoverButton"] * {
        color: #f8fbff !important;
        -webkit-text-fill-color: #f8fbff !important;
    }
    /* ================================================================
       SIDEBAR NAVIGATION — ALWAYS VISIBLE
       Keep the native sidebar control obvious, but do not target
       button[kind="header"] because Streamlit also uses that selector
       for its top-right toolbar controls.
       ================================================================ */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapsedControl"] button {
        visibility: visible !important;
        display: flex !important;
        pointer-events: auto !important;
        opacity: 1 !important;
        z-index: 999999 !important;
        background: linear-gradient(135deg, #7c5cff 0%, #5b3fd4 100%) !important;
        border: 2px solid #b9a9ff !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        box-shadow: 0 6px 22px rgba(0,0,0,.42), 0 0 0 1px rgba(124,92,255,.25) !important;
        min-width: 52px !important;
        min-height: 44px !important;
        align-items: center !important;
        justify-content: center !important;
    }

    [data-testid="stSidebarCollapseButton"] *,
    [data-testid="stSidebarCollapseButton"] button *,
    [data-testid="stSidebarCollapsedControl"] *,
    [data-testid="stSidebarCollapsedControl"] button * {
        color:#ffffff !important;
        fill:#ffffff !important;
        stroke:#ffffff !important;
        opacity:1 !important;
    }

    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="stSidebarCollapseButton"] svg path,
    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="stSidebarCollapsedControl"] svg path {
        color:#ffffff !important;
        fill:#ffffff !important;
        stroke:#ffffff !important;
        opacity:1 !important;
    }

    [data-testid="stSidebarCollapsedControl"] button:hover,
    [data-testid="stSidebarCollapseButton"] button:hover {
        background: linear-gradient(135deg, #927bff 0%, #704ee8 100%) !important;
        border-color: #ffffff !important;
        transform: translateY(-1px) !important;
    }
    /* Metrics: labels and values must remain readable */
    [data-testid="stMetric"] {
        background: rgba(16,31,51,.72) !important;
        border: 1px solid #263d5a !important;
        border-radius: 14px !important;
        padding: .8rem .9rem !important;
    }
    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] *,
    [data-testid="stMetricDelta"],
    [data-testid="stMetricDelta"] * {
        color: #9fb2ca !important;
        -webkit-text-fill-color: #9fb2ca !important;
    }
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] * {
        color: #f7faff !important;
        -webkit-text-fill-color: #f7faff !important;
    }
    /* Selectors, checkboxes and popovers */
    [data-baseweb="select"] > div,
    [data-baseweb="popover"] > div {
        background: #101f33 !important;
        border-color: #2f4767 !important;
        color: #f4f8ff !important;
    }
    [data-baseweb="select"] *,
    [role="option"] {
        color: #f4f8ff !important;
        -webkit-text-fill-color: #f4f8ff !important;
    }
    [data-testid="stCheckbox"] label,
    [data-testid="stCheckbox"] label * {
        color: #eaf2ff !important;
        -webkit-text-fill-color: #eaf2ff !important;
    }
    /* Mission notification */
    .mission-alert {
        margin: 1rem 0 1.2rem;
        padding: 1rem 1.2rem;
        border: 1px solid rgba(53,208,127,.45);
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(53,208,127,.14), rgba(34,211,238,.07));
        box-shadow: 0 10px 28px rgba(0,0,0,.15);
    }
    .mission-alert-title { color:#9ff5c6; font-weight:850; font-size:1.02rem; }
    .mission-alert-text { color:#c7d7e8; margin-top:.2rem; }
    .jump-link {
        display:inline-block; margin-top:.55rem; padding:.45rem .75rem; border-radius:9px;
        border:1px solid #405477; background:#17263d; color:#dfeaff !important;
        text-decoration:none !important; font-weight:750;
    }
    .jump-link:hover { border-color:#9b8cff; background:#253653; color:#fff !important; }
    .stButton > button { border-radius:12px; font-weight:750; }
    .stLinkButton > a { border-radius:12px; font-weight:700; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# STATE
# ------------------------------------------------------------------
defaults = {
    "recommendations": None,
    "selected_opportunity": None,
    "mission": None,
    "approved": False,
    "browser_result": None,
    "current_stage": "discover",
    "profile_snapshot": None,
    "mission_built": False,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ------------------------------------------------------------------
# SIDEBAR PROFILE
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 👤 Candidate Profile")
    st.markdown("### ✨ Start here")
    st.caption("Fill in your profile in the main panel. Your details stay empty until you enter them.")
    st.markdown("👈 **Use the Candidate Profile panel in the main workspace.**")
    st.markdown("---")
    st.caption("🔒 Human-in-the-loop: ApplyPilot never performs the final application submission automatically.")


def build_personalized_cover_letter(profile, opportunity):
    """Create a cover letter from the current user's actual profile."""
    name = (profile.get("name") or "Candidate").strip()
    education = (profile.get("education") or "").strip()
    skills = [str(s).strip() for s in (profile.get("skills") or []) if str(s).strip()]
    goal = (profile.get("goal") or "").strip()
    title = (opportunity.get("title") or "this opportunity").strip()
    company = (opportunity.get("company") or "your organization").strip()
    location = (profile.get("location") or "").strip()
    skill_text = ", ".join(skills) if skills else "my technical skills"
    education_text = education or "my current academic background"
    goal_text = goal or "this opportunity"
    location_line = f" I am currently seeking opportunities in {location}." if location else ""
    return (
        f"Dear Hiring Team at {company},\n\n"
        f"I am {name}, currently pursuing {education_text}, and I am excited to apply for {title}. "
        f"I am specifically looking for {goal_text}.{location_line}\n\n"
        f"My relevant skills include {skill_text}. I am eager to apply these skills to meaningful work, "
        f"learn from your team, and contribute to the goals of {company}.\n\n"
        f"I would welcome the opportunity to discuss how my background and skills could contribute to this role. "
        f"Thank you for considering my application.\n\n"
        f"Best regards,\n{name}"
    )


def build_profile():
    return {
        "name": name.strip(),
        "education": education.strip(),
        "skills": [s.strip() for s in skills_text.split(",") if s.strip()],
        "location": location.strip(),
        "goal": goal.strip(),
    }


# Cache discovery by profile for 15 minutes. Re-running Streamlit with the same
# search target does not call Anakin again during the cache window.
@st.cache_data(ttl=900, show_spinner=False)
def cached_discovery(profile):
    return run_applypilot(profile)

# ------------------------------------------------------------------
# HERO
# ------------------------------------------------------------------
st.markdown(
    '<div class="hero"><div class="live-pill">● LIVE AGENT WORKSPACE</div><div class="brand">🚀 Apply<span>Pilot</span></div><div class="tagline">An autonomous career agent that discovers, reasons, prepares and navigates — with you in control of the final action.</div></div>',
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# START HERE — MAIN PROFILE
# ------------------------------------------------------------------
# Keep the editable profile in the main workspace so first-time users can
# see it immediately, even if Streamlit remembers a collapsed sidebar.
st.markdown("### 👋 Start here")
st.markdown(
    '<div class="search-hero"><div class="search-target">👤 Step 1 — Complete your Candidate Profile</div>'
    '<div class="small" style="margin-top:.4rem;line-height:1.7">Enter your own details below. All fields start blank for every new user. These details are used for live opportunity matching and personalized application preparation.</div></div>',
    unsafe_allow_html=True,
)

with st.expander("👤 Candidate Profile — fill this first", expanded=True):
    profile_col1, profile_col2 = st.columns(2)
    with profile_col1:
        name = st.text_input("Full name", placeholder="Your full name", value="", key="main_name")
        education = st.text_input("Education", value="", placeholder="e.g. Final-year BCA", key="main_education")
        location = st.text_input("Location preference", value="", placeholder="e.g. Chennai / India / Remote", key="main_location")
    with profile_col2:
        skills_text = st.text_area("Skills", value="", placeholder="e.g. Python, Java, React, SQL", help="Separate skills with commas.", key="main_skills")
        goal = st.text_area("What are you looking for?", value="", placeholder="e.g. AI internships, frontend jobs, data science roles", height=90, help="This is the main search intent. Changing it changes the Anakin search queries.", key="main_goal")

    missing_fields = []
    if not name.strip():
        missing_fields.append("full name")
    if not education.strip():
        missing_fields.append("education")
    if not skills_text.strip():
        missing_fields.append("skills")
    if not location.strip():
        missing_fields.append("location preference")
    if not goal.strip():
        missing_fields.append("search target")

    if missing_fields:
        st.info("✍️ Complete all five profile fields above to unlock Live Discovery. Missing: " + ", ".join(missing_fields) + ".")
    else:
        st.success("✓ Candidate Profile complete — you can now run Live Discovery.")

    find_button = st.button(
        "✦ Run Live Discovery",
        type="primary",
        use_container_width=True,
        disabled=bool(missing_fields),
        key="main_discovery_button",
    )

st.write("")

st.markdown("### Your agent journey")
stages = [
    ("discover", "01", "🔎", "DISCOVER", "Find live opportunities"),
    ("analyze", "02", "🧠", "ANALYZE", "Reason about fit"),
    ("prepare", "03", "📋", "PREPARE", "Build an application mission"),
    ("act", "04", "🤖", "ACT", "Navigate the live web"),
    ("review", "05", "🛡️", "REVIEW", "Human controls submission"),
]
order = {x[0]: i for i, x in enumerate(stages)}
current = order.get(st.session_state.current_stage, 0)
cols = st.columns(5)
for i, (key, number, icon, title, desc) in enumerate(stages):
    cls = "active" if i == current else "done" if i < current else ""
    mark = "✓" if i < current else "●" if i == current else "○"
    with cols[i]:
        st.markdown(f'<div class="stage {cls}"><div class="stage-num">{mark} STAGE {number}</div><div class="stage-title">{icon} {title}</div><div class="stage-desc">{desc}</div></div>', unsafe_allow_html=True)

st.write("")
st.markdown(
    """<div class="search-hero">
        <div class="search-target">🧭 How to use ApplyPilot</div>
        <div class="small" style="margin-top:.45rem;line-height:1.7">
            <b>1.</b> Open <b>Candidate Profile — fill this first</b> above and complete every field → <b>2.</b> Run Live Discovery → <b>3.</b> Choose an opportunity and click <b>Build Mission</b> → <b>4.</b> Tick <b>every checklist item</b> → <b>5.</b> Tick <b>Human approval</b> → <b>6.</b> Click <b>Start Anakin Browser Agent</b>.
        </div>
        <div class="small" style="margin-top:.55rem">💡 <b>Nothing is submitted automatically.</b> ApplyPilot always stops before final submission.</div>
    </div>""",
    unsafe_allow_html=True,
)

# Clear, persistent feedback after Build Mission so the user knows
# exactly what happened and where the generated mission is located.
if st.session_state.mission_built and st.session_state.mission and st.session_state.selected_opportunity:
    st.markdown(
        '''<div class="mission-alert">
            <div class="mission-alert-title">📋 Application Mission is ready</div>
            <div class="mission-alert-text">Your mission is ready. Next: review the details → tick <b>every checklist item</b> → tick <b>Human approval</b> → then use the <b>Start Anakin Browser Agent</b> button.</div>
            <a class="jump-link" href="#application-mission">↓ Jump to Application Mission</a>
        </div>''',
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------------
# DISCOVERY
# ------------------------------------------------------------------
if find_button:
    profile = build_profile()
    if not skills_text.strip():
        st.error("Please enter at least one skill.")
    elif not goal.strip():
        st.error("Please describe what you are looking for.")
    else:
        st.session_state.profile_snapshot = profile
        st.session_state.selected_opportunity = None
        st.session_state.mission = None
        st.session_state.approved = False
        st.session_state.browser_result = None
        st.session_state.mission_built = False
        st.session_state.current_stage = "analyze"
        with st.spinner("✦ ApplyPilot is searching the live web and reasoning about your target..."):
            try:
                st.session_state.recommendations = cached_discovery(profile)
            except Exception as exc:
                st.error(f"Agent error: {exc}")

result = st.session_state.recommendations

if result:
    profile = st.session_state.profile_snapshot or build_profile()
    recommendations = result.get("recommendations", [])
    stats = result.get("search_stats", {})

    st.markdown('<div class="section-label">SEARCH TARGET</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="search-hero"><div class="search-target">🎯 {profile.get("goal", "Internships")}</div><div class="small">{profile.get("location", "India / Remote")} · {profile.get("education", "Student")} · Skills: {", ".join(profile.get("skills", []))}</div></div>', unsafe_allow_html=True)
    st.write("")

    stat_cols = st.columns(4)
    with stat_cols[0]: st.metric("Opportunities", len(recommendations))
    with stat_cols[1]: st.metric("Live searches", stats.get("queries_used", 0))
    with stat_cols[2]: st.metric("Candidates screened", stats.get("candidates_analyzed", 0))
    with stat_cols[3]: st.metric("Search results", stats.get("raw_results", 0))

    st.markdown("## ✦ Top matches")
    st.caption("Ranked using your search target, skills, education, location, opportunity status and source quality. Official/company and reputable application sources are prioritized.")

    if not recommendations:
        st.warning(result.get("message", "No suitable current opportunities were found."))
    else:
        for index, item in enumerate(recommendations):
            score = item.get("score", 0)
            try:
                score_int = int(float(score))
            except Exception:
                score_int = 0
            status = str(item.get("status", "unknown")).lower()
            action = str(item.get("action", "PREPARE")).upper()
            company = item.get("company") or "Company not specified"
            source_label = item.get("source_label", "Web source")

            status_text = "🟢 Active" if status == "active" else "🟡 Needs verification"
            action_text = "APPLY NOW" if action == "APPLY_NOW" else "PREPARE"
            matching = item.get("matching_skills", []) or []
            missing = item.get("missing_requirements", []) or []

            with st.container():
                st.markdown('<div class="op-card">', unsafe_allow_html=True)
                left, right = st.columns([5, 1])
                with left:
                    st.markdown(f'<div class="op-rank">#{index + 1} · {action_text} · {status_text}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="op-title">{item.get("title", "Opportunity")}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="company">{company}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="small">Source: {source_label}</div>', unsafe_allow_html=True)
                    reason = item.get("reason", "")
                    if reason:
                        st.write(reason)
                    if matching:
                        st.markdown("**Matching skills**")
                        st.markdown(" ".join(f'<span class="chip">✓ {s}</span>' for s in matching), unsafe_allow_html=True)
                    if missing:
                        st.markdown("**Verify before applying**")
                        st.write(" · ".join(str(x) for x in missing[:3]))
                    if item.get("deadline"):
                        st.write(f"**Deadline:** {item.get('deadline')}")
                    if item.get("url"):
                        st.link_button("Open opportunity", item.get("url"), use_container_width=False)
                with right:
                    st.markdown(f'<div class="score">{score_int}</div><div class="score-label">match / 100</div>', unsafe_allow_html=True)
                    st.write("")
                    if action in {"APPLY_NOW", "PREPARE"} and item.get("url"):
                        if st.button("📋 Build Mission", key=f"mission_{index}", use_container_width=True):
                            st.session_state.selected_opportunity = item
                            st.session_state.approved = False
                            st.session_state.browser_result = None
                            st.session_state.current_stage = "prepare"
                            st.session_state.mission = generate_application_mission(profile, item)
                            st.session_state.mission_built = True
                            st.toast("Mission built successfully. Jumping to your application mission below.", icon="📋")
                            st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------
# MISSION
# ------------------------------------------------------------------
opportunity = st.session_state.selected_opportunity
mission = st.session_state.mission

if opportunity and mission:
    st.markdown('<div id="application-mission"></div>', unsafe_allow_html=True)
    st.divider()
    st.markdown("## 📋 Application Mission")
    display_name = profile.get("name") or "Candidate"
    st.markdown(f'<div class="mission-box"><b>Prepared for {display_name}</b><br><span class="muted">ApplyPilot converted the selected opportunity into a personalized, human-reviewable mission.</span></div>', unsafe_allow_html=True)
    st.write("")
    st.success("✓ Mission built successfully — review the preparation below before authorizing the browser agent.")

    mc = st.columns(3)
    with mc[0]: st.metric("Match", f"{opportunity.get('score', 0)}/100")
    with mc[1]: st.metric("Eligibility", str(opportunity.get("eligibility", "unknown")).upper())
    with mc[2]: st.metric("Recommendation", opportunity.get("action", "PREPARE"))

    st.markdown(f"### {opportunity.get('title', 'Opportunity')}")
    st.markdown("#### 🧠 Why this matches you")
    st.info(mission.get("match_summary", "No assessment available."))

    st.markdown("#### 📄 Resume preparation")
    for suggestion in mission.get("resume_suggestions", []) or []:
        st.markdown(f"✓ {suggestion}")

    st.markdown("#### ✍️ Personalized cover letter")
    # Always generate the visible cover letter from the CURRENT user's profile.
    candidate_name = (profile.get("name") or "Candidate").strip()
    cover_letter = build_personalized_cover_letter(profile, opportunity)
    st.text_area("Review and edit before using", value=cover_letter, height=260, key="cover_letter_preview")
    st.caption(f"✍️ Personalized for {candidate_name} using the education, skills, search target and location entered in this session.")

    st.markdown("#### ✅ Mission checklist")
    checklist_items = mission.get("checklist", []) or []
    st.info(f"☑️ Step 1 of 2: Review and tick all {len(checklist_items)} checklist item(s) below. Then complete the Human approval checkbox. The browser agent unlocks only after both are complete.")
    checklist_complete = True
    for index, task in enumerate(checklist_items):
        checked = st.checkbox(task, key=f"mission_check_{index}")
        if not checked:
            checklist_complete = False

    if opportunity.get("url"):
        st.link_button("🌐 Open official opportunity", opportunity.get("url"), use_container_width=True)

    st.markdown("#### 🛡️ Human approval")
    st.warning("Approve only after reviewing the opportunity and preparation. ApplyPilot will navigate the live page but will never submit the final application automatically.")
    approval = st.checkbox("I reviewed this opportunity and authorize ApplyPilot to continue.", key="approval_checkbox")
    if not checklist_complete:
        st.caption("🔒 Step 2 is locked until every mission checklist item above is ticked.")
    elif not approval:
        st.info("☑️ **Step 2 of 2:** The mission checklist is complete. Tick the Human approval box above to unlock the agent start button.")
    else:
        st.success("✓ **Ready:** Checklist complete + Human approval complete.")
        if st.button("🚀 Start Anakin Browser Agent", type="primary", use_container_width=True):
            st.session_state.approved = True
            st.session_state.current_stage = "act"
            st.session_state.browser_result = None
            st.rerun()

# ------------------------------------------------------------------
# ACTION CENTER
# ------------------------------------------------------------------
application_url = opportunity.get("url") if opportunity else None
if st.session_state.approved and opportunity and application_url:
    st.divider()
    st.markdown("## 🤖 Agent Action Center")
    st.markdown('<div class="action-box"><b>ApplyPilot is acting on your behalf</b><br><span class="muted">Open → Read → Understand → Inspect → Stop before final submission.</span></div>', unsafe_allow_html=True)
    st.write("")

    result = st.session_state.browser_result
    if result is None:
        cols = st.columns(5)
        plan = [("01", "🌐", "OPEN"), ("02", "🔎", "READ"), ("03", "🧠", "UNDERSTAND"), ("04", "📝", "INSPECT"), ("05", "🛡️", "HUMAN REVIEW")]
        for col, (n, icon, title) in zip(cols, plan):
            with col:
                st.markdown(f'<div class="stage"><div class="stage-num">STEP {n}</div><div class="stage-title">{icon} {title}</div></div>', unsafe_allow_html=True)
        st.write("")
        st.info("🚀 **Final step:** Click the button below to let Anakin open and inspect the live opportunity. ApplyPilot will stop before final submission.")
        if st.button("🌐 Start Anakin Browser Agent", type="primary", use_container_width=True):
            with st.spinner("🤖 Anakin is inspecting the live opportunity..."):
                try:
                    st.session_state.browser_result = inspect_and_open_application(application_url)
                    st.session_state.current_stage = "review"
                    st.rerun()
                except Exception as exc:
                    st.error("Anakin could not complete the browser step.")
                    st.warning("The site may block automation or require verification. Do not repeatedly retry the same page.")
                    with st.expander("Technical details"):
                        st.code(str(exc), language="text")

    result = st.session_state.browser_result
    if result:
        if result.get("success"):
            st.markdown("### ✅ Agent execution complete")
            warning = result.get("navigation_warning")
            if warning:
                st.warning(warning)

            apply_found = bool(result.get("apply_control_found"))
            app_opened = bool(result.get("application_page_opened"))
            real_form = bool(result.get("real_application_form"))
            fields = result.get("form_fields", []) or []
            agent_status = result.get("agent_status", "BLOCKED")
            verification = bool(result.get("verification_detected"))

            steps = [
                ("Open live opportunity", True),
                ("Read page content", True),
                ("Find application control", apply_found),
                ("Open application destination", app_opened),
                ("Verify application form", real_form),
            ]
            st.markdown("#### 🧭 Agent trace")
            for label, done in steps:
                st.markdown(f'<div class="field-row">{"✓" if done else "○"} <b>{label}</b>{"" if done else " <span class=\"muted\">not reached</span>"}</div>', unsafe_allow_html=True)
            st.markdown('<div class="field-row">🛡️ <b>Final submission</b> <span class="muted">blocked — human controlled</span></div>', unsafe_allow_html=True)

            status_map = {
                "APPLICATION_READY": ("🟢", "APPLICATION READY", "A genuine application workflow and relevant fields were detected.", "status-ready"),
                "APPLICATION_PAGE_OPENED": ("🔵", "APPLICATION PAGE OPENED", "The destination was reached, but a genuine application form was not confirmed.", "status-info"),
                "APPLICATION_CONTROL_FOUND": ("🟡", "APPLY CONTROL FOUND", "An Apply control was found, but its destination was not reached.", "status-warn"),
                "VERIFICATION_BLOCKED": ("🟠", "VERIFICATION BLOCKED", "The live destination requires anti-bot/security verification before the application can be inspected.", "status-warn"),
                "OPPORTUNITY_ONLY": ("🟠", "OPPORTUNITY ONLY", "The page was readable, but no application workflow was reached.", "status-warn"),
                "BLOCKED": ("🔴", "PAGE BLOCKED", "The page could not be inspected reliably.", "status-danger"),
            }
            icon, title, desc, css = status_map.get(agent_status, ("⚪", agent_status.replace("_", " "), "Inspection completed.", "status-info"))
            st.markdown(f'<div class="action-box {css}"><b style="font-size:1.2rem">{icon} {title}</b><br><span class="muted">{desc}</span></div>', unsafe_allow_html=True)
            st.write("")

            metrics = st.columns(3)
            with metrics[0]: st.metric("Apply control", "FOUND" if apply_found else "NOT FOUND")
            with metrics[1]: st.metric("Destination", "REACHED" if app_opened else "NOT REACHED")
            with metrics[2]: st.metric("Application fields", len(fields) if real_form else 0)

            if verification:
                st.warning(result.get("verification_reason") or "The destination requires verification.")
            elif real_form:
                st.success("Application workflow verified. Review the live page before any consequential action.")
            elif app_opened:
                st.info("Application destination reached, but ApplyPilot could not confidently verify a real form. Generic newsletter/search/comment fields are excluded.")
            elif apply_found:
                st.warning("Apply control found, but the destination could not be reached safely.")

            st.markdown("### 🔎 Application inspection")
            if real_form:
                field_cols = st.columns(2)
                for i, field in enumerate(fields[:20]):
                    label = field.get("label") or field.get("placeholder") or field.get("name") or field.get("id") or "Application field"
                    with field_cols[i % 2]:
                        st.markdown(f'<div class="field-row">✓ <b>{label}</b> <span class="muted">({field.get("type", "field")})</span></div>', unsafe_allow_html=True)
            else:
                st.info("No genuine application fields were confirmed. Newsletter, search, comment and contact fields are intentionally excluded.")

            st.markdown("### 🌐 Browser evidence")
            live_url = result.get("url") or application_url
            st.write(f"**Inspected page:** {result.get('title') or 'Live page'}")
            if live_url:
                st.link_button("Open inspected page", live_url, use_container_width=True)
            screenshot = result.get("screenshot")
            if screenshot:
                st.image(screenshot, caption="Live page state inspected by Anakin Browser", use_container_width=True)
            else:
                st.info("No browser screenshot was returned.")

            st.divider()
            st.markdown("### 🛡️ Final Review")
            if verification:
                st.warning("ApplyPilot reached the live destination but encountered an anti-bot/security verification step. Nothing was submitted.")
            elif real_form:
                st.success("ApplyPilot reached and verified an application workflow. Final submission remains under human control.")
            elif app_opened:
                st.info("ApplyPilot reached the application destination, but form verification is incomplete. Review the live page manually.")
            elif apply_found:
                st.warning("ApplyPilot found an Apply control but did not reach its destination. Nothing was submitted.")
            else:
                st.warning("ApplyPilot inspected the opportunity but did not reach an application workflow. Nothing was submitted.")
            st.markdown("**Submission:** 🛑 Blocked by design — ApplyPilot never submits the final application automatically.")
        else:
            st.error("⚠️ ApplyPilot could not reliably inspect this page.")
            if result.get("navigation_warning"):
                st.warning(result.get("navigation_warning"))
            if result.get("error"):
                st.code(result.get("error"), language="text")
            if result.get("screenshot"):
                st.image(result.get("screenshot"), caption="Live page state reached by Anakin Browser", use_container_width=True)

# ------------------------------------------------------------------
# WELCOME
# ------------------------------------------------------------------
if st.session_state.recommendations is None and not opportunity:
    st.write("")
    st.markdown("## 👋 Welcome to your career mission")
    st.write("Tell ApplyPilot exactly what you want. The search target drives discovery, while your skills, education and location drive ranking.")
    wc = st.columns(3)
    cards = [
        ("🔎", "Discover", "Search the live web using your actual role and opportunity requirements."),
        ("🧠", "Reason", "Rank opportunities by fit, eligibility, freshness and source quality."),
        ("🤖", "Act safely", "Navigate live pages after approval, then stop before consequential submission."),
    ]
    for col, (icon, title, desc) in zip(wc, cards):
        with col:
            st.markdown(f'<div class="stat-card"><div style="font-size:1.5rem">{icon}</div><b>{title}</b><div class="small">{desc}</div></div>', unsafe_allow_html=True)
