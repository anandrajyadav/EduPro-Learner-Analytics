# ============================================================
# EDUPRO - FINAL RESEARCH PAPER GENERATOR
# STEP 31
# ============================================================

import os
import pandas as pd


# ============================================================
# PATHS
# ============================================================

REPORT_DIR = os.path.join(
    "outputs",
    "reports"
)

MASTER_FILE = os.path.join(
    REPORT_DIR,
    "step28_master_research_results.csv"
)

INSIGHTS_FILE = os.path.join(
    REPORT_DIR,
    "step27_final_research_insights.csv"
)

RECOMMENDATIONS_FILE = os.path.join(
    REPORT_DIR,
    "step27_recommendations.csv"
)

CONCLUSION_FILE = os.path.join(
    REPORT_DIR,
    "step27_research_conclusion.txt"
)

LIMITATIONS_FILE = os.path.join(
    REPORT_DIR,
    "step27_limitations.csv"
)

FUTURE_SCOPE_FILE = os.path.join(
    REPORT_DIR,
    "step27_future_scope.csv"
)

OUTPUT_FILE = os.path.join(
    REPORT_DIR,
    "EduPro_Final_Research_Paper.txt"
)


# ============================================================
# HELPERS
# ============================================================

def load_csv(filename):

    path = os.path.join(
        REPORT_DIR,
        filename
    )

    if os.path.exists(path):

        try:
            return pd.read_csv(path)

        except Exception:
            return pd.DataFrame()

    return pd.DataFrame()


def load_text(path):

    if os.path.exists(path):

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    return ""


def dataframe_to_text(df, max_rows=15):

    if df.empty:
        return "No data available."

    return df.head(max_rows).to_string(
        index=False
    )


# ============================================================
# LOAD REPORTS
# ============================================================

insights = load_csv(
    "step27_final_research_insights.csv"
)

recommendations = load_csv(
    "step27_recommendations.csv"
)

limitations = load_csv(
    "step27_limitations.csv"
)

future_scope = load_csv(
    "step27_future_scope.csv"
)

conclusion = load_text(
    CONCLUSION_FILE
)


# ============================================================
# LOAD MASTER RESULTS
# ============================================================

master_results = pd.DataFrame()

if os.path.exists(MASTER_FILE):

    try:

        master_results = pd.read_csv(
            MASTER_FILE
        )

    except Exception:

        master_results = pd.DataFrame()


# ============================================================
# TITLE
# ============================================================

paper = []

paper.append(
    "=" * 80
)

paper.append(
    "LEARNER DEMOGRAPHICS AND COURSE ENROLLMENT"
)

paper.append(
    "BEHAVIOR ANALYSIS ON EDUPRO"
)

paper.append(
    "=" * 80
)

paper.append("")

paper.append(
    "A DESCRIPTIVE ANALYTICS APPROACH FOR UNDERSTANDING "
    "LEARNER PARTICIPATION, COURSE PREFERENCES AND "
    "ENROLLMENT BEHAVIOR"
)

paper.append("")

paper.append(
    "Research Project – Master of Computer Applications (MCA)"
)

paper.append("")


# ============================================================
# ABSTRACT
# ============================================================

paper.append(
    "1. ABSTRACT"
)

paper.append("-" * 80)

paper.append(
    """
Online learning platforms generate large volumes of data related
to learners, courses and enrollment transactions. However, raw
transaction records alone do not provide a clear understanding of
learner demographics, course preferences and enrollment behavior.

This research project presents a descriptive analytics study of
learner demographics and course enrollment behavior on the EduPro
platform. The study integrates learner, course and transaction
datasets to construct a unified analytical dataset. Descriptive
statistical techniques, demographic segmentation, cross-dimensional
analysis, temporal analysis and learner activity segmentation are
used to identify meaningful patterns in the data.

The analysis focuses on learner age groups, gender participation,
course categories, course levels, course types, learner engagement,
monthly enrollment behavior and relationships between demographic
groups and course preferences.

An interactive Streamlit dashboard was also developed to provide
visual exploration of the analytical results. The project further
examines how the findings can support education-related planning
and Sustainable Development Goal 4, particularly in relation to
access, skills development and gender participation.

The study is descriptive in nature and does not attempt to predict
future learner behavior or establish causal relationships.
"""
)

