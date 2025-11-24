import spacy
import re

nlp = spacy.load("en_core_web_sm")

SKILLS = [
    "python", "java", "c++", "machine learning", "deep learning", "nlp",
    "sql", "mysql", "pandas", "numpy", "tensorflow", "pytorch", "opencv",
    "react", "node", "html", "css", "javascript", "docker", "kubernetes"
]

def extract_name(text):
    lines = text.split("\n")
    top = " ".join(lines[:3])  # first few lines

    # Check for uppercase name (most resumes)
    for line in lines[:4]:
        if line.strip().isupper() and len(line.split()) <= 4:
            return line.strip().title()

    # Otherwise fall back to spaCy
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

    return None

def extract_email(text):
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r'\+?\d[\d -]{8,}\d', text)
    return match.group(0) if match else None

def extract_skills(text):
    text_lower = text.lower()
    found = [skill for skill in SKILLS if skill in text_lower]
    return list(set(found))

def parse_resume(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "raw_text": text[:500]  # preview only
    }
