# ============================================================
# EDUPRO - LEARNER DEMOGRAPHICS & COURSE ENROLLMENT ANALYTICS
# FINAL STREAMLIT DASHBOARD - STABLE VERSION
# ============================================================

import os
import io
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
# ============================================================
# EDU PRO — PREMIUM PLOTLY THEME
# ============================================================

def apply_premium_theme(fig, height=430, kind=None):
    """Apply a Plotly-safe premium theme to every dashboard chart.

    Important: Plotly colorbar titles use `title=dict(font=...)`;
    `titlefont` is not a valid ColorBar property in current Plotly.
    """
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.42)",
        colorway=["#6366F1", "#8B5CF6", "#06B6D4", "#22C55E", "#F59E0B", "#F43F5E"],
        font=dict(family="Inter, Arial, sans-serif", color="#E2E8F0", size=13),
        title=dict(font=dict(size=19, color="#F8FAFC"), x=0.02, xanchor="left"),
        margin=dict(l=55, r=30, t=65, b=55),
        hoverlabel=dict(bgcolor="#111827", bordercolor="#6366F1", font=dict(color="#F8FAFC", size=13)),
        xaxis=dict(showgrid=False, zeroline=False, linecolor="rgba(148,163,184,0.18)", tickfont=dict(color="#94A3B8")),
        yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.10)", zeroline=False, linecolor="rgba(148,163,184,0.12)", tickfont=dict(color="#94A3B8")),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#CBD5E1")),
    )

    # Heatmap-specific styling. This is Plotly-version safe.
    if kind == "heatmap" or any(trace.type == "heatmap" for trace in fig.data):
        fig.update_coloraxes(
            colorscale=[
                [0.00, "#0B1020"],
                [0.20, "#1E1B4B"],
                [0.45, "#3730A3"],
                [0.70, "#6366F1"],
                [0.88, "#8B5CF6"],
                [1.00, "#06B6D4"],
            ],
            colorbar=dict(
                thickness=12,
                outlinewidth=0,
                tickfont=dict(color="#CBD5E1", size=11),
                title=dict(font=dict(color="#E2E8F0", size=12)),
            ),
        )

        for trace in fig.data:
            if trace.type == "heatmap":
                trace.update(
                    hovertemplate="<b>%{x}</b> × <b>%{y}</b><br>Enrollments: %{z:,}<extra></extra>"
                )

    # Bar styling
    if any(trace.type == "bar" for trace in fig.data):
        for trace in fig.data:
            if trace.type == "bar":
                trace.update(
                    marker=dict(
                        line=dict(color="rgba(255,255,255,0.16)", width=1),
                    ),
                    hoverlabel=dict(bgcolor="#111827"),
                )

    # Pie / donut styling
    if any(trace.type == "pie" for trace in fig.data):
        fig.update_traces(
            marker=dict(line=dict(color="#0B1020", width=2)),
            textfont=dict(color="#F8FAFC", size=12),
            hovertemplate="<b>%{label}</b><br>Value: %{value:,}<br>Share: %{percent}<extra></extra>",
        )

    # Line styling
    if any(trace.type == "scatter" for trace in fig.data):
        for trace in fig.data:
            if trace.type == "scatter" and trace.mode and "lines" in trace.mode:
                trace.update(line=dict(width=3), marker=dict(size=7))

    return fig


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EduPro | Learner Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# GLOBAL CSS
# ONLY CSS - NO HTML COMPONENTS
# ============================================================

