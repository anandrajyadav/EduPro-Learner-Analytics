<div align="center">

<!-- ═══════════════════════════════════════════════════════════════════════ -->

<!--                         PREMIUM HERO                                    -->

<!-- ═══════════════════════════════════════════════════════════════════════ -->

<a href="https://github.com/anandrajyadav/EduPro-Learner-Analytics">
  <img src="assets/edupro-3d-motion.gif" alt="EduPro Learner Analytics — 3D Motion Hero" width="100%">
</a>

📊 EduPro Learner Analytics

Learner Demographics & Course Enrollment Behavior Analysis

<p>
  <b>Descriptive Educational Data Analytics • Interactive Visualization • Research</b>
</p>

<p>
  <a href="https://github.com/anandrajyadav/EduPro-Learner-Analytics">
    <img src="https://img.shields.io/badge/GitHub-Repository-111827?style=for-the-badge&logo=github&logoColor=white">
  </a>
  <a href="https://zenodo.org/records/22816169">
    <img src="https://img.shields.io/badge/Research-DOI-7C3AED?style=for-the-badge&logo=doi&logoColor=white">
  </a>
  <img src="https://img.shields.io/badge/Python-3.x-2563EB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Pandas-Analytics-150458?style=for-the-badge&logo=pandas&logoColor=white">
  <img src="https://img.shields.io/badge/Plotly-Visualization-3F4F75?style=for-the-badge&logo=plotly&logoColor=white">
  <img src="https://img.shields.io/badge/Streamlit-Interactive%20Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">
</p>

<p>
  <img src="https://img.shields.io/badge/Analytics-Descriptive-0F766E?style=flat-square">
  <img src="https://img.shields.io/badge/Research-SDG%204-0EA5E9?style=flat-square">
  <img src="https://img.shields.io/badge/Status-Completed-16A34A?style=flat-square">
  <img src="https://img.shields.io/badge/Repository-Public-111827?style=flat-square">
</p>

<br>

Anand Raj Yadav · Shruti Ravindra Gaikwad
MCA Students · DYPIMCAM · Pune, Maharashtra, India

<br>

Turning educational data into visual evidence, research insight, and an interactive analytical experience.

</div>

🧭 Explore



Section

What you'll find

🎯

Overview

Problem, purpose & scope

🔬

Research

Questions & analytical framework

🧩

Data

Dataset architecture & entities

🛠️

Technology

Tools & implementation stack

📊

Dashboard

Analytical views & visualizations

🔄

Methodology

End-to-end research workflow

🎓

Journey

10-day development timeline

🌍

SDG 4

Education-oriented context

📄

Publication

Research paper & DOI

🚀

Setup

Run the project locally

🎯 Project Overview

EduPro Learner Analytics is a descriptive analytics and educational data analysis project designed to understand who learners are, what they enroll in, and how enrollment behavior varies across demographic and course dimensions.

The project transforms learner, teacher, course, and transaction data into:

📌 Demographic insights

📚 Course preference analysis

👥 Gender-wise comparisons

🎓 Age-group behavior analysis

📈 Enrollment trends

🔥 Cross-dimensional heatmaps

📊 Interactive visual analytics

🧠 Evidence-based descriptive insights

🌍 SDG 4-oriented educational planning context

<div align="center">

DATA → ANALYSIS → VISUALIZATION → INSIGHT → RESEARCH

</div>

Scope: This project focuses on descriptive analytics. It does not make individual learner predictions, recommendations, or monetization decisions.

✨ Why EduPro?

Educational platforms generate large amounts of learner and enrollment data. Raw records alone do not clearly communicate:

Which learner age groups are most active?

How does enrollment participation differ across genders?

Which course categories attract different learner segments?

Do age groups show different preferences for beginner, intermediate, or advanced courses?

How concentrated is enrollment among active learners?

What patterns can be communicated through an interactive analytics dashboard?

EduPro addresses these questions through a structured analytics workflow.

🔬 Research Questions

<table>
<tr>
<td width="50%">

RQ1 — Age & Activity

Which age groups are most active in course enrollment?

RQ2 — Gender Participation

How do enrollment patterns differ by gender?

RQ3 — Category Preferences

What course categories are preferred by different learner segments?

</td>
<td width="50%">

RQ4 — Course Level

Are beginner, intermediate, and advanced courses more popular among specific age groups?

RQ5 — Engagement Distribution

How are enrollments distributed across learners and how concentrated is activity among active users?

RQ6 — Temporal Behavior

How does enrollment activity change over time?

</td>
</tr>
</table>

