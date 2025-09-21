import re
import pdfplumber
import docx2txt

# A base skill set you can expand
SKILL_SET = [
    "python","sql","pandas","numpy","power bi","tableau",
    "machine learning","nlp","spark","pyspark","excel","deep learning"
]

def clean_text(text):
    """Lowercase, remove special chars, extra spaces"""
    t = (text or "").lower()
    t = re.sub(r'[^a-z0-9\s]', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def read_pdf(file):
    """Extract text from PDF"""
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + " "
    return text

def read_docx(file):
    """Extract text from DOCX"""
    return docx2txt.process(file)

def extract_skills(text, skill_list=SKILL_SET):
    """Return list of skills found in text"""
    text_clean = clean_text(text)
    found = []
    for skill in skill_list:
        if skill.lower() in text_clean:
            found.append(skill)
    return found