st.markdown(
    """
<style>
:root {
    --ep-bg:#070b17; --ep-indigo:#6366f1; --ep-violet:#8b5cf6;
    --ep-cyan:#06b6d4; --ep-text:#f8fafc; --ep-muted:#94a3b8;
}

/* ===== APP BACKGROUND ===== */
.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(99,102,241,.16), transparent 28%),
        radial-gradient(circle at 90% 5%, rgba(6,182,212,.10), transparent 24%),
        radial-gradient(circle at 50% 100%, rgba(139,92,246,.08), transparent 32%),
        var(--ep-bg) !important;
    color:var(--ep-text) !important;
}
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main { background:transparent !important; }
[data-testid="stHeader"] {
    background:rgba(7,11,23,.72) !important;
    backdrop-filter:blur(14px);
}
.block-container {
    max-width:1540px !important;
    padding:2.2rem 2.2rem 3rem !important;
}

/* ===== TYPOGRAPHY ===== */
h1,h2,h3,h4,h5,h6 { color:#f8fafc !important; letter-spacing:-.02em; }
h1 { font-size:clamp(2rem,3vw,3rem) !important; font-weight:800 !important; }
h2 { font-size:1.65rem !important; font-weight:750 !important; }
h3 { font-size:1.15rem !important; font-weight:700 !important; }
p,li,label { color:#cbd5e1 !important; }
[data-testid="stCaptionContainer"] { color:#94a3b8 !important; }

/* ===== KPI CARDS ===== */
[data-testid="stMetric"] {
    position:relative; overflow:hidden; min-height:118px;
    padding:20px 22px !important;
    border:1px solid rgba(148,163,184,.15) !important;
    border-radius:20px !important;
    background:linear-gradient(145deg,rgba(30,41,59,.96),rgba(9,14,29,.96)) !important;
    box-shadow:0 18px 45px rgba(0,0,0,.28),inset 0 1px 0 rgba(255,255,255,.045) !important;
    transition:transform .22s ease,box-shadow .22s ease,border-color .22s ease;
}
[data-testid="stMetric"]::before {
    content:""; position:absolute; width:110px; height:110px; right:-55px; top:-55px;
    border-radius:50%; background:rgba(99,102,241,.16);
}
[data-testid="stMetric"]:hover {
    transform:translateY(-4px);
    border-color:rgba(99,102,241,.42) !important;
    box-shadow:0 24px 55px rgba(0,0,0,.34),0 0 28px rgba(99,102,241,.10) !important;
}
[data-testid="stMetricLabel"] {
    color:#94a3b8 !important; font-size:.82rem !important;
    font-weight:650 !important; text-transform:uppercase; letter-spacing:.07em;
}
[data-testid="stMetricValue"] {
    color:#fff !important; font-size:clamp(1.7rem,2.4vw,2.35rem) !important;
    font-weight:800 !important; letter-spacing:-.04em;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#0a1020 0%,#080d1a 55%,#070b15 100%) !important;
    border-right:1px solid rgba(148,163,184,.13);
}
section[data-testid="stSidebar"] > div { background:transparent !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color:#f8fafc !important; }
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:#94a3b8 !important; }

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background:rgba(15,23,42,.88) !important;
    border:1px solid rgba(148,163,184,.18) !important;
    border-radius:13px !important; min-height:46px;
    box-shadow:inset 0 1px 0 rgba(255,255,255,.025);
}
section[data-testid="stSidebar"] div[data-baseweb="select"] > div:hover {
    border-color:rgba(99,102,241,.55) !important;
}
section[data-testid="stSidebar"] [data-baseweb="tag"] {
    background:linear-gradient(135deg,#6366f1,#8b5cf6) !important;
    border:0 !important; border-radius:8px !important; color:#fff !important;
}
section[data-testid="stSidebar"] [data-baseweb="tag"] span { color:#fff !important; }

[data-baseweb="popover"] { z-index:999999 !important; }
[data-baseweb="popover"] [role="listbox"] {
    background:#111827 !important; border:1px solid rgba(148,163,184,.18) !important;
    border-radius:14px !important; box-shadow:0 24px 70px rgba(0,0,0,.45) !important;
}
[data-baseweb="popover"] [role="option"] { color:#e2e8f0 !important; }
[data-baseweb="popover"] [role="option"]:hover { background:rgba(99,102,241,.16) !important; }

/* ===== TABS ===== */
.stTabs [data-baseweb="tab-list"] {
    gap:6px; padding:7px; border-radius:16px;
    background:rgba(15,23,42,.72);
    border:1px solid rgba(148,163,184,.13);
    box-shadow:inset 0 1px 0 rgba(255,255,255,.025);
    overflow-x:auto;
}
.stTabs [data-baseweb="tab"] {
    height:42px; padding:8px 14px; border-radius:11px;
    color:#94a3b8 !important; background:transparent;
    font-weight:650; border:1px solid transparent; white-space:nowrap;
    transition:all .2s ease;
}
.stTabs [data-baseweb="tab"]:hover { color:#fff !important; background:rgba(99,102,241,.10); }
.stTabs [aria-selected="true"] {
    color:#fff !important;
    background:linear-gradient(135deg,#4f46e5,#7c3aed) !important;
    border-color:rgba(255,255,255,.12) !important;
    box-shadow:0 8px 24px rgba(79,70,229,.25);
}

/* ===== CHART CARDS ===== */
[data-testid="stPlotlyChart"] {
    padding:7px; border-radius:20px;
    background:linear-gradient(145deg,rgba(15,23,42,.78),rgba(9,14,28,.70));
    border:1px solid rgba(148,163,184,.12);
    box-shadow:0 16px 40px rgba(0,0,0,.20),inset 0 1px 0 rgba(255,255,255,.025);
    transition:transform .22s ease,border-color .22s ease;
}
[data-testid="stPlotlyChart"]:hover {
    transform:translateY(-2px); border-color:rgba(99,102,241,.25);
}

/* ===== TABLES ===== */
[data-testid="stDataFrame"] {
    border:1px solid rgba(148,163,184,.14) !important;
    border-radius:16px !important; overflow:hidden !important;
    box-shadow:0 16px 38px rgba(0,0,0,.18);
}

/* ===== BUTTONS ===== */
.stButton > button,.stDownloadButton > button {
    border:1px solid rgba(99,102,241,.35) !important;
    border-radius:12px !important;
    background:linear-gradient(135deg,#4f46e5,#7c3aed) !important;
    color:#fff !important; font-weight:700 !important;
    box-shadow:0 9px 25px rgba(79,70,229,.20);
    transition:all .2s ease;
}
.stButton > button:hover,.stDownloadButton > button:hover {
    transform:translateY(-2px); box-shadow:0 13px 32px rgba(79,70,229,.30);
}

/* ===== ALERTS / DIVIDERS ===== */
div[data-testid="stAlert"] {
    border-radius:15px !important;
    border:1px solid rgba(148,163,184,.14) !important;
    background:rgba(15,23,42,.72) !important;
}
hr { border-color:rgba(148,163,184,.12) !important; margin:1.3rem 0 !important; }

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar { width:9px; height:9px; }
::-webkit-scrollbar-track { background:#070b15; }
::-webkit-scrollbar-thumb {
    background:linear-gradient(#4f46e5,#7c3aed); border-radius:99px;
}

/* ===== EXECUTIVE INSIGHT CARDS ===== */
.ep-insight-grid {
    display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:14px; margin:18px 0 24px;
}
.ep-insight {
    position:relative; overflow:hidden; padding:18px 18px 17px; border-radius:18px;
    background:linear-gradient(145deg,rgba(17,24,39,.92),rgba(8,13,27,.94));
    border:1px solid rgba(148,163,184,.13); box-shadow:0 14px 35px rgba(0,0,0,.18);
}
.ep-insight:after {
    content:""; position:absolute; width:90px; height:90px; right:-35px; top:-40px;
    border-radius:50%; background:rgba(99,102,241,.12);
}
.ep-insight-kicker {font-size:10px; text-transform:uppercase; letter-spacing:.12em; color:#818cf8; font-weight:800;}
.ep-insight-value {font-size:20px; font-weight:800; color:#f8fafc; margin-top:7px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
.ep-insight-detail {font-size:12px; color:#94a3b8; margin-top:5px; line-height:1.45;}
.ep-section-label {
    display:flex; align-items:center; gap:9px; margin:26px 0 12px;
    color:#a5b4fc; font-size:11px; font-weight:800; letter-spacing:.14em; text-transform:uppercase;
}
.ep-section-label:before {content:""; width:24px; height:2px; border-radius:9px; background:linear-gradient(90deg,#6366f1,#06b6d4);}
@media (max-width:1100px) {.ep-insight-grid {grid-template-columns:repeat(2,minmax(0,1fr));}}
@media (max-width:600px) {.ep-insight-grid {grid-template-columns:1fr;}}


/* ===== FILTER SUMMARY + AUTO INSIGHTS ===== */
.ep-filter-summary {
    display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin:4px 0 18px;
    padding:10px 12px; border-radius:14px;
    background:rgba(15,23,42,.62); border:1px solid rgba(148,163,184,.12);
}
.ep-filter-label {font-size:10px; text-transform:uppercase; letter-spacing:.12em; color:#64748b; font-weight:800; margin-right:3px;}
.ep-filter-chip {padding:6px 10px; border-radius:999px; background:rgba(99,102,241,.12); color:#c7d2fe; border:1px solid rgba(99,102,241,.18); font-size:11px; font-weight:700;}
.ep-auto-grid {display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:14px; margin:0 0 24px;}
.ep-auto-card {padding:17px 18px; border-radius:18px; background:linear-gradient(145deg,rgba(17,24,39,.9),rgba(8,13,27,.95)); border:1px solid rgba(148,163,184,.12); box-shadow:0 14px 35px rgba(0,0,0,.16);}
.ep-auto-title {font-size:10px; text-transform:uppercase; letter-spacing:.12em; color:#67e8f9; font-weight:800;}
.ep-auto-text {margin-top:7px; color:#e2e8f0; font-size:13px; line-height:1.55;}
.ep-auto-text strong {color:#fff;}
@media (max-width:1100px){ .ep-context-grid{grid-template-columns:repeat(2,minmax(0,1fr));} }
@media (max-width:900px){ .ep-insight-grid,.ep-auto-grid,.ep-context-grid{grid-template-columns:1fr;} }

/* ===== ANALYTICAL CONTEXT ===== */
.ep-context-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; margin:8px 0 24px; }
.ep-context-card { display:flex; gap:12px; align-items:flex-start; padding:16px; border-radius:17px; background:linear-gradient(145deg,rgba(15,23,42,.86),rgba(8,13,27,.94)); border:1px solid rgba(148,163,184,.12); box-shadow:0 14px 32px rgba(0,0,0,.16), inset 0 1px 0 rgba(255,255,255,.025); }
.ep-context-icon { width:34px; height:34px; flex:0 0 34px; display:flex; align-items:center; justify-content:center; border-radius:11px; background:rgba(99,102,241,.13); border:1px solid rgba(99,102,241,.20); color:#c4b5fd; font-weight:800; }
.ep-context-title { color:#94a3b8; font-size:10px; text-transform:uppercase; letter-spacing:.10em; font-weight:800; }
.ep-context-value { color:#f8fafc; font-size:1.02rem; line-height:1.25; font-weight:800; margin-top:5px; }
.ep-context-detail { color:#64748b; font-size:11px; line-height:1.4; margin-top:5px; }

/* ===== MOBILE ===== */
@media (max-width:900px) {
    .block-container { padding-left:1rem !important; padding-right:1rem !important; }
    [data-testid="stMetric"] { min-height:100px; padding:16px !important; }
    .stTabs [data-baseweb="tab"] { padding:7px 10px; font-size:.82rem; }
}
</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# CONSTANTS
# ============================================================

DATA_FILE = os.path.join("data", "EduPro.xlsx")
REPORT_DIR = os.path.join("outputs", "reports")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_text(series):
    return (
        series
        .astype(str)
        .str.strip()
        .replace("nan", np.nan)
    )


def create_age_group(age):

    if pd.isna(age):
        return "Unknown"

    if age < 18:
        return "<18"

    elif age <= 25:
        return "18–25"

    elif age <= 35:
        return "26–35"

    elif age <= 45:
        return "36–45"

    else:
        return "45+"


def safe_divide(a, b):

    if b == 0:
        return 0

    return a / b


# ============================================================
# LOAD EXCEL DATA
# ============================================================

@st.cache_data
def load_data():

    if not os.path.exists(DATA_FILE):

        return None, None, None, None

    users = pd.read_excel(
        DATA_FILE,
        sheet_name="Users"
    )

    teachers = pd.read_excel(
        DATA_FILE,
        sheet_name="Teachers"
    )

    courses = pd.read_excel(
        DATA_FILE,
        sheet_name="Courses"
    )

    transactions = pd.read_excel(
        DATA_FILE,
        sheet_name="Transactions"
    )

    return users, teachers, courses, transactions


# ============================================================
# BUILD MASTER DATASET
# ============================================================

@st.cache_data
def build_master(users, courses, transactions):

    users = users.copy()
    courses = courses.copy()
    transactions = transactions.copy()

    # -------------------------
    # Clean Users
    # -------------------------

    users["UserID"] = users["UserID"].astype(str).str.strip()

    users["Age"] = pd.to_numeric(
        users["Age"],
        errors="coerce"
    )

    users["Gender"] = clean_text(
        users["Gender"]
    )

    # -------------------------
    # Clean Transactions
    # -------------------------

    transactions["UserID"] = (
        transactions["UserID"]
        .astype(str)
        .str.strip()
    )

    transactions["CourseID"] = (
        transactions["CourseID"]
        .astype(str)
        .str.strip()
    )

    transactions["TransactionDate"] = pd.to_datetime(
        transactions["TransactionDate"],
        errors="coerce"
    )

    transactions["Amount"] = pd.to_numeric(
        transactions["Amount"],
        errors="coerce"
    )

    # -------------------------
    # Clean Courses
    # -------------------------

    courses["CourseID"] = (
        courses["CourseID"]
        .astype(str)
        .str.strip()
    )

    courses["CourseCategory"] = clean_text(
        courses["CourseCategory"]
    )

    courses["CourseType"] = clean_text(
        courses["CourseType"]
    )

    courses["CourseLevel"] = clean_text(
        courses["CourseLevel"]
    )

    courses["CourseName"] = clean_text(
        courses["CourseName"]
    )

    courses["CoursePrice"] = pd.to_numeric(
        courses["CoursePrice"],
        errors="coerce"
    )

    courses["CourseRating"] = pd.to_numeric(
        courses["CourseRating"],
        errors="coerce"
    )

    # -------------------------
    # Merge Transactions + Users
    # -------------------------

    master = transactions.merge(
        users[
            [
                "UserID",
                "UserName",
                "Age",
                "Gender"
            ]
        ],
        on="UserID",
        how="left"
    )

    # -------------------------
    # Merge Courses
    # -------------------------

    master = master.merge(
        courses[
            [
                "CourseID",
                "CourseName",
                "CourseCategory",
                "CourseType",
                "CourseLevel",
                "CoursePrice",
                "CourseRating",
                "CourseDuration"
            ]
        ],
        on="CourseID",
        how="left"
    )

    # -------------------------
    # Age Groups
    # -------------------------

    master["AgeGroup"] = master["Age"].apply(
        create_age_group
    )

    # -------------------------
    # Date Features
    # -------------------------

    master["Year"] = (
        master["TransactionDate"]
        .dt.year
    )

    master["Month"] = (
        master["TransactionDate"]
        .dt.month
    )

    master["YearMonth"] = (
        master["TransactionDate"]
        .dt.to_period("M")
        .astype(str)
    )

    return master


# ============================================================
# LOAD DATA
# ============================================================

users, teachers, courses, transactions = load_data()


# ============================================================
# DATA FILE ERROR
# ============================================================

if users is None:

    st.error(
        "EduPro.xlsx was not found."
    )

    st.info(
        "Please keep the Excel file here:"
    )

    st.code(
        "data/EduPro.xlsx"
    )

    st.stop()


# ============================================================
# BUILD MASTER
# ============================================================

master = build_master(
    users,
    courses,
    transactions
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div style="
        padding:24px 28px; margin-bottom:22px; border-radius:22px;
        background:
            radial-gradient(circle at 92% 20%,rgba(6,182,212,.16),transparent 24%),
            linear-gradient(135deg,rgba(30,41,59,.92),rgba(9,14,29,.94));
        border:1px solid rgba(148,163,184,.14);
        box-shadow:0 22px 55px rgba(0,0,0,.24),inset 0 1px 0 rgba(255,255,255,.04);
    ">
        <div style="font-size:12px;font-weight:800;letter-spacing:.16em;
                    color:#818cf8;text-transform:uppercase;margin-bottom:8px;">
            EDU PRO • LEARNER ANALYTICS
        </div>
        <div style="font-size:32px;line-height:1.15;font-weight:850;
                    color:#f8fafc;letter-spacing:-.035em;">
            Learner Intelligence Dashboard
        </div>
        <div style="margin-top:9px;font-size:14px;color:#94a3b8;">
            Learner demographics · course preferences · engagement · enrollment behavior
        </div>
        <div style="margin-top:16px;display:flex;flex-wrap:wrap;gap:8px;">
            <span style="padding:6px 10px;border-radius:999px;background:rgba(99,102,241,.14);
                         color:#a5b4fc;font-size:11px;font-weight:700;">DESCRIPTIVE ANALYTICS</span>
            <span style="padding:6px 10px;border-radius:999px;background:rgba(6,182,212,.12);
                         color:#67e8f9;font-size:11px;font-weight:700;">INTERACTIVE DASHBOARD</span>
            <span style="padding:6px 10px;border-radius:999px;background:rgba(16,185,129,.12);
                         color:#6ee7b7;font-size:11px;font-weight:700;">RESEARCH PROJECT</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "🎛️ Dashboard Filters"
)

st.sidebar.caption(
    "Use filters to explore learner behavior."
)

presentation_mode = st.sidebar.toggle(
    "🎤 Presentation Mode",
    value=False,
    help="Show a concise executive view suitable for presentations, viva, and research demonstrations."
)

# Portfolio / publication resources
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔗 Project Resources")
st.sidebar.markdown(
    "[GitHub Repository](https://github.com/anandrajyadav/EduPro-Learner-Analytics)"
)
st.sidebar.markdown(
    "[Research DOI — Zenodo](https://doi.org/10.5281/zenodo.22816169)"
)
st.sidebar.caption("Public research record • Descriptive analytics • SDG 4 context")


# Filter state + reset
filter_defaults = {
    "age": sorted(master["AgeGroup"].dropna().unique().tolist()),
    "gender": sorted(master["Gender"].dropna().unique().tolist()),
    "category": sorted(master["CourseCategory"].dropna().unique().tolist()),
    "level": sorted(master["CourseLevel"].dropna().unique().tolist()),
    "type": sorted(master["CourseType"].dropna().unique().tolist()),
}

for _key, _value in filter_defaults.items():
    if _key not in st.session_state:
        st.session_state[_key] = _value.copy()

if st.sidebar.button("↺ Reset All Filters", use_container_width=True):
    for _key, _value in filter_defaults.items():
        st.session_state[_key] = _value.copy()
    st.rerun()

# Age Group
age_options = sorted(
    master["AgeGroup"]
    .dropna()
    .unique()
    .tolist()
)

selected_age = st.sidebar.multiselect(
    "Age Group",
    age_options,
    key="age"
)


# Gender
gender_options = sorted(
    master["Gender"]
    .dropna()
    .unique()
    .tolist()
)

selected_gender = st.sidebar.multiselect(
    "Gender",
    gender_options,
    key="gender"
)


# Category
category_options = sorted(
    master["CourseCategory"]
    .dropna()
    .unique()
    .tolist()
)

selected_category = st.sidebar.multiselect(
    "Course Category",
    category_options,
    key="category"
)


# Course Level
level_options = sorted(
    master["CourseLevel"]
    .dropna()
    .unique()
    .tolist()
)

selected_level = st.sidebar.multiselect(
    "Course Level",
    level_options,
    key="level"
)


# Course Type
type_options = sorted(
    master["CourseType"]
    .dropna()
    .unique()
    .tolist()
)

selected_type = st.sidebar.multiselect(
    "Course Type",
    type_options,
    key="type"
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered = master[
    master["AgeGroup"].isin(selected_age)
    &
    master["Gender"].isin(selected_gender)
    &
    master["CourseCategory"].isin(selected_category)
    &
    master["CourseLevel"].isin(selected_level)
    &
    master["CourseType"].isin(selected_type)
].copy()


# ============================================================
# EMPTY FILTER WARNING
# ============================================================

if filtered.empty:

    st.warning(
        "No records match the selected filters."
    )

    st.stop()


# ============================================================
# ACTIVE FILTER SUMMARY
# ============================================================

def _chip_value(values):
    if not values:
        return "All"
    if len(values) <= 2:
        return ", ".join(map(str, values))
    return f"{len(values)} selected"

filter_summary_html = f"""
<div class=\"ep-filter-summary\">
    <span class=\"ep-filter-label\">Active filters</span>
    <span class=\"ep-filter-chip\">Age: {_chip_value(selected_age)}</span>
    <span class=\"ep-filter-chip\">Gender: {_chip_value(selected_gender)}</span>
    <span class=\"ep-filter-chip\">Category: {_chip_value(selected_category)}</span>
    <span class=\"ep-filter-chip\">Level: {_chip_value(selected_level)}</span>
    <span class=\"ep-filter-chip\">Type: {_chip_value(selected_type)}</span>
</div>
"""
st.markdown(filter_summary_html, unsafe_allow_html=True)


# ============================================================
# ACTIVE FILTER SUMMARY
# ============================================================

def _chip_value(values):
    if not values:
        return "All"
    if len(values) <= 2:
        return ", ".join(map(str, values))
    return f"{len(values)} selected"

st.markdown(
    f"""
    <div class=\"ep-filter-summary\">
        <span class=\"ep-filter-label\">Active filters</span>
        <span class=\"ep-filter-chip\">Age: {_chip_value(selected_age)}</span>
        <span class=\"ep-filter-chip\">Gender: {_chip_value(selected_gender)}</span>
        <span class=\"ep-filter-chip\">Category: {_chip_value(selected_category)}</span>
        <span class=\"ep-filter-chip\">Level: {_chip_value(selected_level)}</span>
        <span class=\"ep-filter-chip\">Type: {_chip_value(selected_type)}</span>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_enrollments = len(filtered)

unique_learners = (
    filtered["UserID"]
    .nunique()
)

unique_courses = (
    filtered["CourseID"]
    .nunique()
)

average_enrollment = safe_divide(
    total_enrollments,
    unique_learners
)

average_age = filtered["Age"].mean()


# ============================================================
# KPI ROW
# ============================================================

k1, k2, k3, k4, k5 = st.columns(5)

with k1:

    st.metric(
        "Total Enrollments",
        f"{total_enrollments:,}"
    )

with k2:

    st.metric(
        "Unique Learners",
        f"{unique_learners:,}"
    )

with k3:

    st.metric(
        "Courses",
        f"{unique_courses:,}"
    )

with k4:

    st.metric(
        "Avg Enrollments / Learner",
        f"{average_enrollment:.2f}"
    )

with k5:

    st.metric(
        "Average Age",
        f"{average_age:.1f}"
    )

# ============================================================
# EXECUTIVE INSIGHT STRIP
# ============================================================

age_order = ["<18", "18–25", "26–35", "36–45", "45+"]
age_summary = filtered.groupby("AgeGroup").size().reindex(age_order).fillna(0)
top_age = age_summary.idxmax() if age_summary.sum() else "—"
top_age_count = int(age_summary.max()) if age_summary.sum() else 0

category_summary = filtered.groupby("CourseCategory").size().sort_values(ascending=False)
top_category = category_summary.index[0] if not category_summary.empty else "—"
top_category_count = int(category_summary.iloc[0]) if not category_summary.empty else 0

level_summary = filtered.groupby("CourseLevel").size().sort_values(ascending=False)
top_level = level_summary.index[0] if not level_summary.empty else "—"
top_level_count = int(level_summary.iloc[0]) if not level_summary.empty else 0

gender_summary = filtered.groupby("Gender").size().sort_values(ascending=False)
top_gender = gender_summary.index[0] if not gender_summary.empty else "—"
top_gender_share = (gender_summary.iloc[0] / total_enrollments * 100) if not gender_summary.empty and total_enrollments else 0

st.markdown(
    f"""
    <div class=\"ep-section-label\">Executive Snapshot</div>
    <div class=\"ep-insight-grid\">
        <div class=\"ep-insight\">
            <div class=\"ep-insight-kicker\">Most Active Age Group</div>
            <div class=\"ep-insight-value\">{top_age}</div>
            <div class=\"ep-insight-detail\">{top_age_count:,} enrollments in the filtered view</div>
        </div>
        <div class=\"ep-insight\">
            <div class=\"ep-insight-kicker\">Leading Category</div>
            <div class=\"ep-insight-value\">{top_category}</div>
            <div class=\"ep-insight-detail\">{top_category_count:,} enrollments</div>
        </div>
        <div class=\"ep-insight\">
            <div class=\"ep-insight-kicker\">Leading Course Level</div>
            <div class=\"ep-insight-value\">{top_level}</div>
            <div class=\"ep-insight-detail\">{top_level_count:,} enrollments</div>
        </div>
        <div class=\"ep-insight\">
            <div class=\"ep-insight-kicker\">Largest Gender Segment</div>
            <div class=\"ep-insight-value\">{top_gender}</div>
            <div class=\"ep-insight-detail\">{top_gender_share:.1f}% of filtered enrollments</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# AUTOMATIC DATA-DRIVEN INSIGHTS
# ============================================================

top_course_row = (
    filtered.groupby(["CourseID", "CourseName"]).size().sort_values(ascending=False)
)
top_course_name = top_course_row.index[0][1] if not top_course_row.empty else "—"
top_course_count = int(top_course_row.iloc[0]) if not top_course_row.empty else 0
category_share = (top_category_count / total_enrollments * 100) if total_enrollments else 0
active_learner_rate = (unique_learners / len(users) * 100) if len(users) else 0

st.markdown(
    f"""
    <div class=\"ep-section-label\">Data-Driven Signals</div>
    <div class=\"ep-auto-grid\">
        <div class=\"ep-auto-card\">
            <div class=\"ep-auto-title\">Category concentration</div>
            <div class=\"ep-auto-text\"><strong>{top_category}</strong> represents <strong>{category_share:.1f}%</strong> of enrollments in the current filtered view.</div>
        </div>
        <div class=\"ep-auto-card\">
            <div class=\"ep-auto-title\">Course engagement</div>
            <div class=\"ep-auto-text\"><strong>{top_course_name}</strong> has the highest enrollment count with <strong>{top_course_count:,}</strong> enrollments.</div>
        </div>
        <div class=\"ep-auto-card\">
            <div class=\"ep-auto-title\">Learner coverage</div>
            <div class=\"ep-auto-text\"><strong>{unique_learners:,}</strong> unique learners appear in this view, equal to <strong>{active_learner_rate:.1f}%</strong> of the available user base.</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# ANALYTICAL CONTEXT
# ============================================================

all_enrollments = len(master)
filter_enrollment_share = (total_enrollments / all_enrollments * 100) if all_enrollments else 0
learner_participation = (unique_learners / len(users) * 100) if len(users) else 0

valid_dates = filtered["TransactionDate"].dropna()
if not valid_dates.empty:
    date_range_text = f"{valid_dates.min():%d %b %Y} → {valid_dates.max():%d %b %Y}"
else:
    date_range_text = "No valid dates"

level_share_series = filtered["CourseLevel"].value_counts(normalize=True).mul(100)
top_level_share = float(level_share_series.iloc[0]) if not level_share_series.empty else 0

st.markdown(
    f"""
    <div class=\"ep-section-label\">Analytical Context</div>
    <div class=\"ep-context-grid\">
        <div class=\"ep-context-card\"><div class=\"ep-context-icon\">◉</div><div><div class=\"ep-context-title\">Filtered Dataset Share</div><div class=\"ep-context-value\">{filter_enrollment_share:.1f}%</div><div class=\"ep-context-detail\">{total_enrollments:,} of {all_enrollments:,} enrollments</div></div></div>
        <div class=\"ep-context-card\"><div class=\"ep-context-icon\">◎</div><div><div class=\"ep-context-title\">Learner Participation</div><div class=\"ep-context-value\">{learner_participation:.1f}%</div><div class=\"ep-context-detail\">{unique_learners:,} unique learners in this view</div></div></div>
        <div class=\"ep-context-card\"><div class=\"ep-context-icon\">◆</div><div><div class=\"ep-context-title\">Dominant Level</div><div class=\"ep-context-value\">{top_level}</div><div class=\"ep-context-detail\">{top_level_share:.1f}% of filtered enrollments</div></div></div>
        <div class=\"ep-context-card\"><div class=\"ep-context-icon\">◷</div><div><div class=\"ep-context-title\">Date Coverage</div><div class=\"ep-context-value\">{date_range_text}</div><div class=\"ep-context-detail\">Valid transaction-date range</div></div></div>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()



# ============================================================
# PHASE 5 — RESEARCH INTELLIGENCE LAYER
# ============================================================

st.markdown(
    """
    <div style="margin:24px 0 14px;">
        <div style="font-size:11px;font-weight:800;letter-spacing:.16em;
                    color:#818cf8;text-transform:uppercase;">RESEARCH INTELLIGENCE</div>
        <div style="font-size:24px;font-weight:800;color:#f8fafc;margin-top:4px;">
            What does the filtered data show?
        </div>
        <div style="font-size:13px;color:#94a3b8;margin-top:5px;">
            Automatically generated descriptive observations from the currently selected dataset.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


def _safe_share(value, total):
    return (float(value) / float(total) * 100) if total else 0.0


# -------------------------
# Research aggregates
# -------------------------
research_rows = []
research_total = len(filtered)

if research_total > 0:
    age_counts = filtered["AgeGroup"].value_counts()
    category_counts = filtered["CourseCategory"].value_counts()
    level_counts = filtered["CourseLevel"].value_counts()
    gender_counts = filtered["Gender"].value_counts()

    if not age_counts.empty:
        age_name = str(age_counts.index[0])
        age_value = int(age_counts.iloc[0])
        research_rows.append({
            "Dimension": "Age Group",
            "Observation": f"{age_name} accounts for the largest share of filtered enrollments ({_safe_share(age_value, research_total):.1f}%)."
        })

    if not category_counts.empty:
        category_name = str(category_counts.index[0])
        category_value = int(category_counts.iloc[0])
        research_rows.append({
            "Dimension": "Course Category",
            "Observation": f"{category_name} is the most represented course category with {category_value:,} enrollments ({_safe_share(category_value, research_total):.1f}%)."
        })

    if not level_counts.empty:
        level_name = str(level_counts.index[0])
        level_value = int(level_counts.iloc[0])
        research_rows.append({
            "Dimension": "Course Level",
            "Observation": f"{level_name} has the highest enrollment volume with {level_value:,} enrollments ({_safe_share(level_value, research_total):.1f}%)."
        })

    if not gender_counts.empty:
        gender_name = str(gender_counts.index[0])
        gender_value = int(gender_counts.iloc[0])
        research_rows.append({
            "Dimension": "Gender",
            "Observation": f"{gender_name} represents the largest gender segment in the filtered enrollment records ({_safe_share(gender_value, research_total):.1f}%)."
        })

    # Age × Category
    age_category_research = pd.crosstab(
        filtered["AgeGroup"], filtered["CourseCategory"]
    )
    if not age_category_research.empty:
        stacked = age_category_research.stack()
        if not stacked.empty:
            idx = stacked.idxmax()
            research_rows.append({
                "Dimension": "Age × Category",
                "Observation": f"The largest age-group/category combination is {idx[0]} × {idx[1]} with {int(stacked.max()):,} enrollments."
            })

    # Age × Level
    age_level_research = pd.crosstab(
        filtered["AgeGroup"], filtered["CourseLevel"]
    )
    if not age_level_research.empty:
        stacked = age_level_research.stack()
        if not stacked.empty:
            idx = stacked.idxmax()
            research_rows.append({
                "Dimension": "Age × Level",
                "Observation": f"The largest age-group/level combination is {idx[0]} × {idx[1]} with {int(stacked.max()):,} enrollments."
            })

    # Gender × Level
    gender_level_research = pd.crosstab(
        filtered["Gender"], filtered["CourseLevel"]
    )
    if not gender_level_research.empty:
        stacked = gender_level_research.stack()
        if not stacked.empty:
            idx = stacked.idxmax()
            research_rows.append({
                "Dimension": "Gender × Level",
                "Observation": f"The largest gender/level combination is {idx[0]} × {idx[1]} with {int(stacked.max()):,} enrollments."
            })

    # Temporal observation
    temporal_research = (
        filtered.dropna(subset=["TransactionDate"])
        .groupby(filtered.dropna(subset=["TransactionDate"])["TransactionDate"].dt.to_period("M"))
        .size()
    )
    if not temporal_research.empty:
        peak_period = temporal_research.idxmax()
        low_period = temporal_research.idxmin()
        research_rows.append({
            "Dimension": "Temporal",
            "Observation": f"Enrollment volume peaks in {peak_period} ({int(temporal_research.max()):,}) and is lowest in {low_period} ({int(temporal_research.min()):,})."
        })


# -------------------------
# Insight cards
# -------------------------
if research_rows:
    card_items = research_rows[:4]
    cols = st.columns(len(card_items))
    for col, item in zip(cols, card_items):
        with col:
            st.markdown(
                f"""
                <div style="height:100%;min-height:145px;padding:18px;border-radius:18px;
                            background:linear-gradient(145deg,rgba(30,41,59,.90),rgba(9,14,29,.92));
                            border:1px solid rgba(99,102,241,.18);
                            box-shadow:0 14px 34px rgba(0,0,0,.20);">
                    <div style="font-size:10px;font-weight:800;letter-spacing:.12em;
                                color:#67e8f9;text-transform:uppercase;margin-bottom:9px;">
                        {item['Dimension']}
                    </div>
                    <div style="font-size:13px;line-height:1.65;color:#cbd5e1;">
                        {item['Observation']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with st.expander("📑 View complete research observations", expanded=False):
        research_df = pd.DataFrame(research_rows)
        st.dataframe(research_df, use_container_width=True, hide_index=True)

        st.download_button(
            "⬇️ Download Research Observations",
            data=research_df.to_csv(index=False).encode("utf-8"),
            file_name="edupro_filtered_research_observations.csv",
            mime="text/csv",
            key="download_research_observations"
        )
else:
    st.info("Not enough filtered data to generate research observations.")



# ============================================================
# PHASE 6 — EXECUTIVE / PRESENTATION MODE
# ============================================================

if presentation_mode:

    st.markdown(
        """
        <div style="margin:30px 0 18px;padding:26px 28px;border-radius:22px;
                    background:linear-gradient(135deg,rgba(30,41,59,.92),rgba(15,23,42,.96));
                    border:1px solid rgba(129,140,248,.28);
                    box-shadow:0 18px 45px rgba(0,0,0,.22);">
            <div style="font-size:11px;font-weight:800;letter-spacing:.18em;
                        color:#818cf8;text-transform:uppercase;">EXECUTIVE / PRESENTATION MODE</div>
            <div style="font-size:29px;font-weight:850;color:#f8fafc;margin-top:7px;">
                EduPro Learner Analytics — Executive Brief
            </div>
            <div style="font-size:14px;color:#94a3b8;margin-top:7px;line-height:1.6;">
                A concise, evidence-based snapshot of the currently filtered learner
                enrollment data. All observations are descriptive and based on the
                selected records.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    exec_total = len(filtered)
    exec_learners = filtered["UserID"].nunique() if exec_total else 0
    exec_courses = filtered["CourseID"].nunique() if exec_total else 0
    exec_avg = (exec_total / exec_learners) if exec_learners else 0

    c1, c2, c3, c4 = st.columns(4)
    executive_kpis = [
        ("ENROLLMENTS", f"{exec_total:,}", "Filtered transaction records"),
        ("LEARNERS", f"{exec_learners:,}", "Unique learners represented"),
        ("COURSES", f"{exec_courses:,}", "Unique courses represented"),
        ("AVG / LEARNER", f"{exec_avg:.2f}", "Enrollments per represented learner"),
    ]

    for col, (label, value, note) in zip([c1, c2, c3, c4], executive_kpis):
        with col:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{value}</div>
                    <div class="kpi-sub">{note}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    if exec_total:

        age_exec = filtered["AgeGroup"].value_counts()
        category_exec = filtered["CourseCategory"].value_counts()
        level_exec = filtered["CourseLevel"].value_counts()
        gender_exec = filtered["Gender"].value_counts()

        top_age = age_exec.index[0]
        top_age_n = int(age_exec.iloc[0])
        top_cat = category_exec.index[0]
        top_cat_n = int(category_exec.iloc[0])
        top_level = level_exec.index[0]
        top_level_n = int(level_exec.iloc[0])
        top_gender = gender_exec.index[0]
        top_gender_n = int(gender_exec.iloc[0])

        st.markdown("### 🔎 Executive Findings")

        f1, f2, f3 = st.columns(3)

        with f1:
            st.markdown(
                f"""
                <div class="chart-card">
                    <div class="chart-title">👥 Demographic Signal</div>
                    <div style="font-size:23px;font-weight:800;color:#f8fafc;margin:10px 0 5px;">
                        {top_age}
                    </div>
                    <div style="color:#94a3b8;font-size:13px;">
                        Highest observed enrollment volume among age groups:
                        <b style="color:#cbd5e1;">{top_age_n:,}</b>
                        ({top_age_n/exec_total*100:.1f}%).
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with f2:
            st.markdown(
                f"""
                <div class="chart-card">
                    <div class="chart-title">🎓 Course Signal</div>
                    <div style="font-size:23px;font-weight:800;color:#f8fafc;margin:10px 0 5px;">
                        {top_cat}
                    </div>
                    <div style="color:#94a3b8;font-size:13px;">
                        Leading observed category with
                        <b style="color:#cbd5e1;">{top_cat_n:,}</b>
                        enrollments ({top_cat_n/exec_total*100:.1f}%).
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with f3:
            st.markdown(
                f"""
                <div class="chart-card">
                    <div class="chart-title">📚 Learning-Level Signal</div>
                    <div style="font-size:23px;font-weight:800;color:#f8fafc;margin:10px 0 5px;">
                        {top_level}
                    </div>
                    <div style="color:#94a3b8;font-size:13px;">
                        Most represented course level:
                        <b style="color:#cbd5e1;">{top_level_n:,}</b>
                        enrollments ({top_level_n/exec_total*100:.1f}%).
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("### 📊 Evidence Snapshot")

        evidence_df = pd.DataFrame({
            "Dimension": ["Age Group", "Course Category", "Course Level", "Gender"],
            "Highest Observed Segment": [top_age, top_cat, top_level, top_gender],
            "Enrollments": [top_age_n, top_cat_n, top_level_n, top_gender_n],
            "Share of Filtered Enrollments": [
                f"{top_age_n/exec_total*100:.1f}%",
                f"{top_cat_n/exec_total*100:.1f}%",
                f"{top_level_n/exec_total*100:.1f}%",
                f"{top_gender_n/exec_total*100:.1f}%"
            ]
        })

        st.dataframe(
            evidence_df,
            use_container_width=True,
            hide_index=True
        )

        # Cross-dimensional highlight
        cross_exec = (
            filtered.groupby(["AgeGroup", "CourseCategory"])
            .size()
            .reset_index(name="Enrollments")
            .sort_values("Enrollments", ascending=False)
        )

        st.markdown("### 🔗 Cross-Dimensional Highlight")

        if not cross_exec.empty:
            strongest_age = cross_exec.iloc[0]["AgeGroup"]
            strongest_category = cross_exec.iloc[0]["CourseCategory"]
            strongest_n = int(cross_exec.iloc[0]["Enrollments"])

            st.info(
                f"The strongest observed age-group × course-category combination is "
                f"**{strongest_age} × {strongest_category}**, with **{strongest_n:,} enrollments** "
                f"within the current filter selection."
            )

        # Compact trend visualization
        st.markdown("### 📈 Trend Snapshot")

        if "TransactionDate" in filtered.columns:
            trend_exec = (
                filtered.assign(
                    Month=filtered["TransactionDate"].dt.to_period("M").astype(str)
                )
                .groupby("Month")
                .size()
                .reset_index(name="Enrollments")
            )

            if not trend_exec.empty:
                peak_row = trend_exec.loc[trend_exec["Enrollments"].idxmax()]

                fig_exec = px.line(
                    trend_exec,
                    x="Month",
                    y="Enrollments",
                    markers=True,
                    title="Monthly Enrollment Volume"
                )
                fig_exec = polish_chart(fig_exec, height=390, kind="line")
                fig_exec.add_annotation(
                    x=peak_row["Month"],
                    y=peak_row["Enrollments"],
                    text=f"Peak: {int(peak_row['Enrollments']):,}",
                    showarrow=True,
                    arrowhead=2,
                    font=dict(color="#E2E8F0", size=12)
                )
                st.plotly_chart(fig_exec, use_container_width=True)

        # SDG 4 framing
        st.markdown("### 🌍 SDG 4 Evidence Framing")

        s1, s2, s3 = st.columns(3)
        sdg_cards = [
            ("ACCESS", "Learner representation", "Demographic distributions provide descriptive visibility into who is represented in the dataset."),
            ("SKILLS", "Course-level participation", "Course categories and levels show the observed structure of learning participation."),
            ("INCLUSION", "Gender participation", "Gender-wise enrollment distributions provide a descriptive participation view.")
        ]

        for col, (label, title, body) in zip([s1, s2, s3], sdg_cards):
            with col:
                st.markdown(
                    f"""
                    <div class="chart-card">
                        <div style="font-size:10px;font-weight:800;letter-spacing:.16em;color:#67e8f9;">
                            SDG 4 · {label}
                        </div>
                        <div style="font-size:17px;font-weight:800;color:#f8fafc;margin:8px 0;">
                            {title}
                        </div>
                        <div style="font-size:12px;color:#94a3b8;line-height:1.6;">
                            {body}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Presentation-ready narrative
        report_lines = [
            "EDUPRO LEARNER ANALYTICS — EXECUTIVE BRIEF",
            "",
            f"Filtered enrollments: {exec_total:,}",
            f"Unique learners represented: {exec_learners:,}",
            f"Unique courses represented: {exec_courses:,}",
            f"Average enrollments per represented learner: {exec_avg:.2f}",
            "",
            "KEY OBSERVATIONS",
            f"- Highest observed age-group enrollment: {top_age} ({top_age_n:,}; {top_age_n/exec_total*100:.1f}%).",
            f"- Leading observed course category: {top_cat} ({top_cat_n:,}; {top_cat_n/exec_total*100:.1f}%).",
            f"- Most represented course level: {top_level} ({top_level_n:,}; {top_level_n/exec_total*100:.1f}%).",
            f"- Largest observed gender segment: {top_gender} ({top_gender_n:,}; {top_gender_n/exec_total*100:.1f}%).",
            f"- Strongest observed age-group × category combination: {strongest_age} × {strongest_category} ({strongest_n:,}).",
            "",
            "INTERPRETATION",
            "These findings describe the composition and enrollment behavior visible in the selected dataset.",
            "They should be interpreted as descriptive evidence rather than predictions or causal conclusions.",
            "",
            "SDG 4 FRAMING",
            "The analysis can support education-planning discussions by providing descriptive evidence on learner representation,",
            "course participation, skills-level distribution, and gender participation.",
            "",
            "LIMITATION",
            "Observed patterns depend on the available EduPro dataset and the active dashboard filters."
        ]

        st.download_button(
            "⬇️ Download Executive Brief (.txt)",
            data="\n".join(report_lines).encode("utf-8"),
            file_name="edupro_executive_brief.txt",
            mime="text/plain",
            key="download_executive_brief"
        )

    else:
        st.warning("No records match the current filters. Reset or broaden the filters to generate the executive brief.")


# ============================================================
# PHASE 7 + PHASE 8 — RESEARCH REPORT + FINAL QA
# ============================================================

st.divider()

st.markdown(
    """
    <div style="margin:22px 0 14px;">
        <div style="font-size:11px;font-weight:800;letter-spacing:.16em;
                    color:#22d3ee;text-transform:uppercase;">FINAL RESEARCH LAYER</div>
        <div style="font-size:24px;font-weight:800;color:#f8fafc;margin-top:4px;">
            Research Report & Quality Assurance
        </div>
        <div style="font-size:13px;color:#94a3b8;margin-top:5px;">
            Filter-aware evidence, reproducible validation checks, and presentation-ready research exports.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# PHASE 8 — DATA QUALITY / VALIDATION
# ------------------------------------------------------------

qa_total = len(master)
qa_filtered = len(filtered)

qa_checks = []

def _qa_add(name, value, status, detail):
    qa_checks.append({
        "Check": name,
        "Value": value,
        "Status": status,
        "Detail": detail
    })

# Required sheets / row counts
_qa_add(
    "Users table",
    f"{len(users):,} rows",
    "PASS" if len(users) > 0 else "FAIL",
    "Users source table loaded."
)
_qa_add(
    "Courses table",
    f"{len(courses):,} rows",
    "PASS" if len(courses) > 0 else "FAIL",
    "Courses source table loaded."
)
_qa_add(
    "Transactions table",
    f"{len(transactions):,} rows",
    "PASS" if len(transactions) > 0 else "FAIL",
    "Transactions source table loaded."
)

# Key integrity checks
users_ids = set(users["UserID"].dropna().astype(str).str.strip())
course_ids = set(courses["CourseID"].dropna().astype(str).str.strip())

tx_user_ids = set(transactions["UserID"].dropna().astype(str).str.strip())
tx_course_ids = set(transactions["CourseID"].dropna().astype(str).str.strip())

missing_user_refs = len(tx_user_ids - users_ids)
missing_course_refs = len(tx_course_ids - course_ids)

_qa_add(
    "UserID referential integrity",
    f"{missing_user_refs:,} missing IDs",
    "PASS" if missing_user_refs == 0 else "CHECK",
    "Transaction UserIDs not found in Users."
)
_qa_add(
    "CourseID referential integrity",
    f"{missing_course_refs:,} missing IDs",
    "PASS" if missing_course_refs == 0 else "CHECK",
    "Transaction CourseIDs not found in Courses."
)

# Duplicate key checks
dup_users = int(users["UserID"].duplicated().sum())
dup_courses = int(courses["CourseID"].duplicated().sum())
dup_transactions = int(transactions["TransactionID"].duplicated().sum()) if "TransactionID" in transactions.columns else 0

_qa_add(
    "Duplicate UserID",
    f"{dup_users:,}",
    "PASS" if dup_users == 0 else "CHECK",
    "Duplicate primary-key candidates in Users."
)
_qa_add(
    "Duplicate CourseID",
    f"{dup_courses:,}",
    "PASS" if dup_courses == 0 else "CHECK",
    "Duplicate primary-key candidates in Courses."
)
_qa_add(
    "Duplicate TransactionID",
    f"{dup_transactions:,}",
    "PASS" if dup_transactions == 0 else "CHECK",
    "Duplicate transaction identifiers."
)

# Missingness
missing_cells = int(master.isna().sum().sum())
missing_rate = safe_divide(missing_cells, max(master.shape[0] * master.shape[1], 1)) * 100

_qa_add(
    "Master missing cells",
    f"{missing_cells:,} ({missing_rate:.2f}%)",
    "PASS" if missing_cells == 0 else "INFO",
    "Missing values are retained and handled explicitly where required."
)

# Date validity
invalid_dates = int(master["TransactionDate"].isna().sum())
_qa_add(
    "Transaction dates",
    f"{invalid_dates:,} invalid/missing",
    "PASS" if invalid_dates == 0 else "CHECK",
    "Dates are required for temporal analysis."
)

# Numeric validity
invalid_amounts = int(master["Amount"].isna().sum())
_qa_add(
    "Transaction amount",
    f"{invalid_amounts:,} invalid/missing",
    "PASS" if invalid_amounts == 0 else "INFO",
    "Amount is numeric where supplied."
)

# Merge coverage
merge_missing_user = int(master["UserName"].isna().sum()) if "UserName" in master.columns else 0
merge_missing_course = int(master["CourseName"].isna().sum()) if "CourseName" in master.columns else 0

_qa_add(
    "Merged user coverage",
    f"{merge_missing_user:,} unmatched rows",
    "PASS" if merge_missing_user == 0 else "CHECK",
    "Transactions successfully linked to learner records."
)
_qa_add(
    "Merged course coverage",
    f"{merge_missing_course:,} unmatched rows",
    "PASS" if merge_missing_course == 0 else "CHECK",
    "Transactions successfully linked to course records."
)

qa_df = pd.DataFrame(qa_checks)
qa_passes = int((qa_df["Status"] == "PASS").sum())
qa_checks_count = len(qa_df)
qa_issues = int((qa_df["Status"] == "CHECK").sum())

qa_col1, qa_col2, qa_col3 = st.columns(3)
with qa_col1:
    st.metric("QA Checks", qa_checks_count)
with qa_col2:
    st.metric("Passed", qa_passes)
with qa_col3:
    st.metric("Items to Check", qa_issues)

with st.expander("🛡️ View Final Validation Results", expanded=False):
    st.dataframe(qa_df, use_container_width=True, hide_index=True)

    qa_note = (
        "All critical structural checks passed."
        if qa_issues == 0
        else "Some checks require review before treating the dataset as fully clean."
    )
    if qa_issues == 0:
        st.success("✅ " + qa_note)
    else:
        st.warning("⚠️ " + qa_note)

# ------------------------------------------------------------
# PHASE 7 — FILTER-AWARE RESEARCH REPORT
# ------------------------------------------------------------

report_lines = [
    "EDUPRO LEARNER ANALYTICS",
    "FILTER-AWARE RESEARCH REPORT",
    "=" * 72,
    "",
    "RESEARCH SCOPE",
    "Descriptive analysis of learner demographics and course enrollment behavior.",
    "No prediction, recommendation engine, or causal inference is performed.",
    "",
    "DATASET SNAPSHOT",
    f"Users: {len(users):,}",
    f"Teachers: {len(teachers):,}",
    f"Courses: {len(courses):,}",
    f"Transactions: {len(transactions):,}",
    f"Master records: {len(master):,}",
    f"Filtered records: {len(filtered):,}",
]

if not filtered.empty:
    report_lines += [
        "",
        "FILTER STATE",
        f"Age groups: {', '.join(map(str, selected_age))}",
        f"Gender: {', '.join(map(str, selected_gender))}",
        f"Categories: {', '.join(map(str, selected_category))}",
        f"Course levels: {', '.join(map(str, selected_level))}",
        f"Course types: {', '.join(map(str, selected_type))}",
        "",
        "EXECUTIVE METRICS",
        f"Total enrollments: {len(filtered):,}",
        f"Unique learners: {filtered['UserID'].nunique():,}",
        f"Unique courses: {filtered['CourseID'].nunique():,}",
        f"Average enrollments per represented learner: "
        f"{safe_divide(len(filtered), filtered['UserID'].nunique()):.2f}",
    ]

    def _report_top(column):
        vc = filtered[column].value_counts()
        return (str(vc.index[0]), int(vc.iloc[0])) if not vc.empty else ("N/A", 0)

    r_age, r_age_n = _report_top("AgeGroup")
    r_cat, r_cat_n = _report_top("CourseCategory")
    r_level, r_level_n = _report_top("CourseLevel")
    r_gender, r_gender_n = _report_top("Gender")
    r_course, r_course_n = _report_top("CourseName")

    report_lines += [
        "",
        "KEY DESCRIPTIVE OBSERVATIONS",
        f"- Highest observed age-group enrollment: {r_age} ({r_age_n:,}; "
        f"{safe_divide(r_age_n, len(filtered))*100:.1f}%).",
        f"- Leading observed course category: {r_cat} ({r_cat_n:,}; "
        f"{safe_divide(r_cat_n, len(filtered))*100:.1f}%).",
        f"- Most represented course level: {r_level} ({r_level_n:,}; "
        f"{safe_divide(r_level_n, len(filtered))*100:.1f}%).",
        f"- Largest observed gender segment: {r_gender} ({r_gender_n:,}; "
        f"{safe_divide(r_gender_n, len(filtered))*100:.1f}%).",
        f"- Top observed course by enrollment: {r_course} ({r_course_n:,}).",
    ]

    age_cat = filtered.groupby(["AgeGroup", "CourseCategory"]).size().reset_index(name="Enrollments")
    if not age_cat.empty:
        row = age_cat.loc[age_cat["Enrollments"].idxmax()]
        report_lines.append(
            f"- Strongest observed age-group × category combination: "
            f"{row['AgeGroup']} × {row['CourseCategory']} ({int(row['Enrollments']):,})."
        )

    if "TransactionDate" in filtered.columns and filtered["TransactionDate"].notna().any():
        monthly = (
            filtered.dropna(subset=["TransactionDate"])
            .assign(YearMonth=lambda d: d["TransactionDate"].dt.to_period("M").astype(str))
            .groupby("YearMonth").size()
        )
        if not monthly.empty:
            peak_month = str(monthly.idxmax())
            low_month = str(monthly.idxmin())
            report_lines += [
                f"- Peak observed enrollment month: {peak_month} ({int(monthly.max()):,}).",
                f"- Lowest observed enrollment month: {low_month} ({int(monthly.min()):,}).",
            ]

    report_lines += [
        "",
        "SDG 4 CONTEXT",
        "The descriptive evidence can support education-planning discussions around learner",
        "representation, course participation, skills-level distribution, and gender participation.",
        "This analysis does not establish SDG 4 achievement or causal impact.",
        "",
        "QUALITY ASSURANCE",
        f"QA checks performed: {qa_checks_count}",
        f"QA checks passed: {qa_passes}",
        f"Checks requiring review: {qa_issues}",
        "",
        "LIMITATIONS",
        "Results depend on the available EduPro dataset, its field definitions, and the active filters.",
        "Observed associations should not be interpreted as causal relationships.",
        "",
        "END OF REPORT"
    ]
else:
    report_lines += [
        "",
        "No records match the current filter state.",
        "Reset or broaden filters to generate descriptive findings."
    ]

report_text = "\n".join(report_lines)

# Research report downloads
report_col1, report_col2, report_col3 = st.columns(3)

with report_col1:
    st.download_button(
        "📄 Research Report (.txt)",
        data=report_text.encode("utf-8"),
        file_name="edupro_filter_aware_research_report.txt",
        mime="text/plain",
        use_container_width=True,
        key="phase78_research_report"
    )

with report_col2:
    qa_csv = qa_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "🛡️ QA Report (.csv)",
        data=qa_csv,
        file_name="edupro_final_validation_report.csv",
        mime="text/csv",
        use_container_width=True,
        key="phase78_qa_report"
    )

# ------------------------------------------------------------
# ONE-CLICK EXCEL RESEARCH PACKAGE
# ------------------------------------------------------------

try:
    from io import BytesIO

    excel_buffer = BytesIO()

    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        pd.DataFrame({
            "Metric": [
                "Master Records",
                "Filtered Records",
                "Unique Learners",
                "Unique Courses",
                "Average Enrollments per Learner",
                "QA Checks",
                "QA Passed",
                "QA Items to Check"
            ],
            "Value": [
                len(master),
                len(filtered),
                filtered["UserID"].nunique() if not filtered.empty else 0,
                filtered["CourseID"].nunique() if not filtered.empty else 0,
                round(safe_divide(len(filtered), filtered["UserID"].nunique()), 2)
                if not filtered.empty else 0,
                qa_checks_count,
                qa_passes,
                qa_issues
            ]
        }).to_excel(writer, sheet_name="Executive Summary", index=False)

        qa_df.to_excel(writer, sheet_name="Validation", index=False)

        if not filtered.empty:
            filtered.groupby("AgeGroup").size().reset_index(name="Enrollments").to_excel(
                writer, sheet_name="Age Analysis", index=False
            )
            filtered.groupby("CourseCategory").size().reset_index(name="Enrollments").sort_values(
                "Enrollments", ascending=False
            ).to_excel(writer, sheet_name="Category Analysis", index=False)
            filtered.groupby("CourseLevel").size().reset_index(name="Enrollments").sort_values(
                "Enrollments", ascending=False
            ).to_excel(writer, sheet_name="Level Analysis", index=False)
            filtered.groupby("Gender").size().reset_index(name="Enrollments").sort_values(
                "Enrollments", ascending=False
            ).to_excel(writer, sheet_name="Gender Analysis", index=False)

            age_cat_export = (
                filtered.groupby(["AgeGroup", "CourseCategory"])
                .size()
                .reset_index(name="Enrollments")
                .sort_values("Enrollments", ascending=False)
            )
            age_cat_export.to_excel(writer, sheet_name="Age Category", index=False)

            monthly_export = (
                filtered.dropna(subset=["TransactionDate"])
                .assign(YearMonth=lambda d: d["TransactionDate"].dt.to_period("M").astype(str))
                .groupby("YearMonth")
                .size()
                .reset_index(name="Enrollments")
            )
            monthly_export.to_excel(writer, sheet_name="Monthly Trend", index=False)

        pd.DataFrame({"Report": report_lines}).to_excel(
            writer, sheet_name="Research Report", index=False
        )

    excel_buffer.seek(0)

    with report_col3:
        st.download_button(
            "📦 Complete Research Package (.xlsx)",
            data=excel_buffer.getvalue(),
            file_name="edupro_complete_research_package.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key="phase78_excel_package"
        )
except Exception as excel_error:
    with report_col3:
        st.warning(f"Excel package could not be generated: {excel_error}")

# ------------------------------------------------------------
# FINAL STATUS
# ------------------------------------------------------------

if qa_issues == 0:
    st.success(
        "🏁 Final QA status: all defined structural validation checks passed. "
        "The dashboard is ready for the final deployment/portfolio phase."
    )
else:
    st.warning(
        f"🏁 Final QA status: {qa_issues} validation item(s) require review. "
        "The report remains available, but review the QA table before final submission."
    )



# ============================================================
# TABS
# ============================================================

tabs = st.tabs(
    [
        "📊 Overview",
        "👥 Demographics",
        "🎓 Course Intelligence",
        "🔥 Learner Engagement",
        "📅 Temporal Trends",
        "🔗 Cross-Dimensional",
        "🔬 Research Findings",
        "🌍 SDG 4",
        "📘 Methodology"
    ]
)


# ============================================================
# TAB 1 - OVERVIEW
# ============================================================

with tabs[0]:

    st.header(
        "Overview"
    )

    col1, col2 = st.columns(2)

    # -------------------------
    # Age Distribution
    # -------------------------

    with col1:

        age_data = (
            filtered
            .groupby("AgeGroup")
            .size()
            .reset_index(name="Enrollments")
        )

        age_order = [
            "<18",
            "18–25",
            "26–35",
            "36–45",
            "45+"
        ]

        age_data["AgeGroup"] = pd.Categorical(
            age_data["AgeGroup"],
            categories=age_order,
            ordered=True
        )

        age_data = age_data.sort_values(
            "AgeGroup"
        )

        fig = px.bar(
            age_data,
            x="AgeGroup",
            y="Enrollments",
            title="Enrollment by Age Group",
            text="Enrollments",
            template="plotly_dark"
        )
        st.plotly_chart(
            apply_premium_theme(fig, height=420),
            use_container_width=True
        )

    # -------------------------
    # Category Distribution
    # -------------------------

    with col2:

        category_data = (
            filtered
            .groupby("CourseCategory")
            .size()
            .reset_index(name="Enrollments")
            .sort_values(
                "Enrollments",
                ascending=False
            )
        )

        fig = px.bar(
            category_data,
            x="CourseCategory",
            y="Enrollments",
            title="Course Category Demand",
            text="Enrollments",
            template="plotly_dark"
        )

        fig.update_layout(
            xaxis_tickangle=-35
        )

        st.plotly_chart(
            apply_premium_theme(fig),
            use_container_width=True
        )

    col3, col4 = st.columns(2)

    # -------------------------
    # Course Level
    # -------------------------

    with col3:

        level_data = (
            filtered
            .groupby("CourseLevel")
            .size()
            .reset_index(name="Enrollments")
        )

        fig = px.pie(
            level_data,
            names="CourseLevel",
            values="Enrollments",
            title="Course Level Distribution",
            hole=0.45,
            template="plotly_dark"
        )

        st.plotly_chart(
            apply_premium_theme(fig),
            use_container_width=True
        )

    # -------------------------
    # Gender
    # -------------------------

    with col4:

        gender_data = (
            filtered
            .groupby("Gender")
            .size()
            .reset_index(name="Enrollments")
        )

        fig = px.pie(
            gender_data,
            names="Gender",
            values="Enrollments",
            title="Gender Participation",
            hole=0.45,
            template="plotly_dark"
        )

        st.plotly_chart(
            apply_premium_theme(fig),
            use_container_width=True
        )


# ============================================================
# TAB 2 - DEMOGRAPHICS
# ============================================================

with tabs[1]:

    st.header(
        "Learner Demographics"
    )

    # -------------------------
    # Age × Gender
    # -------------------------

    age_gender = pd.crosstab(
        filtered["AgeGroup"],
        filtered["Gender"]
    )

    age_gender = age_gender.reindex(
        [
            "<18",
            "18–25",
            "26–35",
            "36–45",
            "45+"
        ]
    )

    fig = px.imshow(
        age_gender,
        text_auto=True,
        aspect="auto",
        title="Age Group × Gender Enrollment",
        template="plotly_dark"
    )

    st.plotly_chart(
        apply_premium_theme(fig),
        use_container_width=True
    )

    # -------------------------
    # Gender by Age
    # -------------------------

    gender_age = (
        filtered
        .groupby(
            ["AgeGroup", "Gender"]
        )
        .size()
        .reset_index(
            name="Enrollments"
        )
    )

    fig = px.bar(
        gender_age,
        x="AgeGroup",
        y="Enrollments",
        color="Gender",
        barmode="group",
        title="Gender Participation Across Age Groups",
        template="plotly_dark"
    )

    st.plotly_chart(
        apply_premium_theme(fig),
        use_container_width=True
    )

    # -------------------------
    # Demographic Table
    # -------------------------

    demographic_summary = (
        filtered
        .groupby(
            ["AgeGroup", "Gender"]
        )
        .agg(
            Enrollments=("UserID", "count"),
            UniqueLearners=("UserID", "nunique")
        )
        .reset_index()
    )

    st.subheader(
        "Demographic Summary"
    )

    st.dataframe(
        demographic_summary,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 3 - COURSE INTELLIGENCE
# ============================================================

with tabs[2]:

    st.header(
        "Course Intelligence"
    )

    # -------------------------
    # Category Performance
    # -------------------------

    category_performance = (
        filtered
        .groupby("CourseCategory")
        .agg(
            Enrollments=("CourseID", "count"),
            UniqueLearners=("UserID", "nunique"),
            AverageRating=("CourseRating", "mean"),
            AveragePrice=("CoursePrice", "mean")
        )
        .reset_index()
    )

    category_performance[
        "AverageRating"
    ] = category_performance[
        "AverageRating"
    ].round(2)

    category_performance[
        "AveragePrice"
    ] = category_performance[
        "AveragePrice"
    ].round(2)

    fig = px.bar(
        category_performance.sort_values(
            "Enrollments",
            ascending=False
        ),
        x="CourseCategory",
        y="Enrollments",
        title="Category Performance",
        template="plotly_dark"
    )

    fig.update_layout(
        xaxis_tickangle=-35
    )

    st.plotly_chart(
        apply_premium_theme(fig),
        use_container_width=True
    )

    # -------------------------
    # Level Demand
    # -------------------------

    level_performance = (
        filtered
        .groupby("CourseLevel")
        .agg(
            Enrollments=("CourseID", "count"),
            UniqueLearners=("UserID", "nunique"),
            AverageRating=("CourseRating", "mean")
        )
        .reset_index()
    )

    fig = px.bar(
        level_performance,
        x="CourseLevel",
        y="Enrollments",
        color="CourseLevel",
        title="Course Level Demand",
        template="plotly_dark"
    )

    st.plotly_chart(
        apply_premium_theme(fig),
        use_container_width=True
    )

    # -------------------------
    # Top Courses
    # -------------------------

    top_courses = (
        filtered
        .groupby(
            [
                "CourseID",
                "CourseName",
                "CourseCategory"
            ]
        )
        .agg(
            Enrollments=("UserID", "count"),
            UniqueLearners=("UserID", "nunique"),
            AverageRating=("CourseRating", "mean")
        )
        .reset_index()
        .sort_values(
            "Enrollments",
            ascending=False
        )
        .head(15)
    )

    top_courses["Rank"] = range(1, len(top_courses) + 1)

    fig = px.bar(
        top_courses.sort_values(
            "Enrollments"
        ),
        x="Enrollments",
        y="CourseName",
        orientation="h",
        title="Top 15 Most Enrolled Courses",
        template="plotly_dark"
    )

    st.plotly_chart(
        apply_premium_theme(fig),
        use_container_width=True
    )

    st.subheader(
        "Top Course Ranking"
    )

    st.dataframe(
        top_courses[["Rank", "CourseName", "CourseCategory", "Enrollments", "UniqueLearners", "AverageRating"]],
        use_container_width=True,
        hide_index=True
    )

    st.subheader(
        "Course Performance Table"
    )

    st.dataframe(
        category_performance,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 4 - LEARNER ENGAGEMENT
# ============================================================

with tabs[3]:

    st.header(
        "Learner Engagement & Activity"
    )

    learner_activity = (
        filtered
        .groupby("UserID")
        .agg(
            TotalEnrollments=("CourseID", "count"),
            UniqueCourses=("CourseID", "nunique"),
            TotalSpend=("Amount", "sum"),
            Age=("Age", "first"),
            AgeGroup=("AgeGroup", "first"),
            Gender=("Gender", "first")
        )
        .reset_index()
    )

    def activity_segment(x):

        if x <= 2:
            return "Low Activity"

        elif x <= 5:
            return "Moderate"

        elif x <= 10:
            return "High"

        else:
            return "Very High"

    learner_activity[
        "ActivitySegment"
    ] = learner_activity[
        "TotalEnrollments"
    ].apply(activity_segment)

    # -------------------------
    # Activity Distribution
    # -------------------------

    activity_data = (
        learner_activity
        .groupby("ActivitySegment")
        .size()
        .reset_index(
            name="Learners"
        )
    )

    activity_order = [
        "Low Activity",
        "Moderate",
        "High",
        "Very High"
    ]

    activity_data["ActivitySegment"] = pd.Categorical(
        activity_data["ActivitySegment"],
        categories=activity_order,
        ordered=True
    )

    activity_data = activity_data.sort_values(
        "ActivitySegment"
    )

    fig = px.bar(
        activity_data,
        x="ActivitySegment",
        y="Learners",
        title="Learner Activity Segments",
        template="plotly_dark"
    )

    st.plotly_chart(
        apply_premium_theme(fig),
        use_container_width=True
    )

    # -------------------------
    # Enrollment Share
    # -------------------------

    enrollment_share = (
        learner_activity
        .groupby("ActivitySegment")
        ["TotalEnrollments"]
        .sum()
        .reset_index()
    )

    enrollment_share["ActivitySegment"] = pd.Categorical(
        enrollment_share["ActivitySegment"],
        categories=activity_order,
        ordered=True
    )

    enrollment_share = enrollment_share.sort_values(
        "ActivitySegment"
    )

    fig = px.pie(
        enrollment_share,
        names="ActivitySegment",
        values="TotalEnrollments",
        title="Enrollment Share by Activity Segment",
        hole=0.45,
        template="plotly_dark"
    )

    st.plotly_chart(
        apply_premium_theme(fig),
        use_container_width=True
    )

    # -------------------------
    # Age × Activity
    # -------------------------

    age_activity = pd.crosstab(
        learner_activity["AgeGroup"],
        learner_activity["ActivitySegment"]
    )

    age_activity = age_activity.reindex(
        [
            "<18",
            "18–25",
            "26–35",
            "36–45",
            "45+"
        ]
    )

    age_activity = age_activity.reindex(
        columns=activity_order,
        fill_value=0
    )

    fig = px.imshow(
        age_activity,
        text_auto=True,
        aspect="auto",
        title="Age Group × Learner Activity",
        template="plotly_dark"
    )

    st.plotly_chart(
        apply_premium_theme(fig),
        use_container_width=True
    )

    # -------------------------
    # Learner Activity Table
    # -------------------------

    st.subheader(
        "Top Active Learners"
    )

    top_active = learner_activity.sort_values(
        "TotalEnrollments",
        ascending=False
    ).head(20)

    st.dataframe(
        top_active,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 5 - TEMPORAL TRENDS
# ============================================================

with tabs[4]:

    st.header(
        "Temporal Enrollment Trends"
    )

    temporal = (
        filtered
        .dropna(subset=["TransactionDate"])
        .groupby("YearMonth")
        .size()
        .reset_index(
            name="Enrollments"
        )
    )

    temporal["Date"] = pd.to_datetime(
        temporal["YearMonth"]
    )

    temporal = temporal.sort_values(
        "Date"
    )

    temporal["MoM_Change"] = (
        temporal["Enrollments"]
        .pct_change() * 100
    )

    # -------------------------
    # Monthly Trend
    # -------------------------

    fig = px.line(
        temporal,
        x="Date",
        y="Enrollments",
        markers=True,
        title="Monthly Enrollment Trend",
        template="plotly_dark"
    )

    fig = apply_premium_theme(fig, height=440, kind="line")

    if not temporal.empty:
        peak_row = temporal.loc[temporal["Enrollments"].idxmax()]
        fig.add_trace(
            go.Scatter(
                x=[peak_row["Date"]],
                y=[peak_row["Enrollments"]],
                mode="markers+text",
                text=["Peak"],
                textposition="top center",
                marker=dict(size=11, color="#F59E0B", line=dict(width=2, color="#FEF3C7")),
                name="Peak",
                hovertemplate="<b>Peak: %{x|%b %Y}</b><br>Enrollments: %{y:,}<extra></extra>"
            )
        )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -------------------------
    # MoM Change
    # -------------------------

    fig = px.bar(
        temporal,
        x="Date",
        y="MoM_Change",
        title="Month-over-Month Enrollment Change (%)",
        template="plotly_dark"
    )

    st.plotly_chart(
        apply_premium_theme(fig),
        use_container_width=True
    )

    # -------------------------
    # Peak Period
    # -------------------------

    if not temporal.empty:

        peak = temporal.loc[
            temporal["Enrollments"].idxmax()
        ]

        lowest = temporal.loc[
            temporal["Enrollments"].idxmin()
        ]

        fig_peak = None
        # Add peak/low markers to the already-rendered trend chart when possible.
        # The chart itself remains above; this compact summary keeps the analysis readable.
        peak_label = f"Peak: {peak['YearMonth']} ({int(peak['Enrollments']):,})"
        low_label = f"Low: {lowest['YearMonth']} ({int(lowest['Enrollments']):,})"

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Peak Enrollment Period",
                peak["YearMonth"],
                f"{int(peak['Enrollments']):,} enrollments"
            )

        with c2:

            st.metric(
                "Lowest Enrollment Period",
                lowest["YearMonth"],
                f"{int(lowest['Enrollments']):,} enrollments"
            )


# ============================================================
# TAB 6 - CROSS DIMENSIONAL
# ============================================================

with tabs[5]:

    st.header(
        "Cross-Dimensional Analysis"
    )

    # -------------------------
    # Age × Category
    # -------------------------

    age_category = pd.crosstab(
        filtered["AgeGroup"],
        filtered["CourseCategory"]
    )

    age_category = age_category.reindex(
        [
            "<18",
            "18–25",
            "26–35",
            "36–45",
            "45+"
        ]
    )

    fig = px.imshow(
        age_category,
        text_auto=True,
        aspect="auto",
        title="Age Group × Course Category",
        template="plotly_dark"
    )

    st.plotly_chart(
        apply_premium_theme(fig),
        use_container_width=True
    )

    # -------------------------
    # Age × Level
    # -------------------------

    age_level = pd.crosstab(
        filtered["AgeGroup"],
        filtered["CourseLevel"]
    )

    age_level = age_level.reindex(
        [
            "<18",
            "18–25",
            "26–35",
            "36–45",
            "45+"
        ]
    )

    fig = px.imshow(
        age_level,
        text_auto=True,
        aspect="auto",
        title="Age Group × Course Level",
        template="plotly_dark"
    )

    st.plotly_chart(
        apply_premium_theme(fig),
        use_container_width=True
    )

    # -------------------------
    # Gender × Category
    # -------------------------

    gender_category = pd.crosstab(
        filtered["Gender"],
        filtered["CourseCategory"]
    )

    fig = px.imshow(
        gender_category,
        text_auto=True,
        aspect="auto",
        title="Gender × Course Category",
        template="plotly_dark"
    )

    st.plotly_chart(
        apply_premium_theme(fig),
        use_container_width=True
    )

    # -------------------------
    # Gender × Level
    # -------------------------

    gender_level = pd.crosstab(
        filtered["Gender"],
        filtered["CourseLevel"]
    )

    fig = px.imshow(
        gender_level,
        text_auto=True,
        aspect="auto",
        title="Gender × Course Level",
        template="plotly_dark"
    )

    st.plotly_chart(
        apply_premium_theme(fig),
        use_container_width=True
    )


# ============================================================
# TAB 7 - RESEARCH FINDINGS
# ============================================================

with tabs[6]:

    st.header(
        "🔬 Research Findings"
    )

    insights_file = os.path.join(
        REPORT_DIR,
        "step27_final_research_insights.csv"
    )

    recommendations_file = os.path.join(
        REPORT_DIR,
        "step27_recommendations.csv"
    )

    if os.path.exists(insights_file):

        insights = pd.read_csv(
            insights_file
        )

        st.subheader(
            "Final Research Insights"
        )

        st.dataframe(
            insights,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Research insights file not found."
        )

    if os.path.exists(recommendations_file):

        recommendations = pd.read_csv(
            recommendations_file
        )

        st.subheader(
            "Recommendations"
        )

        st.dataframe(
            recommendations,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Recommendations file not found."
        )


# ============================================================
# TAB 8 - SDG 4
# ============================================================

with tabs[7]:

    st.header(
        "🌍 SDG 4 – Quality Education"
    )

    st.info(
        "This project provides descriptive evidence about learner "
        "demographics and course enrollment behavior that can support "
        "education planning and SDG 4-related analysis."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.subheader(
            "SDG 4.3"
        )

        st.write(
            "Access to education and participation across learner "
            "age groups and course levels."
        )

    with col2:

        st.subheader(
            "SDG 4.4"
        )

        st.write(
            "Understanding demand for skill-oriented course "
            "categories and learning levels."
        )

    with col3:

        st.subheader(
            "SDG 4.5"
        )

        st.write(
            "Examining participation patterns across gender "
            "and demographic groups."
        )

    st.divider()

    sdg_file = os.path.join(
        REPORT_DIR,
        "step28_table19_sdg4_mapping.csv"
    )

    if os.path.exists(sdg_file):

        sdg_data = pd.read_csv(
            sdg_file
        )

        st.subheader(
            "SDG 4 Mapping"
        )

        st.dataframe(
            sdg_data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "SDG 4 mapping report not found."
        )


# ============================================================
# TAB 9 - METHODOLOGY
# ============================================================

with tabs[8]:

    st.header(
        "📘 Research Methodology"
    )

    methodology = pd.DataFrame(
        {
            "Stage": [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10
            ],
            "Stage Description": [
                "Data Collection",
                "Data Cleaning",
                "Data Validation",
                "Master Dataset Creation",
                "Demographic Analysis",
                "Course Preference Analysis",
                "Learner Engagement Analysis",
                "Temporal Analysis",
                "Cross-Dimensional Analysis",
                "Research Findings & SDG Mapping"
            ]
        }
    )

    st.dataframe(
        methodology,
        use_container_width=True,
        hide_index=True
    )

    st.subheader(
        "Dataset Structure"
    )

    dataset_profile = pd.DataFrame(
        {
            "Dataset": [
                "Users",
                "Teachers",
                "Courses",
                "Transactions",
                "Master Dataset"
            ],
            "Rows": [
                len(users),
                len(teachers),
                len(courses),
                len(transactions),
                len(master)
            ]
        }
    )

    st.dataframe(
        dataset_profile,
        use_container_width=True,
        hide_index=True
    )

    st.subheader(
        "Analytical Scope"
    )

    st.write(
        """
        • Descriptive analytics only

        • Learner demographic analysis

        • Enrollment behavior analysis

        • Course category and level preferences

        • Gender participation analysis

        • Age-group preference analysis

        • Learner engagement segmentation

        • Temporal enrollment analysis

        • Cross-dimensional analysis

        • SDG 4 alignment

        • No prediction or recommendation engine
        """
    )


# ============================================================
# DOWNLOAD CENTER
# ============================================================

st.divider()

st.header(
    "📥 Download Center"
)


# -------------------------
# Filtered Dataset
# -------------------------

csv_data = filtered.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Dataset",
    data=csv_data,
    file_name="edupro_filtered_dataset.csv",
    mime="text/csv"
)


# -------------------------
# Executive Snapshot CSV
# -------------------------

executive_summary = pd.DataFrame({
    "Metric": [
        "Total Enrollments",
        "Unique Learners",
        "Unique Courses",
        "Average Enrollments per Learner",
        "Average Age",
        "Most Active Age Group",
        "Leading Category",
        "Leading Course Level",
        "Largest Gender Segment",
        "Top Course"
    ],
    "Value": [
        total_enrollments,
        unique_learners,
        unique_courses,
        round(average_enrollment, 2),
        round(average_age, 2),
        top_age,
        top_category,
        top_level,
        top_gender,
        top_course_name
    ]
})

summary_csv = executive_summary.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download Executive Snapshot",
    data=summary_csv,
    file_name="edupro_executive_snapshot.csv",
    mime="text/csv"
)


# -------------------------
# Master Research Results
# -------------------------

master_results_file = os.path.join(
    REPORT_DIR,
    "step28_master_research_results.csv"
)

if os.path.exists(master_results_file):

    with open(
        master_results_file,
        "rb"
    ) as f:

        st.download_button(
            label="⬇️ Download Master Research Results",
            data=f.read(),
            file_name="step28_master_research_results.csv",
            mime="text/csv"
        )


# -------------------------
# Research Excel Workbook
# -------------------------

excel_file = os.path.join(
    REPORT_DIR,
    "step28_research_paper_tables.xlsx"
)

if os.path.exists(excel_file):

    with open(
        excel_file,
        "rb"
    ) as f:

        st.download_button(
            label="⬇️ Download Research Tables Excel",
            data=f.read(),
            file_name="step28_research_paper_tables.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "EduPro Learner Analytics | MCA Research Project | "
    "Descriptive Analytics Dashboard"
)
