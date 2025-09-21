from extractor import read_pdf, read_docx, extract_skills
from scorer import score_resume
from feedback import generate_feedback
from parser import parse_jd



def semantic_match(jd_text, resume_text):
    """
    Placeholder function for semantic matching.
    Returns 0 similarity for now.
    """
    return 0



def check_resume(jd_file, resume_file, weights=None):
    # Read JD (pretend always PDF for now)
    jd_text = read_pdf(jd_file)
    jd_data = parse_jd(jd_text)
    jd_skills = jd_data["must_have"] + jd_data["good_to_have"]

    # Read Resume (support PDF/DOCX)
    if resume_file.endswith(".pdf"):
        resume_text = read_pdf(resume_file)
    elif resume_file.endswith(".docx"):
        resume_text = read_docx(resume_file)
    else:
        raise ValueError("Unsupported file type")

    # Score the resume
    score, verdict, color, matched, missing, details = score_resume(
        jd_skills, resume_text, weights
    )

    # Feedback
    feedback = generate_feedback(resume_file, score, matched, missing)

    return {
        "Resume": resume_file,
        "Score": score,
        "Verdict": verdict,
        "Matched": matched,
        "Missing": missing,
        "Feedback": feedback,
        "Details": details
    }

if __name__ == "__main__":
    # Example run
    jd = "sample_jd.pdf"
    resume = "sample_resume.pdf"
    result = check_resume(jd, resume)
    print(result["Feedback"])



