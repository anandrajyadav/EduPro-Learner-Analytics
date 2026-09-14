# ============================================================
# EDUPRO PROJECT - FINAL VALIDATION
# STEP 30
# ============================================================

import os
import sys
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_DIR = os.getcwd()

DATA_DIR = os.path.join(
    PROJECT_DIR,
    "data"
)

OUTPUT_DIR = os.path.join(
    PROJECT_DIR,
    "outputs"
)

REPORT_DIR = os.path.join(
    OUTPUT_DIR,
    "reports"
)

CHART_DIR = os.path.join(
    OUTPUT_DIR,
    "charts"
)

DATA_FILE = os.path.join(
    DATA_DIR,
    "EduPro.xlsx"
)

APP_FILE = os.path.join(
    PROJECT_DIR,
    "app.py"
)


# ============================================================
# OUTPUT HELPERS
# ============================================================

errors = []
warnings = []
successes = []


def success(message):
    print(f"[PASS] {message}")
    successes.append(message)


def warning(message):
    print(f"[WARNING] {message}")
    warnings.append(message)


def error(message):
    print(f"[FAIL] {message}")
    errors.append(message)


# ============================================================
# HEADER
# ============================================================

print()
print("=" * 70)
print("EDUPRO LEARNER ANALYTICS - FINAL PROJECT VALIDATION")
print("=" * 70)
print()


# ============================================================
# 1. PROJECT STRUCTURE
# ============================================================

print("1. CHECKING PROJECT STRUCTURE")
print("-" * 70)

required_paths = {
    "data folder": DATA_DIR,
    "outputs folder": OUTPUT_DIR,
    "reports folder": REPORT_DIR,
    "charts folder": CHART_DIR,
    "EduPro.xlsx": DATA_FILE,
    "app.py": APP_FILE
}

for name, path in required_paths.items():

    if os.path.exists(path):
        success(f"{name} found")
    else:
        error(f"{name} missing: {path}")


# ============================================================
# 2. EXCEL WORKBOOK VALIDATION
# ============================================================

print()
print("2. CHECKING EXCEL WORKBOOK")
print("-" * 70)

if os.path.exists(DATA_FILE):

    try:

        excel = pd.ExcelFile(
            DATA_FILE
        )

        expected_sheets = [
            "Users",
            "Teachers",
            "Courses",
            "Transactions"
        ]

        for sheet in expected_sheets:

            if sheet in excel.sheet_names:
                success(
                    f"Excel sheet found: {sheet}"
                )
            else:
                error(
                    f"Missing Excel sheet: {sheet}"
                )

    except Exception as e:

        error(
            f"Could not open Excel workbook: {e}"
        )


# ============================================================
# 3. LOAD DATA
# ============================================================

print()
print("3. LOADING DATASETS")
print("-" * 70)

try:

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

    success(
        f"Users loaded: {len(users):,} rows"
    )

    success(
        f"Teachers loaded: {len(teachers):,} rows"
    )

    success(
        f"Courses loaded: {len(courses):,} rows"
    )

    success(
        f"Transactions loaded: {len(transactions):,} rows"
    )

except Exception as e:

    error(
        f"Dataset loading failed: {e}"
    )

    sys.exit(1)


# ============================================================
# 4. ROW COUNT VALIDATION
# ============================================================

print()
print("4. CHECKING DATASET SIZE")
print("-" * 70)

expected_sizes = {
    "Users": 3000,
    "Teachers": 60,
    "Courses": 60,
    "Transactions": 10000
}

actual_sizes = {
    "Users": len(users),
    "Teachers": len(teachers),
    "Courses": len(courses),
    "Transactions": len(transactions)
}

for dataset, expected in expected_sizes.items():

    actual = actual_sizes[dataset]

    if actual == expected:

        success(
            f"{dataset}: {actual:,} rows"
        )

    else:

        warning(
            f"{dataset}: expected {expected:,}, found {actual:,}"
        )


