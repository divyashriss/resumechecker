from extractor import clean_text, extract_skills

def parse_jd(jd_text, skill_list=None):
    """
    Extract role title, must-have skills, good-to-have skills from JD text
    """
    jd_clean = clean_text(jd_text)
    lines = jd_clean.splitlines()
    
    role_title = lines[0] if lines else "Unknown Role"
    
    # Skills extraction
    must_have_skills = extract_skills(jd_text, skill_list) if skill_list else []
    
    # For simplicity, assume no separate 'good-to-have' parsing
    good_to_have_skills = []
    
    return {
        "role_title": role_title,
        "must_have_skills": must_have_skills,
        "good_to_have_skills": good_to_have_skills
    }

def parse_resume(resume_text, skill_list=None):
    """
    Extract skills & normalize resume text
    """
    skills_found = extract_skills(resume_text, skill_list) if skill_list else []
    return {
        "skills": skills_found,
        "raw_text": clean_text(resume_text)
    }