🧩 Dataset Architecture

The analysis uses four logical entities connected through relational identifiers:

                           ┌─────────────────────┐
                           │        USERS        │
                           ├─────────────────────┤
                           │ UserID              │
                           │ UserName            │
                           │ Age                 │
                           │ Gender              │
                           │ Email               │
                           └──────────┬──────────┘
                                      │ UserID
                                      ▼
                           ┌─────────────────────┐
                           │    TRANSACTIONS     │
                           ├─────────────────────┤
                           │ TransactionID       │
                           │ UserID              │
                           │ CourseID            │
                           │ TransactionDate     │
                           │ Amount              │
                           │ PaymentMethod       │
                           │ TeacherID           │
                           └───────┬───────┬─────┘
                                   │       │
                             CourseID       │ TeacherID
                                   │       │
                         ┌─────────▼───┐ ┌─▼───────────────┐
                         │   COURSES   │ │    TEACHERS     │
                         ├─────────────┤ ├─────────────────┤
                         │ CourseID    │ │ TeacherID       │
                         │ CourseName  │ │ TeacherName     │
                         │ Category    │ │ Expertise       │
                         │ Type        │ │ Experience      │
                         │ Level       │ │ Rating          │
                         │ Rating      │ │ Gender          │
                         └─────────────┘ └─────────────────┘

📦 Workbook Entities

Sheet

Records

Analytical Role

👤 Users

3,000

Learner demographics

👨‍🏫 Teachers

60

Instructor information

📚 Courses

60

Course metadata

💳 Transactions

10,000

Enrollment / transaction behavior

Core Fields

Users
UserID · UserName · Age · Gender · Email

Teachers
TeacherID · TeacherName · Age · Gender · Expertise · YearsOfExperience · TeacherRating

Courses
CourseID · CourseName · CourseCategory · CourseType · CourseLevel · CoursePrice · CourseDuration · CourseRating

Transactions
TransactionID · UserID · CourseID · TransactionDate · Amount · PaymentMethod · TeacherID

🛠️ Technology Stack

<div align="center">

Layer

Technology

🐍 Programming

Python

🧮 Data Manipulation

Pandas · NumPy

📊 Visualization

Plotly · Matplotlib · Seaborn

🖥️ Dashboard

Streamlit

📗 Excel Processing

OpenPyXL

📄 Research Document

Python-docx

🔀 Version Control

Git · GitHub

🌐 Research Repository

Zenodo

🔎 Research Type

Descriptive Analytics

</div>

🔄 Analytical Methodology

<p align="center">
  <img src="assets/research-pipeline-motion.gif" alt="EduPro Research Pipeline" width="100%">
</p>

┌─────────────────────────┐
│  Raw Educational Data   │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Data Loading            │
│ Quality Validation      │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Referential Integrity   │
│ & Data Consistency      │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Data Integration        │
│ Users ↔ Transactions    │
│ Courses ↔ Teachers      │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Age-Band Creation       │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Exploratory Analysis    │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Demographics            │
│ Course Preferences      │
│ Engagement & Time       │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Cross-Dimensional       │
│ Analysis & Heatmaps     │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Interactive Streamlit   │
│ Dashboard               │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Research Interpretation │
│ & Publication           │
└─────────────────────────┘

Age Bands

<18     →     18–25     →     26–35     →     36–45     →     45+

Analytical Dimensions

Age

Gender

Course Category

Course Type

Course Level

Enrollment Count

Transaction Date

Learner Engagement

Course / Teacher Attributes

📊 Interactive Dashboard

The Streamlit dashboard is designed as an interactive analytical interface rather than a static report.

01 · Overview

Overall enrollment KPIs

High-level demographic summary

Course activity overview

02 · Demographics

Age-group distribution

Gender participation

Enrollment by demographic segments

03 · Course Intelligence

Category popularity

Course type distribution

Course-level preferences

Course ratings and enrollment context

04 · Learner Behavior

Enrollment frequency

Active learner distribution

Courses per learner

Engagement concentration

05 · Cross-Dimensional Analysis

Age × Category

Age × Level

Gender × Level

Segment comparisons

06 · Insights

Evidence-based descriptive observations

Educational planning context

SDG 4-oriented interpretation

🎞️ Motion Preview

<div align="center">

<img src="assets/edupro-3d-motion.gif" alt="EduPro 3D Animated Experience" width="90%">

<br><br>

A GitHub-friendly 3D-inspired animated research presentation

</div>

📸 Dashboard Screenshots

<div align="center">