paper.append("")


# ============================================================
# KEYWORDS
# ============================================================

paper.append(
    "2. KEYWORDS"
)

paper.append("-" * 80)

paper.append(
    "Descriptive Analytics, Learner Analytics, "
    "Educational Data Analytics, Course Enrollment, "
    "Learner Demographics, Course Preference, "
    "Streamlit Dashboard, SDG 4, Quality Education"
)

paper.append("")


# ============================================================
# INTRODUCTION
# ============================================================

paper.append(
    "3. INTRODUCTION"
)

paper.append("-" * 80)

paper.append(
    """
The rapid growth of online learning platforms has created new
opportunities for learners to access educational content across
different subjects, skill levels and learning formats. At the same
time, these platforms generate large datasets containing information
about learners, courses and enrollment transactions.

Educational data analytics can transform such raw records into
useful information for understanding learner participation and
learning preferences. Demographic variables such as age and gender
can be analyzed together with course attributes to identify patterns
in enrollment behavior.

The present study focuses on EduPro, an online learning platform
dataset containing learner information, teacher information, course
information and enrollment transactions. The purpose of this study
is to analyze the existing data using descriptive analytics and
identify meaningful patterns in learner participation and course
preferences.

The project also demonstrates the practical use of data analytics
through an interactive Streamlit dashboard. The dashboard enables
users to explore demographic distributions, course demand, learner
engagement, temporal trends and cross-dimensional relationships.

The research additionally considers the relevance of these findings
to SDG 4, which promotes inclusive and equitable quality education
and lifelong learning opportunities.
"""
)

paper.append("")


# ============================================================
# PROBLEM STATEMENT
# ============================================================

paper.append(
    "4. PROBLEM STATEMENT"
)

paper.append("-" * 80)

paper.append(
    """
Raw learner and transaction datasets contain valuable information,
but meaningful educational insights cannot be obtained easily
without systematic analysis.

The main problem addressed by this research is the lack of a
structured analytical view of learner demographics and course
enrollment behavior.

The study therefore investigates:

• Which learner age groups show higher enrollment participation?

• How does enrollment participation differ across genders?

• Which course categories and types are more popular?

• Which course levels attract different learner segments?

• How do course preferences vary across age and gender?

• How active are individual learners?

• How does enrollment behavior change over time?

• How can these descriptive findings support education-related
  planning?
"""
)

paper.append("")


# ============================================================
# OBJECTIVES
# ============================================================

paper.append(
    "5. RESEARCH OBJECTIVES"
)

paper.append("-" * 80)

objectives = [
    "Analyze learner demographics using age and gender.",
    "Identify the most active learner age groups.",
    "Analyze gender-wise enrollment participation.",
    "Identify popular course categories and course types.",
    "Analyze preferences for beginner, intermediate and advanced courses.",
    "Study relationships between age groups and course preferences.",
    "Study relationships between gender and course preferences.",
    "Analyze learner engagement and activity levels.",
    "Analyze monthly enrollment behavior.",
    "Develop an interactive Streamlit analytics dashboard.",
    "Identify findings relevant to education planning and SDG 4."
]

for i, objective in enumerate(
    objectives,
    start=1
):

    paper.append(
        f"{i}. {objective}"
    )

paper.append("")


# ============================================================
# RESEARCH QUESTIONS
# ============================================================

paper.append(
    "6. RESEARCH QUESTIONS"
)

paper.append("-" * 80)

questions = [
    "Which age groups are most active on the EduPro platform?",
    "How does enrollment participation differ by gender?",
    "Which course categories are most preferred by learners?",
    "How do course preferences vary across age groups?",
    "How do course preferences vary across gender groups?",
    "Are beginner, intermediate and advanced courses preferred by different learner segments?",
    "How is learner engagement distributed across activity levels?",
    "What are the major temporal patterns in course enrollment?",
    "Which demographic-course combinations show higher enrollment?",
    "How can the findings support education-related planning?"
]