# ============================================================
# 5. REQUIRED COLUMNS
# ============================================================

print()
print("5. CHECKING REQUIRED COLUMNS")
print("-" * 70)

required_columns = {

    "Users": [
        "UserID",
        "UserName",
        "Age",
        "Gender",
        "Email"
    ],

    "Teachers": [
        "TeacherID",
        "TeacherName",
        "Age",
        "Gender",
        "Expertise",
        "YearsOfExperience",
        "TeacherRating"
    ],

    "Courses": [
        "CourseID",
        "CourseName",
        "CourseCategory",
        "CourseType",
        "CourseLevel",
        "CoursePrice",
        "CourseDuration",
        "CourseRating"
    ],

    "Transactions": [
        "TransactionID",
        "UserID",
        "CourseID",
        "TransactionDate",
        "Amount",
        "PaymentMethod",
        "TeacherID"
    ]
}

datasets = {
    "Users": users,
    "Teachers": teachers,
    "Courses": courses,
    "Transactions": transactions
}

for dataset_name, columns in required_columns.items():

    df = datasets[dataset_name]

    for column in columns:

        if column in df.columns:

            success(
                f"{dataset_name}.{column}"
            )

        else:

            error(
                f"Missing column: {dataset_name}.{column}"
            )


# ============================================================
# 6. DUPLICATE ID VALIDATION
# ============================================================

print()
print("6. CHECKING DUPLICATE IDs")
print("-" * 70)

id_checks = {
    "Users.UserID": (
        users,
        "UserID"
    ),

    "Teachers.TeacherID": (
        teachers,
        "TeacherID"
    ),

    "Courses.CourseID": (
        courses,
        "CourseID"
    ),

    "Transactions.TransactionID": (
        transactions,
        "TransactionID"
    )
}

for name, (df, column) in id_checks.items():

    duplicates = df[column].duplicated().sum()

    if duplicates == 0:

        success(
            f"{name}: no duplicate IDs"
        )

    else:

        error(
            f"{name}: {duplicates} duplicate IDs"
        )


# ============================================================
# 7. REFERENTIAL INTEGRITY
# ============================================================

print()
print("7. CHECKING REFERENTIAL INTEGRITY")
print("-" * 70)

user_ids = set(
    users["UserID"]
)

course_ids = set(
    courses["CourseID"]
)

teacher_ids = set(
    teachers["TeacherID"]
)

transaction_user_ids = set(
    transactions["UserID"]
)

transaction_course_ids = set(
    transactions["CourseID"]
)

transaction_teacher_ids = set(
    transactions["TeacherID"]
)


missing_users = (
    transaction_user_ids
    - user_ids
)

missing_courses = (
    transaction_course_ids
    - course_ids
)

missing_teachers = (
    transaction_teacher_ids
    - teacher_ids
)


if not missing_users:

    success(
        "All transaction UserIDs exist in Users"
    )

else:

    error(
        f"Missing UserIDs: {len(missing_users)}"
    )


if not missing_courses:

    success(
        "All transaction CourseIDs exist in Courses"
    )

else:

    error(
        f"Missing CourseIDs: {len(missing_courses)}"
    )


if not missing_teachers:

    success(
        "All transaction TeacherIDs exist in Teachers"
    )

else:

    error(
        f"Missing TeacherIDs: {len(missing_teachers)}"
    )


# ============================================================
# 8. MASTER DATASET VALIDATION
# ============================================================

print()
print("8. BUILDING MASTER DATASET")
print("-" * 70)

