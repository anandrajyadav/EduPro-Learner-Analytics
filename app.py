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

.main {
    background-color: #0b1020;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

h1, h2, h3 {
    color: #ffffff !important;
}

p, label {
    color: #cbd5e1 !important;
}

[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        rgba(30,41,59,0.95),
        rgba(15,23,42,0.95)
    );
    border: 1px solid rgba(148,163,184,0.20);
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] {
    background-color: #0f172a;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #111827;
    border-radius: 10px;
    padding: 10px 18px;
}

.stTabs [aria-selected="true"] {
    background-color: #2563eb;
}

div[data-testid="stDataFrame"] {
    border-radius: 12px;
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

st.title(
    "📊 EduPro Learner Analytics Dashboard"
)

st.caption(
    "Learner Demographics and Course Enrollment Behavior Analysis"
)

st.markdown(
    "Descriptive analytics dashboard for understanding learner demographics, "
    "course preferences, engagement patterns and enrollment behavior."
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
    default=age_options
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
    default=gender_options
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
    default=category_options
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
    default=level_options
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
    default=type_options
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


st.divider()


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
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
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
            template="plotly_dark"
        )

        fig.update_layout(
            xaxis_tickangle=-35
        )

        st.plotly_chart(
            fig,
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
            fig,
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
            fig,
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
        fig,
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
        fig,
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
        fig,
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
        fig,
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
        fig,
        use_container_width=True
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
        fig,
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
        fig,
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
        fig,
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
        fig,
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
        fig,
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
        fig,
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
        fig,
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
        fig,
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