for i, question in enumerate(
    questions,
    start=1
):

    paper.append(
        f"RQ{i}. {question}"
    )

paper.append("")


# ============================================================
# DATASET
# ============================================================

paper.append(
    "7. DATASET DESCRIPTION"
)

paper.append("-" * 80)

paper.append(
    """
The EduPro dataset contains four primary relational datasets:
Users, Teachers, Courses and Transactions.
"""
)

paper.append("")

paper.append(
    "Dataset Profile:"
)

paper.append(
    "• Users: 3,000 records"
)

paper.append(
    "• Teachers: 60 records"
)

paper.append(
    "• Courses: 60 records"
)

paper.append(
    "• Transactions: 10,000 records"
)

paper.append("")

paper.append(
    """
The Users dataset contains learner demographic information.
The Teachers dataset contains teacher expertise and experience
information. The Courses dataset contains course categories,
types, levels, prices, duration and ratings. The Transactions
dataset records learner enrollment transactions.

The datasets are integrated using UserID and CourseID to construct
the master analytical dataset.
"""
)

paper.append("")


# ============================================================
# METHODOLOGY
# ============================================================

paper.append(
    "8. METHODOLOGY"
)

paper.append("-" * 80)

methodology = [
    "Data collection",
    "Data cleaning",
    "Data validation",
    "Referential integrity validation",
    "Master dataset construction",
    "Demographic analysis",
    "Course preference analysis",
    "Learner engagement analysis",
    "Temporal analysis",
    "Cross-dimensional analysis",
    "Statistical summary",
    "Research findings generation",
    "SDG 4 mapping",
    "Interactive dashboard development"
]

for i, item in enumerate(
    methodology,
    start=1
):

    paper.append(
        f"{i}. {item}"
    )

paper.append("")


# ============================================================
# DATA PREPROCESSING
# ============================================================

paper.append(
    "9. DATA PREPROCESSING"
)

paper.append("-" * 80)

paper.append(
    """
The data preprocessing stage included checking duplicate
identifiers, missing values, data types and referential integrity.

TransactionDate was converted into a standard datetime format.
Numeric fields such as Age, Amount, CoursePrice and CourseRating
were converted into appropriate numeric types.

Age groups were created using the following categories:

• Below 18
• 18–25
• 26–35
• 36–45
• 45+

The cleaned Users, Transactions and Courses datasets were merged
to create a unified master dataset for analysis.
"""
)

paper.append("")


# ============================================================
# DESCRIPTIVE ANALYSIS
# ============================================================

paper.append(
    "10. DESCRIPTIVE ANALYSIS"
)

paper.append("-" * 80)

paper.append(
    """
The descriptive analysis examined the distribution of learners,
enrollments, course categories, course levels, course types and
gender participation.

The analysis also calculated learner-level engagement measures
including total enrollments, unique courses and learner activity
segments.

The following activity segments were used:

• Low Activity: 1–2 enrollments
• Moderate Activity: 3–5 enrollments
• High Activity: 6–10 enrollments
• Very High Activity: 11 or more enrollments

These segments provide a descriptive representation of learner
engagement intensity.
"""
)

paper.append("")


# ============================================================
# COURSE PREFERENCE ANALYSIS
# ============================================================

paper.append(
    "11. COURSE PREFERENCE ANALYSIS"
)

paper.append("-" * 80)

paper.append(
    """
Course enrollment behavior was analyzed using CourseCategory,
CourseType and CourseLevel.

The study examined:

• Overall category preference
• Overall course-level preference
• Course-type preference
• Age-group × category relationships
• Age-group × level relationships
• Gender × category relationships
• Gender × level relationships
• Top enrolled courses
• Course popularity
• Learner course diversity
"""
)

paper.append("")


# ============================================================
# TEMPORAL ANALYSIS
# ============================================================

paper.append(
    "12. TEMPORAL ANALYSIS"
)

paper.append("-" * 80)

paper.append(
    """
Transaction dates were analyzed to identify monthly and yearly
enrollment patterns.

The analysis includes:

• Monthly enrollment volume
• Yearly enrollment volume
• Month-over-month changes
• Peak enrollment period
• Lowest enrollment period
• Category-wise temporal behavior
• Course-level temporal behavior
"""
)