try:

    users_temp = users.copy()
    courses_temp = courses.copy()
    transactions_temp = transactions.copy()

    users_temp["UserID"] = (
        users_temp["UserID"]
        .astype(str)
        .str.strip()
    )

    courses_temp["CourseID"] = (
        courses_temp["CourseID"]
        .astype(str)
        .str.strip()
    )

    transactions_temp["UserID"] = (
        transactions_temp["UserID"]
        .astype(str)
        .str.strip()
    )

    transactions_temp["CourseID"] = (
        transactions_temp["CourseID"]
        .astype(str)
        .str.strip()
    )

    master = transactions_temp.merge(
        users_temp[
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

    master = master.merge(
        courses_temp[
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

    success(
        f"Master dataset created: {len(master):,} rows"
    )

    if len(master) == len(transactions):

        success(
            "Master dataset preserved all transactions"
        )

    else:

        error(
            "Master dataset row count does not match transactions"
        )

except Exception as e:

    error(
        f"Master dataset creation failed: {e}"
    )

    master = pd.DataFrame()


# ============================================================
# 9. MASTER DATA QUALITY
# ============================================================

if not master.empty:

    print()
    print("9. CHECKING MASTER DATA QUALITY")
    print("-" * 70)

    duplicate_rows = (
        master.duplicated().sum()
    )

    if duplicate_rows == 0:

        success(
            "No duplicate master rows"
        )

    else:

        warning(
            f"Duplicate master rows: {duplicate_rows}"
        )

    important_columns = [
        "UserID",
        "CourseID",
        "TransactionDate",
        "Age",
        "Gender",
        "CourseCategory",
        "CourseLevel"
    ]

    for column in important_columns:

        if column not in master.columns:
            continue

        missing = (
            master[column]
            .isna()
            .sum()
        )

        if missing == 0:

            success(
                f"{column}: no missing values"
            )

        else:

            warning(
                f"{column}: {missing:,} missing values"
            )


# ============================================================
# 10. DATE VALIDATION
# ============================================================

print()
print("10. CHECKING TRANSACTION DATES")
print("-" * 70)

if "TransactionDate" in transactions.columns:

    dates = pd.to_datetime(
        transactions["TransactionDate"],
        errors="coerce"
    )

    invalid_dates = dates.isna().sum()

    if invalid_dates == 0:

        success(
            "All transaction dates are valid"
        )

    else:

        warning(
            f"Invalid/missing dates: {invalid_dates:,}"
        )

    if dates.notna().any():

        success(
            f"Date range: {dates.min().date()} to {dates.max().date()}"
        )


# ============================================================
# 11. REPORT FILE VALIDATION
# ============================================================

print()
print("11. CHECKING RESEARCH REPORTS")
print("-" * 70)

required_reports = [

    "step24_key_findings.csv",

    "step24_research_question_summary.csv",

    "step25_final_research_findings.csv",

    "step25_research_questions.csv",

    "step25_research_objectives.csv",

    "step26_government_stakeholder_analysis.csv",

    "step26_sdg4_mapping.csv",

    "step27_final_research_insights.csv",

    "step27_recommendations.csv",

    "step27_research_conclusion.txt",

    "step27_limitations.csv",

    "step27_future_scope.csv",

    "step28_research_paper_tables.xlsx",

    "step28_master_research_results.csv",

    "step28_research_paper_results.txt"

]

for filename in required_reports:

    path = os.path.join(
        REPORT_DIR,
        filename
    )

    if os.path.exists(path):

        success(
            f"Report found: {filename}"
        )

    else:

        warning(
            f"Report missing: {filename}"
        )


# ============================================================
# 12. CHART VALIDATION
# ============================================================

print()
print("12. CHECKING GENERATED CHARTS")
print("-" * 70)

if os.path.exists(CHART_DIR):

    chart_files = [
        f
        for f in os.listdir(CHART_DIR)
        if f.lower().endswith(
            (".png", ".jpg", ".jpeg")
        )
    ]

    if len(chart_files) > 0:

        success(
            f"{len(chart_files)} chart files found"
        )

    else:

        warning(
            "No chart files found"
        )


# ============================================================
# 13. APP CODE CHECK
# ============================================================

print()
print("13. CHECKING STREAMLIT APP")
print("-" * 70)

if os.path.exists(APP_FILE):

    try:

        with open(
            APP_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            app_code = f.read()

        required_app_features = [

            "streamlit",

            "st.set_page_config",

            "st.sidebar",

            "st.tabs",

            "st.metric",

            "st.plotly_chart",

            "st.download_button",

            "AgeGroup",

            "CourseCategory",

            "CourseLevel",

            "Gender"

        ]

        for feature in required_app_features:

            if feature in app_code:

                success(
                    f"Dashboard feature found: {feature}"
                )

            else:

                warning(
                    f"Dashboard feature not detected: {feature}"
                )

    except Exception as e:

        error(
            f"Could not inspect app.py: {e}"
        )


# ============================================================
# 14. PACKAGE VALIDATION
# ============================================================

print()
print("14. CHECKING PYTHON PACKAGES")
print("-" * 70)

required_packages = [
    "pandas",
    "numpy",
    "openpyxl",
    "plotly",
    "streamlit"
]

for package in required_packages:

    try:

        __import__(package)

        success(
            f"Package installed: {package}"
        )

    except ImportError:

        error(
            f"Package missing: {package}"
        )


# ============================================================
# 15. PROJECT SUMMARY
# ============================================================

print()
print("=" * 70)
print("PROJECT SUMMARY")
print("=" * 70)

print()

print(
    f"Users              : {len(users):,}"
)

print(
    f"Teachers            : {len(teachers):,}"
)

print(
    f"Courses             : {len(courses):,}"
)

print(
    f"Transactions        : {len(transactions):,}"
)

if not master.empty:

    print(
        f"Master Dataset      : {len(master):,}"
    )

print(
    f"Research Reports    : {len(required_reports)} checked"
)

if os.path.exists(CHART_DIR):

    print(
        f"Charts Generated    : {len(chart_files)}"
    )


# ============================================================
# FINAL RESULT
# ============================================================

print()
print("=" * 70)
print("FINAL VALIDATION RESULT")
print("=" * 70)

print()

print(
    f"PASS     : {len(successes)}"
)

print(
    f"WARNINGS : {len(warnings)}"
)

print(
    f"FAIL     : {len(errors)}"
)

print()

if len(errors) == 0:

    print(
        "🎉 PROJECT VALIDATION PASSED"
    )

    print(
        "Your EduPro project is ready for final presentation."
    )

else:

    print(
        "⚠️ PROJECT VALIDATION FOUND ISSUES"
    )

    print(
        "Fix the FAIL items before final submission."
    )


# ============================================================
# SAVE VALIDATION REPORT
# ============================================================

os.makedirs(
    REPORT_DIR,
    exist_ok=True
)

validation_file = os.path.join(
    REPORT_DIR,
    "step30_final_validation_report.txt"
)

with open(
    validation_file,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "EDUPRO FINAL PROJECT VALIDATION REPORT\n"
    )

    f.write(
        "=" * 60 + "\n\n"
    )

    f.write(
        f"PASS     : {len(successes)}\n"
    )

    f.write(
        f"WARNINGS : {len(warnings)}\n"
    )

    f.write(
        f"FAIL     : {len(errors)}\n\n"
    )

    f.write(
        "PROJECT STRUCTURE\n"
    )

    f.write(
        "-" * 60 + "\n"
    )

    for item in successes:

        f.write(
            "[PASS] " + item + "\n"
        )

    for item in warnings:

        f.write(
            "[WARNING] " + item + "\n"
        )

    for item in errors:

        f.write(
            "[FAIL] " + item + "\n"
        )

    f.write(
        "\nFINAL STATUS\n"
    )

    if len(errors) == 0:

        f.write(
            "PROJECT VALIDATION PASSED\n"
        )

    else:

        f.write(
            "PROJECT VALIDATION REQUIRES FIXES\n"
        )


print()
print(
    f"Validation report saved to:\n{validation_file}"
)

print()
print("=" * 70)
print("STEP 30 VALIDATION COMPLETED")
print("=" * 70)