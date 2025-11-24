

---


````markdown
Is My Resume Cooked?
**Score it. Fix it. Level up your job hunt.**  
A Streamlit-powered resume analysis app that extracts information from a PDF resume, analyzes skills & sections, predicts your field, and recommends improvements.

🔗 **Live Demo:** https://ismyresumecooked-xcrlp4mexfdrdxpclynlfv.streamlit.app/

---

 Overview
**Is My Resume Cooked** helps job seekers understand how strong their resume is by analyzing:

- Extracted name, email, phone, skills  
- Candidate level (Fresher / Intermediate / Experienced)  
- Word-level keyword matching  
- Section completeness (projects, education, experience…)  
- Recommended skills to add  
- Suggested job field  
- Resume quality score  
- Recommended online courses

Everything happens locally inside the session — safe and private.

---

 Features

  Resume Parsing
- Upload a single **PDF resume**
- Extracts:
  - Name  
  - Email  
  - Phone  
  - Page count  
  - Skills  
  - Text preview  
- Uses `spaCy` for NER and custom regex-based extraction.

---

  Smart Analysis
- Detects **candidate level** using rules + skills  
- Counts keyword matches across fields:
  - Data Science  
  - Web Development  
  - Android  
  - iOS  
  - UI/UX  
- Computes a **resume score (0–100)** based on:
  - Section completeness  
  - Skill variety  
  - Project/experience presence  

---

  Field Prediction
Chooses the most suitable field based on matched keywords.

Example fields:
- Data Science  
- Web Development  
- UI/UX  
- Android  
- iOS  

---

  Course Recommendations
Suggests curated courses based on predicted field.

Example:
- Andrew Ng Machine Learning
- ML A–Z (Udemy)
- Data Science Foundations
- Web Dev Bootcamps, etc.

---

  Section Detection
Checks if your resume contains:
- Summary  
- Education  
- Hobbies  
- Work Experience  
- Projects  
- Skills  
- Achievements  
- Extra Sections  

---

  Tech Stack
- **Python**
- **Streamlit**
- **spaCy**
- **PyMuPDF / pdfminer**
- **Pandas**
- **MySQL (optional, for logging user stats)**
- **Plotly (for visualizations)**

---

 🛠 Local Installation

 1. Clone the repo
```bash
git clone https://github.com/nandinisingh16/IsMyResumeCooked.git
cd IsMyResumeCooked
````

 2. Create a virtual environment

```bash
python -m venv venv
source venv/Scripts/activate    Windows
```

 3. Install dependencies

```bash
pip install -r requirements.txt
```

 4. (Optional) Add MySQL credentials

Create a file:

```
.streamlit/secrets.toml
```

Inside:

```toml
[mysql]
host="localhost"
user="root"
password="YOUR_PASSWORD"
database="resume_ai"
```

 5. Run the app

```bash
streamlit run App.py
```

---

  Privacy

* Files are processed locally
* Uploaded PDFs are not stored unless configured
* No external API calls for parsing

---

  UI Preview

<img width="146" height="129" alt="image" src="https://github.com/user-attachments/assets/6904fcec-939e-40a8-8daa-e6fd4ca20c37" />

<img width="1355" height="633" alt="image" src="https://github.com/user-attachments/assets/d12ecc81-4a80-4bd1-ab92-c8157368e6be" />

<img width="591" height="512" alt="image" src="https://github.com/user-attachments/assets/7515c0a1-6ce0-4449-bade-b88f66f8b90f" />

<img width="990" height="574" alt="image" src="https://github.com/user-attachments/assets/626f2e39-7283-48bd-8d28-8d9163ec326c" />

<img width="1334" height="524" alt="image" src="https://github.com/user-attachments/assets/8bc659ad-4da9-4b60-9840-1a963fe75865" />

---

  Author

**Raj Nandini**
🔗 LinkedIn: [https://www.linkedin.com/in/raj-nandini2216/](https://www.linkedin.com/in/raj-nandini2216/)
© 2025 — All rights reserved.

---


---

```