paper.append("")


# ============================================================
# CROSS-DIMENSIONAL ANALYSIS
# ============================================================

paper.append(
    "13. CROSS-DIMENSIONAL ANALYSIS"
)

paper.append("-" * 80)

paper.append(
    """
A major component of the research combines multiple dimensions
rather than examining each variable independently.

The analysis includes:

• Age × Gender
• Age × Category
• Age × Course Level
• Gender × Category
• Gender × Course Level
• Activity × Category
• Activity × Course Level
• Age × Gender × Activity

Heatmaps and comparative tables were used to identify differences
in enrollment behavior between learner segments.
"""
)

paper.append("")


# ============================================================
# STREAMLIT DASHBOARD
# ============================================================

paper.append(
    "14. INTERACTIVE DASHBOARD"
)

paper.append("-" * 80)

paper.append(
    """
An interactive Streamlit dashboard was developed to make the
analytical results easier to explore.

The dashboard contains:

• Overview
• Demographics
• Course Intelligence
• Learner Engagement
• Temporal Trends
• Cross-Dimensional Analysis
• Research Findings
• SDG 4 Analysis
• Methodology

Interactive filters allow users to examine the dataset by age group,
gender, course category, course level and course type.

The dashboard also provides downloadable filtered datasets and
research result files.
"""
)

paper.append("")


# ============================================================
# RESULTS
# ============================================================

paper.append(
    "15. RESULTS AND FINDINGS"
)

paper.append("-" * 80)

paper.append(
    """
The complete numerical findings are generated from the analyzed
EduPro dataset and are available in the Step 27 and Step 28
research reports.

The major analytical dimensions include learner demographics,
course preference, learner engagement, temporal enrollment and
cross-dimensional relationships.
"""
)

paper.append("")

paper.append(
    "FINAL RESEARCH INSIGHTS:"
)

paper.append(
    dataframe_to_text(
        insights,
        max_rows=20
    )
)

paper.append("")


# ============================================================
# RECOMMENDATIONS
# ============================================================

paper.append(
    "16. RECOMMENDATIONS"
)

paper.append("-" * 80)

paper.append(
    """
Based on the descriptive findings, the following types of
recommendations can be considered:

1. Monitor learner participation across demographic segments.

2. Use enrollment patterns to understand demand for different
   course categories and skill areas.

3. Track differences in course-level preferences across learner
   segments.

4. Monitor highly active and low-activity learner groups separately.

5. Use temporal enrollment trends for education program planning.

6. Continue monitoring gender participation and demographic
   differences.

7. Use interactive analytics dashboards for evidence-based
   education monitoring.
"""
)

paper.append("")

paper.append(
    dataframe_to_text(
        recommendations,
        max_rows=20
    )
)

paper.append("")


# ============================================================
# SDG 4
# ============================================================

paper.append(
    "17. SDG 4 ALIGNMENT"
)

paper.append("-" * 80)

paper.append(
    """
The project is aligned with selected aspects of Sustainable
Development Goal 4: Quality Education.

SDG 4 promotes inclusive and equitable quality education and
lifelong learning opportunities.

The project's descriptive analysis is particularly relevant to:

Target 4.3:
Equal access to affordable and quality technical, vocational and
tertiary education.

Target 4.4:
Relevant skills, including technical and vocational skills, for
employment, decent work and entrepreneurship.

Target 4.5:
Elimination of gender disparities and equal access to education
and vocational training.

The project does not claim to measure achievement of SDG 4.
Instead, it provides descriptive evidence about learner
participation and course enrollment behavior that can support
education-related planning.
"""
)

paper.append("")


# ============================================================
# GOVERNMENT STAKEHOLDER RELEVANCE
# ============================================================

paper.append(
    "18. GOVERNMENT STAKEHOLDER RELEVANCE"
)

paper.append("-" * 80)

