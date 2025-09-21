import pdfplumber
from docx import Document
import re

SKILL_SET = [
    "python", "sql", "pandas", "numpy", "power bi", "tableau",
    "machine learning", "nlp", "spark", "pyspark"
]

def clean_text(text):
    t = (text or "").lower()
    t = re.sub(r'[^a-z0-9\s]', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def read_pdf(file_path):
    text = ""
    if isinstance(file_path, str):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + " "
    else:
        # file-like object
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + " "
    return text

def read_docx(file_path):
    doc = Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + " "
    return text

def extract_skills(text, skill_list=SKILL_SET):
    text_clean = clean_text(text)
    found_skills = [s for s in skill_list if s.lower() in text_clean]
    return found_skills