🖥️ Dashboard Overview

<img src="screenshots/dashboard-overview.png" alt="Dashboard Overview" width="95%">

👥 Demographics Analysis

<img src="screenshots/demographics-analysis.png" alt="Demographics Analysis" width="95%">

📚 Course Intelligence

<img src="screenshots/course-intelligence.png" alt="Course Intelligence" width="95%">

👤 Learner Behavior

<img src="screenshots/learner-behavior.png" alt="Learner Behavior" width="95%">

💡 Insights Analysis

<img src="screenshots/insights-analysis.png" alt="Insights Analysis" width="95%">

🧪 Methodology & Data Validation

<img src="screenshots/methodology-data-validation.png" alt="Methodology and Data Validation" width="95%">

</div>

📈 Key Analytical Components

👥 Demographic Analysis

Learners are examined across predefined age groups and gender dimensions to understand participation patterns.

📚 Course Preference Analysis

Enrollment activity is analyzed across:

Course categories

Course types

Course levels

Learner age groups

Gender groups

🔥 Cross-Tabulation & Heatmaps

Age Group × Course Category
Age Group × Course Level
Gender    × Course Level

These comparisons help communicate differences across learner segments.

👤 Learner Engagement

The project examines:

Enrollment frequency

Average courses per learner

Active learner concentration

Distribution of enrollment activity

📅 Temporal Analysis

Transaction dates are transformed to support:

Monthly enrollment trends

Time-based activity comparisons

Periodic behavior visualization

🧪 Data Validation & Quality

Data quality is treated as a core part of the analytical workflow.

Validation Checklist

✅ Missing-value checks

✅ Duplicate checks

✅ Data-type validation

✅ UserID referential integrity

✅ CourseID referential integrity

✅ TeacherID referential integrity

✅ Date parsing validation

✅ Numeric field validation

✅ Consistency checks across integrated datasets

The repository includes:

final_validation.py

for project-level validation.

▶️ Run the Project Locally

1️⃣ Clone

git clone https://github.com/anandrajyadav/EduPro-Learner-Analytics.git
cd EduPro-Learner-Analytics

2️⃣ Create a virtual environment

Windows

python -m venv .venv
.venv\Scripts\activate

macOS / Linux

python3 -m venv .venv
source .venv/bin/activate

3️⃣ Install dependencies

python -m pip install -r requirements.txt

4️⃣ Add the dataset

Place the project workbook at:

data/EduPro.xlsx

The original workbook is intentionally excluded from Git tracking through .gitignore because it contains direct learner identifiers such as names and email addresses.

5️⃣ Run validation

python final_validation.py

6️⃣ Launch the dashboard

streamlit run app.py

The dashboard will open in your browser.

📁 Repository Structure

EduPro-Learner-Analytics/
│
├── 📄 app.py
├── 📄 analysis.py
├── 📄 final_validation.py
├── 📄 create_research_docx.py
├── 📄 research_paper.py
├── 📄 README.md
├── 📄 requirements.txt
├── 📄 .gitignore
│
├── 🎞️ assets/
│   ├── edupro-3d-motion.gif
│   └── research-pipeline-motion.gif
│
├── 📸 screenshots/
│   ├── dashboard-overview.png
│   ├── demographics-analysis.png
│   ├── course-intelligence.png
│   ├── learner-behavior.png
│   ├── insights-analysis.png
│   └── methodology-data-validation.png
│
├── 🔐 data/
│   └── EduPro.xlsx
│
└── 📦 outputs/
    └── reports/
        ├── research paper
        ├── presentation
        ├── speaker notes
        └── analytical reports

🌍 SDG 4 — Quality Education

The project is aligned with the analytical context of UN Sustainable Development Goal 4: Quality Education.

EduPro provides descriptive evidence about:

Learner participation

Course enrollment behavior

Demographic engagement

Course-level preferences

Gender participation

Educational content demand

These insights can provide an analytical foundation for discussions around learner access, skills development, participation patterns, and educational planning.

Important: The project does not claim to measure or prove achievement of SDG 4. It provides descriptive analytics that can support education-related analysis and planning.

🧠 Research & Publication

📄 Research Paper

Learner Demographics and Course Enrollment Behavior Analysis on EduPro

Authors

Anand Raj Yadav

Shruti Ravindra Gaikwad

Institution: DYPIMCAM, Pune, Maharashtra, India

🔖 DOI

<div align="center">

<a href="https://doi.org/10.5281/zenodo.22816169">
  <img src="https://img.shields.io/badge/DOI-10.5281%2Fzenodo.22816169-7C3AED?style=for-the-badge&logo=doi&logoColor=white">