paper.append(
    """
The analytical framework can support education stakeholders by
providing a structured view of learner participation and course
demand.

Potential applications include:

• Monitoring participation across learner age groups.

• Understanding gender-wise education participation.

• Identifying demand for skill-oriented course categories.

• Identifying differences in course-level preferences.

• Supporting digital education planning.

• Monitoring learner engagement patterns.

• Supporting evidence-based educational program evaluation.

These applications should be considered as analytical support
rather than direct policy conclusions.
"""
)

paper.append("")


# ============================================================
# LIMITATIONS
# ============================================================

paper.append(
    "19. LIMITATIONS"
)

paper.append("-" * 80)

if not limitations.empty:

    paper.append(
        dataframe_to_text(
            limitations,
            max_rows=20
        )
    )

else:

    paper.append(
        """
• The analysis is based on the available EduPro dataset.

• The dataset may not represent all online learners.

• Enrollment does not necessarily indicate course completion.

• Descriptive analytics cannot establish causality.

• Demographic variables are limited to the available fields.

• The analysis does not include learner satisfaction or learning
  outcome measures.
"""
    )

paper.append("")


# ============================================================
# FUTURE SCOPE
# ============================================================

paper.append(
    "20. FUTURE SCOPE"
)

paper.append("-" * 80)

if not future_scope.empty:

    paper.append(
        dataframe_to_text(
            future_scope,
            max_rows=20
        )
    )

else:

    paper.append(
        """
Future research can extend the project through:

• Course completion analysis
• Learner retention analysis
• Predictive analytics
• Recommendation systems
• Geographic analysis
• Learner satisfaction analysis
• Longitudinal learner behavior analysis
• Learning outcome analysis
"""
    )

paper.append("")


# ============================================================
# CONCLUSION
# ============================================================

paper.append(
    "21. CONCLUSION"
)

paper.append("-" * 80)

if conclusion:

    paper.append(
        conclusion
    )

else:

    paper.append(
        """
This research demonstrates how descriptive analytics can be used
to understand learner demographics and course enrollment behavior
on an online learning platform.

By integrating learner, course and transaction data, the project
provides a unified analytical view of enrollment behavior.

The analysis covers demographic participation, course preferences,
learner engagement, temporal trends and cross-dimensional
relationships.

The interactive Streamlit dashboard makes the analytical results
accessible through visual exploration and filtering.

Overall, the project demonstrates the practical application of
data analytics in educational environments and provides descriptive
evidence that can support education planning and SDG 4-related
analysis.
"""
    )

paper.append("")


# ============================================================
# FINAL STATEMENT
# ============================================================

paper.append(
    "22. FINAL RESEARCH STATEMENT"
)

paper.append("-" * 80)

paper.append(
    """
The EduPro Learner Analytics project demonstrates that structured
descriptive analysis can convert raw learner and enrollment data
into meaningful evidence about participation, course preferences
and learner engagement.

The combination of statistical analysis, visualization,
cross-dimensional analysis and an interactive dashboard provides
a complete analytical framework for understanding learner
enrollment behavior.

The project is intentionally descriptive and focuses on evidence
generation rather than prediction or automated decision-making.
"""
)

paper.append("")


# ============================================================
# SAVE
# ============================================================

os.makedirs(
    REPORT_DIR,
    exist_ok=True
)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "\n".join(paper)
    )


# ============================================================
# FINAL MESSAGE
# ============================================================

print()
print("=" * 80)
print("STEP 31 COMPLETED SUCCESSFULLY")
print("=" * 80)
print()
print(
    "Research paper generated:"
)
print(
    OUTPUT_FILE
)
print()
print(
    "The paper contains:"
)
print(
    "• Abstract"
)
print(
    "• Keywords"
)
print(
    "• Introduction"
)
print(
    "• Problem Statement"
)
print(
    "• Objectives"
)
print(
    "• Research Questions"
)
print(
    "• Dataset"
)
print(
    "• Methodology"
)
print(
    "• Data Preprocessing"
)
print(
    "• Analysis"
)
print(
    "• Results"
)
print(
    "• SDG 4"
)
print(
    "• Government Relevance"
)
print(
    "• Recommendations"
)
print(
    "• Limitations"
)
print(
    "• Future Scope"
)
print(
    "• Conclusion"
)
print()