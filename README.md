
---
**Live demo:** https://ismyresumecooked-xcrlp4mexfdrdxpclynlfv.streamlit.app/
---
# Is My Resume Cooked
**Score it. Fix it. Level up your job hunt.**

[![Streamlit](https://img.shields.io/badge/Streamlit-App-orange)](https://ismyresumecooked-xcrlp4mexfdrdxpclynlfv.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![spaCy](https://img.shields.io/badge/spaCy-NLP-orange)](https://spacy.io/)

---

**Is My Resume Cooked** is a local, Streamlit-based resume analyzer that extracts contact info, detects skills, predicts a best-fit field, scores resume completeness, and recommends skill & course upgrades — built for fast, repeatable improvements to candidate profiles.

**Live demo:** https://ismyresumecooked-xcrlp4mexfdrdxpclynlfv.streamlit.app/

---

## Why this project matters (for recruiters / hiring managers)
- **Demonstrates practical ML/NLP skills:** parsing pipelines, NER, regex heuristics and feature engineering.  
- **Product sense:** UI/UX decisions for resume preview, score transparency, and actionable recommendations.  
- **Engineering hygiene:** Streamlit deployment, packaging, and optional persistence (MySQL) for analytics.  
- **Impact:** Helps candidates improve resumes with measurable, explainable changes — directly translatable to screening/ATS pipelines.

---

## What this repo proves about the author
- Experience building **end-to-end NLP pipelines** and user-facing product features.  
- Ability to **balance accuracy, speed and UX** — pragmatic use of spaCy, pdf parsers and heuristic rules.  
- Familiarity with data engineering basics (DB logging, export, visualization).  
- Comfort deploying production web apps (Streamlit) and preparing them for reuse.

---

## Project Structure
```

Resume/
│── App.py                   # Streamlit app (entry point)
│── courses.py               # Course lists & metadata
│── resume_parser.py         # Parser: spacy + regex + skill extractor
│── requirements.txt
│── README.md
│── logos/
│── uploadedresumes/          # (ignored by git) uploaded test PDFs
│── .gitignore

```

---

## Architecture & Workflow

**High level flow**

```

[User uploads PDF]
↓
[PDF Reader (pypdf / pdfplumber)]  → extract text & page count
↓
[Resume Parser (resume_parser.py)]

* regex (email/phone)
* spaCy NER (name, entities)
* keyword / skill matcher
  ↓
  [Scoring Engine]
* section completeness
* skills coverage vs field taxonomies
* projects & experience checks
  ↓
  [Field Predictor]  → recommends skills & courses
  ↓
  [UI / Streamlit]  → preview, score, recommendations, DB logging

````

**Why this layout**
- Keeps parsing + NLP logic decoupled from UI.
- Simple scoring function that’s transparent and easy to explain to recruiters.
- Data persistence optional (MySQL) for product analytics.

---

## Key Features
- Contact & entity extraction (name, email, phone)
- Skill detection and editable tag UI
- Candidate level heuristic (pages → rough seniority)
- Field prediction (Data Science, Web, Android, iOS, UI/UX)
- Resume scoring (0–100) with per-section feedback
- Course recommendations per field
- Local processing — privacy-first by default

---

## Quick Start (developer)

1. **Clone**
```bash
git clone https://github.com/nandinisingh16/IsMyResumeCooked.git
cd IsMyResumeCooked
````

2. **Create venv & activate**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

3. **Install**

```bash
pip install -r requirements.txt
```

4. **(Optional) Add secrets for MySQL**
   Create `.streamlit/secrets.toml` with:

```toml
[mysql]
host="localhost"
user="root"
password="YOUR_PASSWORD"
database="cv"
```

5. **Run**

```bash
streamlit run App.py
```

---

## Deployment

* Deployed on Streamlit Cloud (link above).
* To deploy your fork: create a Streamlit Cloud app and point it to your GitHub repo; add any secrets in the Streamlit dashboard.

---

## Screenshots

<img width="146" height="129" alt="image" src="https://github.com/user-attachments/assets/6904fcec-939e-40a8-8daa-e6fd4ca20c37" />

<img width="1355" height="633" alt="image" src="https://github.com/user-attachments/assets/d12ecc81-4a80-4bd1-ab92-c8157368e6be" />

<img width="591" height="512" alt="image" src="https://github.com/user-attachments/assets/7515c0a1-6ce0-4449-bade-b88f66f8b90f" />

<img width="990" height="574" alt="image" src="https://github.com/user-attachments/assets/626f2e39-7283-48bd-8d28-8d9163ec326c" />

<img width="1334" height="524" alt="image" src="https://github.com/user-attachments/assets/8bc659ad-4da9-4b60-9840-1a963fe75865" />

---




## Contact

**Raj Nandini Singh**
LinkedIn: [https://www.linkedin.com/in/raj-nandini2216/](https://www.linkedin.com/in/raj-nandini2216/)
Email: [nandinisingh1622@gmail.com](mailto:nandinisingh1622@gmail.com)

---