</a>

<br><br>

<a href="https://zenodo.org/records/22816169">📄 View Published Research Record</a>

</div>

The publication provides a formal research record for the analytical work, methodology, findings framework, limitations, and educational implications.

🎓 10-Day Development Journey

This project was developed through a structured 10-day analytics-to-publication workflow.

Day

Milestone

01

Problem definition & research questions

02

Dataset exploration & validation

03

Preprocessing & date transformation

04

Demographic analysis

05

Course preference analysis

06

Cross-dimensional analysis

07

Engagement & temporal analysis

08

Advanced descriptive summaries

09

Streamlit dashboard development

10

Research paper, SDG framing, validation, documentation & publication

<div align="center">

10 DAYS · 1 RESEARCH PROJECT · DATA → DASHBOARD → PUBLICATION

</div>

🎯 Learning Outcomes

This project demonstrates practical experience with:

Exploratory Data Analysis

Data cleaning and validation

Relational data integration

Pandas data manipulation

Statistical summaries

Data visualization

Interactive dashboard development

Research question formulation

Analytical storytelling

Technical documentation

Git / GitHub workflow

Research publication workflow

🚀 Future Scope

Possible future extensions include:

Larger and more diverse datasets

Longitudinal learner behavior analysis

Statistical hypothesis testing

Cohort analysis

Course completion analysis

Learning outcome analysis

Advanced segmentation

Predictive modeling as a separate research phase

Responsible recommendation systems

Integration with additional educational datasets

These extensions would require additional data and methodological validation beyond the current descriptive scope.

⚠️ Limitations

The current analysis has several limitations:

The dataset represents the available EduPro sample and should not automatically be generalized to all learners.

The project is primarily descriptive and does not establish causal relationships.

Enrollment does not necessarily imply course completion or learning success.

Demographic patterns should be interpreted within the limits of the available sample.

Direct identifiers are not required for public analytical outputs and should remain protected.

The analysis does not independently establish educational policy outcomes.

🔐 Data Privacy

The project follows a privacy-conscious repository approach.

The source workbook contains fields such as:

UserName
Email

These direct identifiers are not intended for public GitHub distribution.

The .gitignore configuration excludes:

data/EduPro.xlsx

Public outputs should contain aggregated or anonymized analytical information rather than personally identifiable learner records.

📚 Project Deliverables

Deliverable

Status

🐍 Python analytical scripts

✅

🖥️ Streamlit dashboard

✅

🧪 Data validation

✅

📄 Research paper

✅

🎤 Presentation

✅

📝 Speaker notes

✅

📸 Dashboard screenshots

✅

🎞️ 3D-inspired motion assets

✅

🌐 Research publication record

✅

💡 What This Project Demonstrates

<div align="center">

RAW DATA

↓

STRUCTURED ANALYSIS

↓

VISUAL EVIDENCE

↓

INTERACTIVE DASHBOARD

↓

RESEARCH COMMUNICATION

</div>

EduPro is designed not merely as a dashboard, but as a complete educational data analytics workflow connecting technical implementation with research-oriented interpretation.

👨‍💻 Authors

<table>
<tr>
<td width="50%" align="center">

Anand Raj Yadav

MCA Student
Aspiring Data Analyst
Data Analytics & Business Intelligence

</td>
<td width="50%" align="center">

Shruti Ravindra Gaikwad

MCA Student
Data Analytics & Business Intelligence

</td>
</tr>
</table>

<div align="center">

DYPIMCAM · Pune, Maharashtra, India

</div>

🔗 Connect & Explore

<div align="center">

<a href="https://github.com/anandrajyadav/EduPro-Learner-Analytics">
  <img src="https://img.shields.io/badge/Explore%20GitHub-111827?style=for-the-badge&logo=github&logoColor=white">
</a>

<a href="https://zenodo.org/records/22816169">
  <img src="https://img.shields.io/badge/Read%20Research-7C3AED?style=for-the-badge&logo=doi&logoColor=white">
</a>

</div>

<div align="center">

⭐ Like the project?

Star the repository and explore the complete analytics workflow.

<br>

<img src="https://capsule-render.vercel.app/api?type=waving&height=120&section=footer&text=Built%20with%20Data%20%7C%20Curiosity%20%7C%20Research&fontSize=22&fontColor=ffffff&animation=twinkling&fontAlignY=65">

<br>

Python · Pandas · NumPy · Plotly · Streamlit · GitHub · Zenodo

</div>
