
````markdown
#  Is My Resume Cooked?
**AI-powered resume analyzer that scores your resume, detects missing sections, identifies your candidate level, extracts skills, and recommends what to improve.**

Upload your PDF, get an instant breakdown, and level up your job hunt — all in one place.

---

##  Features

###  Resume Analysis
- Extracts **name, email, phone**, and resume text
- Detects **skills**, missing sections, and resume structure
- Estimates **candidate level** (Fresher / Intermediate / Experienced)
- Identifies **keyword matches** across fields:
  - Data Science  
  - Web Development  
  - UI/UX  
  - Android Development  
  - iOS Development  

### AI Resume Score
Get a clean **0–100 score** showing how polished your resume is:
- Summary  
- Education  
- Experience  
- Projects  
- Skills  
- Achievements  
- Additional sections  

### 🎓 Course Recommendations
Smart recommendations based on your detected field:
- Machine Learning (Andrew Ng)
- ML A–Z (Udemy)
- Data Science Foundations
- More curated courses

###  PDF Upload (Local Only)
- Works with **single PDF**
- No cloud upload — files are processed **locally** for privacy
- Streamlit UI with drag-and-drop

---

##  UI Preview

The app includes:
- **Resume Upload Panel**
- **Extracted Text Preview (first 1k chars)**
- **Skill Editor (+ suggestions)**
- **Field Match Table**
- **Recommended Courses Section**

>  *Privacy Note:* Uploaded resumes never leave your device (unless you configure database storage).  

---

##  Tech Stack
- **Python**
- **Streamlit** (frontend UI)
- **spaCy** (NER for name extraction)
- **PyPDF2 / pdfplumber** for text extraction
- **MySQL / PyMySQL** (optional storage)
- **Custom rule-based NLP** for skills & sections

---

##  Installation

```bash
git clone https://github.com/nandinisingh16/IsMyResumeCooked.git
cd IsMyResumeCooked
pip install -r requirements.txt
````

### Add MySQL credentials (optional)

Create:

```
.streamlit/secrets.toml
```

```toml
[mysql]
host = "localhost"
user = "root"
password = "YOUR_PASSWORD"
database = "resume_ai"
```

---

##  Run the App

```bash
streamlit run App.py
```

---

##  Project Structure

```
 IsMyResumeCooked
 ┣ 📁 assets
 ┣ 📁 components
 ┣ 📁 utils
 ┣ App.py
 ┣ requirements.txt
 ┣ README.md
 ┗ .gitignore
```

---

##  Author

**Raj Nandini Singh**
🔗 LinkedIn: [https://linkedin.com/in/raj-nandini2216](https://linkedin.com/in/raj-nandini2216)
 Portfolio: Coming soon

---





```
