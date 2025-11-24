"""
Modern, cleaned App.py (2025-safe)
- Uses pypdf for PDF extraction and page count
- Uses resume_parser.parse_resume() as provided
- No pytube / no external YouTube title fetching (embed URLs directly)
- Single DB initialization and consistent schema usage
- Improved skill classification (keyword sets + resume-text fallback)
- Faster progress update (no slow loops)
- Comments for clarity
"""
import streamlit as st
import pandas as pd
import base64
import time
import datetime
import random
import os
from PIL import Image
import sqlite3

from pypdf import PdfReader  # modern maintained pypdf
from Courses import (
    ds_course, web_course, android_course, ios_course, uiux_course,
    resume_videos, interview_videos
)

# local parser (uses spaCy 3.x or custom logic inside resume_parser.py)
from resume_parser import parse_resume

# --- DATABASE SETUP (single initialization) ---
DB_TABLE = "user_data"

def get_connection():
    conn = sqlite3.connect("resume_data.db", check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

# Initialize single connection using secrets
connection = get_connection()
cursor = connection.cursor()

# Create table if not exists (keeps original structure)
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {DB_TABLE} (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Email_ID TEXT NOT NULL,
    resume_score TEXT NOT NULL,
    Timestamp TEXT NOT NULL,
    Page_no TEXT NOT NULL,
    Predicted_Field BLOB NOT NULL,
    User_level BLOB NOT NULL,
    Actual_skills BLOB NOT NULL,
    Recommended_skills BLOB NOT NULL,
    Recommended_courses BLOB NOT NULL
);
"""
cursor.execute(create_table_sql)



# --- HELPERS ---

def extract_text_and_count(pdf_path: str):
    """Extract concatenated page text and return text + page count using pypdf (fast)."""
    reader = PdfReader(pdf_path)
    page_texts = []
    for p in reader.pages:
        page_texts.append(p.extract_text() or "")
    full_text = "\n".join(page_texts)
    return full_text, len(reader.pages)


def get_table_download_link(df: pd.DataFrame, filename: str, link_text: str):
    """Return HTML download link for a dataframe as CSV (safe, client-side)."""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{link_text}</a>'
    return href


def insert_data(name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, courses):
    """Insert a single record into MySQL table."""
    # Do not include ID in the VALUES — let AUTO_INCREMENT handle it.
    insert_sql = f"""
    INSERT INTO {DB_TABLE}
    (Name, Email_ID, resume_score, Timestamp, Page_no,
    Predicted_Field, User_level, Actual_skills, Recommended_skills, Recommended_courses)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(insert_sql, (
        name,
        email,
        str(res_score),
        timestamp,
        str(no_of_pages),
        reco_field,
        cand_level,
        str(skills),
        str(recommended_skills),
        str(courses)
    ))


def course_recommender(course_list, max_items=5):
    """Return list of recommended course names and render them to UI."""
    st.subheader("Courses & Certificate Recommendations 🎓")
    random.shuffle(course_list)
    rec = []
    count = min(max_items, len(course_list))
    for i in range(count):
        c_name, c_link = course_list[i]
        st.markdown(f"{i+1}. [{c_name}]({c_link})")
        rec.append(c_name)
    return rec


# --- Skill classification (improved) ---
FIELD_KEYWORDS = {
    "Data Science": {
        "tensorflow", "pytorch", "keras", "scikit-learn", "machine learning", "deep learning",
        "data analysis", "pandas", "numpy", "nlp", "opencv", "statistics", "sql", "r"
    },
    "Web Development": {
        "react", "django", "flask", "node", "express", "html", "css", "javascript", "typescript",
        "php", "laravel", "wordpress", "angular", "vue", "asp.net"
    },
    "Android Development": {
        "android", "kotlin", "java", "xml", "flutter", "react native"
    },
    "iOS Development": {
        "ios", "swift", "summary-c", "xcode", "cocoa", "cocoa touch"
    },
    "UI/UX": {
        "ux", "ui", "figma", "adobe xd", "sketch", "prototyping", "wireframe", "user research", "photoshop", "illustrator"
    }
}


def predict_field(skills_list, resume_text):
    """Predict best-fit field from skills and resume text. Returns (field_name, recommended_skills, course_list)."""
    text = " ".join(skills_list).lower() + " " + (resume_text or "").lower()
    scores = {}
    for field, keywords in FIELD_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score:
            scores[field] = score
    if not scores:
        return "Unknown", [], []  # no confident prediction

    # choose field with maximum matches
    predicted = max(scores.items(), key=lambda x: x[1])[0]

    # map field to recommended_skills & courses (keeps original lists)
    mapping = {
        "Data Science": (["Data Visualization", "Predictive Analytics", "Statistical Modeling", "Scikit-learn", "TensorFlow", "PyTorch"], ds_course),
        "Web Development": (["React", "Django", "Flask", "Node.js", "HTML", "CSS", "JavaScript"], web_course),
        "Android Development": (["Kotlin", "Android SDK", "Flutter", "Jetpack", "SQLite"], android_course),
        "iOS Development": (["Swift", "Xcode", "UIKit", "summary-C"], ios_course),
        "UI/UX": (["Figma", "Prototyping", "User Research", "Wireframing", "Adobe XD"], uiux_course)
    }
    recommended_skills, courses = mapping.get(predicted, ([], []))
    return predicted, recommended_skills, courses


# --- STREAMLIT APP ---
st.set_page_config(page_title="Is My Resume Cooked", page_icon='./Logo/logo2.png', layout="wide")


def run():
    """Improved, cleaner blue/white frontend layout for the resume analyzer.

    - Injects theme (expects inject_theme() defined elsewhere in this file)
    - Clear sidebar with role and options
    - Modern main area with PDF preview, editable skills, instant re-analyze, nicer course cards
    - Keeps DB save action and admin view intact
    """
    # apply CSS theme (no-op if inject_theme not present)
    try:
        inject_theme()
    except Exception:
        pass

    # make upload directory
    os.makedirs("./Uploaded_Resumes", exist_ok=True)

    # Top header: logo + title
    cols = st.columns([0.6, 3.4])
    with cols[0]:
        try:
            logo = Image.open("./Logo/logo2.png")
            st.image(logo, width=100)
        except Exception:
            st.write("")
    with cols[1]:
        st.title("Is My Resume Cooked")
        st.caption("Score it. Fix it. Level up your job hunt.")

    # Sidebar (updated: clearer headings + copyright/linkedin)
    st.sidebar.title("Is My Resume Cooked")
    st.sidebar.markdown("### Settings & Help")
    role = st.sidebar.selectbox("Select role", ["User", "Admin"])
    max_courses = st.sidebar.slider("Max recommended courses", 1, 8, 4)
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "Upload a single PDF resume. Files are stored locally.\n\n"
        "**Tips:** Use a single-column resume."
       
    )
    with st.sidebar.expander("How to get the best results"):
        st.markdown(
            "- Keep section headers (Education, Projects, Skills)\n"
            "- Use clear, single-column layout\n"
            "- Avoid images/complex layouts for text-heavy content"
        )

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "© 2025 Raj Nandini — [LinkedIn](https://linkedin.com/in/raj-nandini2216)"
    )
    st.sidebar.caption("Privacy: uploaded files are processed locally and stored as configured.")

    # USER VIEW
    if role == "User":
        st.header("Upload & Analyze")
        uploaded = st.file_uploader("Choose your resume (PDF)", type="pdf", accept_multiple_files=False)

        if not uploaded:
            st.info("Upload a PDF to begin. Example: single-page resume in portrait.")
            return

        # Save file
        ts_name = int(time.time())
        save_path = os.path.join("Uploaded_Resumes", f"{ts_name}_{uploaded.name}")
        with open(save_path, "wb") as fh:
            fh.write(uploaded.getbuffer())

        # Extract text and page count
        resume_text, page_count = extract_text_and_count(save_path)

        # Parse resume
        parsed = parse_resume(resume_text or "")
        name = parsed.get("name") or "Unknown"
        email = parsed.get("email") or ""
        phone = parsed.get("phone") or ""
        detected_skills = parsed.get("skills") or []
        preview = parsed.get("raw_text") or (resume_text[:800] if resume_text else "")

        # Layout: left = preview, right = analysis
        left, right = st.columns([1, 1.1])

        # LEFT: PDF preview + raw text expander
        with left:
            st.subheader("Resume Preview")
            try:
                with open(save_path, "rb") as f:
                    pdf_b64 = base64.b64encode(f.read()).decode("utf-8")
                iframe = f'<iframe src="data:application/pdf;base64,{pdf_b64}" width="100%" height="520" type="application/pdf"></iframe>'
                st.markdown(iframe, unsafe_allow_html=True)
            except Exception:
                st.write("Preview unavailable.")
            with st.expander("Show extracted text (first 1k chars)"):
                st.write(preview)

        # RIGHT: analysis box
        with right:
            st.subheader("Analysis")
            st.markdown(f"**Name:** {name}")
            st.markdown(f"**Email:** {email or 'Not found'}")
            st.markdown(f"**Phone:** {phone or 'Not found'}")
            st.markdown(f"**Pages:** {page_count}")

            # Candidate level metric
            if page_count <= 1:
                cand_level = "Fresher"
            elif page_count == 2:
                cand_level = "Intermediate"
            else:
                cand_level = "Experienced"
            st.metric("Estimated candidate level", cand_level)

            # Skills editor: multiselect + fallback text input for freeform
            # Build a small skill bank from FIELD_KEYWORDS
            skill_bank = sorted({kw for kws in FIELD_KEYWORDS.values() for kw in kws})
            preselected = [s for s in detected_skills if s in skill_bank] + [s for s in detected_skills if s not in skill_bank]
            st.markdown("**Detected skills (edit / add)**")
            chosen = st.multiselect("Pick skills from suggestions", options=skill_bank, default=[s for s in preselected if s in skill_bank])
            manual = st.text_input("Add additional skills (comma-separated)", value=", ".join([s for s in preselected if s not in skill_bank]))
            manual_list = [s.strip() for s in manual.split(",") if s.strip()]
            final_skills = list(dict.fromkeys(chosen + manual_list))  # preserve order, unique

            # Quick match summary table
            st.markdown("**Keyword matches by field**")
            text_for_match = " ".join(final_skills).lower() + " " + (resume_text or "").lower()
            match_summary = {fld: sum(1 for kw in kws if kw in text_for_match) for fld, kws in FIELD_KEYWORDS.items()}
            match_df = pd.DataFrame(list(match_summary.items()), columns=["Field", "Matches"]).sort_values("Matches", ascending=False)
            st.table(match_df)

            # Predict field & recommended items
            predicted_field, recommended_skills, recommended_courses = predict_field(final_skills, resume_text)
            if predicted_field != "Unknown":
                st.success(f"Suggested field: {predicted_field}")
                st.markdown("**Recommended skill upgrades:** " + ", ".join(recommended_skills))
            else:
                st.info("Couldn't confidently predict a field.")

            # Checklist & score (compute once and reuse)
            essentials = {
                "summary": ["summary"],
                "Education": ["Education"],
                "Hobbies / Interests": ["hobbies", "interests"],
                "Work Experience": ["Work Experience", "work"],
                "Projects": ["projects", "project"],
                "Skills": ["skills", "technical skills"],
                "Activities / Achievements": ["activities", "achievements"],
                "Additional Sections": ["publications", "conferences", "languages","certifications"]
            }
            score = 0
            checklist = []
            for label, kws in essentials.items():
                present = any(kw in (resume_text or "").lower() for kw in kws)
                checklist.append({"Item": label, "Present": "Yes" if present else "No"})
                if present:
                    score += 12.5
            st.table(pd.DataFrame(checklist))
            st.progress(int(score))
            st.metric("Resume Writing Score", f"{score}/100")

            # Action buttons row: Re-analyze, Save
            a1, a2, a3 = st.columns([1, 1, 1])
            with a1:
                if st.button("Re-analyze"):
                    # re-run minimal prediction and refresh UI
                    st.experimental_rerun()
            with a2:
                if st.button("Save analysis to DB"):
                    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S")
                    try:
                        insert_data(name, email, score, ts, page_count, predicted_field, cand_level, final_skills, recommended_skills, [c[0] for c in recommended_courses])
                        st.success("Analysis saved to DB.")
                    except Exception as e:
                        st.error(f"DB save failed: {e}")
            with a3:
                if st.button("Download CSV report"):
                    df_report = pd.DataFrame([{
                        "Name": name,
                        "Email": email,
                        "Pages": page_count,
                        "Predicted Field": predicted_field,
                        "User Level": cand_level,
                        "Score": score,
                        "Skills": ", ".join(final_skills)
                    }])
                    st.markdown(get_table_download_link(df_report, f"report_{ts_name}.csv", "Download report"), unsafe_allow_html=True)

            # Course recommendations (cards grid)
            st.markdown("### Course recommendations")
            if predicted_field != "Unknown" and recommended_courses:
                recs = recommended_courses.copy()
                random.shuffle(recs)
                recs = recs[:max_courses]
                per_row = 2 if max_courses <= 4 else 3
                for i in range(0, len(recs), per_row):
                    cols = st.columns(per_row)
                    for j, course in enumerate(recs[i:i+per_row]):
                        c_name, c_link = course
                        with cols[j]:
                            st.markdown(f"**{c_name}**")
                            st.markdown(f"[Open course]({c_link})")
            else:
                st.info("No course recommendations available.")

    # ADMIN VIEW (unchanged behaviour; kept simple)
    else:
        st.header("Admin Panel")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):
            if user == "briit" and pwd == "briit123":
                st.success("Welcome Admin")
                cursor.execute(f"SELECT * FROM {DB_TABLE};")
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Resume Score', 'Timestamp', 'Total Page',
                                                 'Predicted Field', 'User Level', 'Actual Skills', 'Recommended Skills',
                                                 'Recommended Course'])
                st.dataframe(df)
                st.markdown(get_table_download_link(df, 'User_Data.csv', 'Download Report'), unsafe_allow_html=True)
                try:
                    import plotly.express as px
                    if not df.empty:
                        fig = px.histogram(df, x='Predicted Field', title='Predicted Field Distribution')
                        st.plotly_chart(fig)
                except Exception:
                    st.write("Plotting unavailable.")
            else:
                st.error("Invalid credentials")

if __name__ == "__main__":
    run()