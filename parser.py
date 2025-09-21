from extractor import clean_text, extract_skills

# parser.py
def parse_jd(jd_text):
    jd_text = jd_text or ""
    # simple fallback: split words, filter for known skills
    SKILL_SET = ["python","sql","pandas","numpy","power bi","tableau","machine learning","nlp"]
    jd_lower = jd_text.lower()
    skills = [s for s in SKILL_SET if s in jd_lower]
    return {"skills": skills}

    
def parse_resume(resume_text, skill_list=None):
    """
    Extract skills & normalize resume text
    """
    skills_found = extract_skills(resume_text, skill_list) if skill_list else []
    return {
        "skills": skills_found,
        "raw_text": clean_text(resume_text)
    }

