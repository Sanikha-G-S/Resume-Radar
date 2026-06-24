import streamlit as st
import pdfplumber
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# DATABASE SETUP
# -----------------------------
conn = sqlite3.connect("resume_analysis.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score REAL,
    missing_skills TEXT
)
""")

conn.commit()
conn.close()

# -----------------------------
# SKILLS DATABASE
# -----------------------------
SKILLS_DB = [
    "python",
    "java",
    "c",
    "c++",
    "html",
    "css",
    "sql",
    "dbms",
    "data structures",
    "algorithms",
    "oop",
    "linux",
    "ubuntu",
    "oracle",
    "web development",
    "git",
    "docker",
    "aws",
    "fastapi",
    "flask",
    "django",
    "mongodb",
    "postgresql",
    "machine learning",
    "deep learning"
]

# -----------------------------
# PAGE TITLE
# -----------------------------
st.title("📄 Smart Resume Analyzer")

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description Here"
)

# -----------------------------
# MAIN LOGIC
# -----------------------------
if uploaded_file:

    text = ""

    try:
        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text.lower()

    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        st.stop()

    # -----------------------------
    # DETECT RESUME SKILLS
    # -----------------------------
    found_skills = []

    for skill in SKILLS_DB:
        if skill in text:
            found_skills.append(skill)

    st.subheader("✅ Skills Detected")

    if found_skills:
        for skill in found_skills:
            st.markdown(f"✅ {skill}")
    else:
        st.warning("No skills detected.")

    # -----------------------------
    # ATS ANALYSIS
    # -----------------------------
    if job_description.strip():

        jd_text = job_description.lower()

        jd_skills = []

        for skill in SKILLS_DB:
            if skill in jd_text:
                jd_skills.append(skill)

        missing_skills = []

        for skill in jd_skills:
            if skill not in found_skills:
                missing_skills.append(skill)

        # -----------------------------
        # ATS SCORE
        # -----------------------------
        vectorizer = TfidfVectorizer()

        vectors = vectorizer.fit_transform(
            [text, jd_text]
        )

        score = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]

        ats_score = round(score * 100, 2)

        st.subheader("📊 ATS Match Score")

        st.metric(
            label="Score",
            value=f"{ats_score}%"
        )

        # -----------------------------
        # SAVE TO DATABASE
        # -----------------------------
        conn = sqlite3.connect("resume_analysis.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO analysis(score, missing_skills)
            VALUES (?, ?)
            """,
            (
                ats_score,
                ", ".join(missing_skills)
            )
        )

        conn.commit()
        conn.close()

        # -----------------------------
        # MISSING SKILLS
        # -----------------------------
        st.subheader("❌ Missing Skills")

        if missing_skills:

            for skill in missing_skills:
                st.markdown(f"❌ {skill}")

        else:
            st.success(
                "Your resume matches all detected job skills!"
            )

        # -----------------------------
        # RECOMMENDATIONS
        # -----------------------------
        st.subheader("💡 Recommendations")

        if missing_skills:

            st.write(
                "Consider adding projects, certifications, or experience related to:"
            )

            for skill in missing_skills:
                st.write(f"• {skill}")

        else:
            st.success(
                "Excellent match for this job description."
            )

    # -----------------------------
    # RESUME PREVIEW
    # -----------------------------
    st.subheader("📄 Resume Preview")

    st.text_area(
        "Extracted Text",
        text,
        height=300
    )

# -----------------------------
# ANALYSIS HISTORY
# -----------------------------
st.subheader("📚 Previous Analyses")

conn = sqlite3.connect("resume_analysis.db")
cursor = conn.cursor()

cursor.execute("""
SELECT score, missing_skills
FROM analysis
ORDER BY id DESC
LIMIT 5
""")

rows = cursor.fetchall()

if rows:

    for row in rows:

        score = row[0]
        missing = row[1]

        st.write(
            f"Score: {score}% | Missing Skills: {missing}"
        )

else:
    st.info("No previous analyses yet.")

conn.close()