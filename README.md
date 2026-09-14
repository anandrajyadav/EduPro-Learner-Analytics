# 📊 EduPro Learner Analytics

## Learner Demographics and Course Enrollment Behavior Analysis on EduPro

A professional descriptive analytics project for understanding learner demographics, course preferences, enrollment behavior, learner engagement, and temporal enrollment patterns using Python, Pandas, Plotly and Streamlit.

---

## 🎯 Project Overview

Online learning platforms generate large amounts of learner, course and enrollment data.

However, raw transaction data does not directly explain:

- Which learner age groups are most active
- How enrollment differs by gender
- Which course categories are most preferred
- Which course levels are popular
- How preferences differ across demographic groups
- How learner engagement is distributed
- How enrollment changes over time

This project applies descriptive analytics to the EduPro dataset to identify these patterns and presents the results through an interactive Streamlit dashboard.

---

## 🎓 Research Title

**Learner Demographics and Course Enrollment Behavior Analysis on EduPro**

### Research Type

Descriptive Analytics

### Academic Program

Master of Computer Applications (MCA)

---

## 🎯 Objectives

1. Analyze learner demographics.
2. Identify the most active age groups.
3. Analyze gender-wise enrollment participation.
4. Identify popular course categories.
5. Analyze course-level preferences.
6. Study age-wise course preferences.
7. Study gender-wise course preferences.
8. Analyze learner engagement.
9. Analyze monthly enrollment behavior.
10. Perform cross-dimensional analysis.
11. Develop an interactive analytics dashboard.
12. Examine relevance to SDG 4.

---

## ❓ Research Questions

- Which age groups are most active?
- How does enrollment participation differ by gender?
- Which course categories are most preferred?
- How do course preferences vary across age groups?
- How do course preferences vary across gender?
- Are different course levels preferred by different learner segments?
- How is learner engagement distributed?
- What temporal patterns exist in enrollment?
- Which demographic-course combinations show higher participation?
- How can these findings support education-related planning?

---

## 📊 Dataset

The project contains four primary datasets.

| Dataset | Records | Purpose |
|---|---:|---|
| Users | 3,000 | Learner demographic information |
| Teachers | 60 | Teacher expertise and experience |
| Courses | 60 | Course attributes |
| Transactions | 10,000 | Enrollment transactions |

### Important Relationships

```text
Users
  |
  | UserID
  ↓
Transactions
  |
  | CourseID
  ↓
Courses