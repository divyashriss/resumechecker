def generate_feedback(resume_name, score, matched, missing):
    """
    Generates concise, professional feedback for a resume.
    """
    feedback = f"**Feedback for {resume_name}:**\n\n"
    feedback += f"- Relevance Score: {score}%\n"
    
    if matched:
        feedback += f"- Strongly matched skills: {', '.join(matched[:10])}\n"
        if len(matched) > 10:
            feedback += f"  *(and {len(matched)-10} more skills matched)*\n"
    else:
        feedback += "- No strong skill matches found.\n"

    if missing:
        feedback += f"- Missing important skills: {', '.join(missing[:10])}\n"
        if len(missing) > 10:
            feedback += f"  *(and {len(missing)-10} more skills missing)*\n"

    # Quick suggestions based on missing skills
    if score < 55:
        feedback += "\n**Suggestions:** Consider highlighting key skills in your resume, " \
                    "add relevant projects, certifications, or trainings to increase your match."
    elif score < 80:
        feedback += "\n**Suggestions:** Good match! You can further improve by emphasizing missing or secondary skills."

    else:
        feedback += "\n**Suggestions:** Excellent match! Keep your resume up-to-date and tailored to the job."

    return feedback

