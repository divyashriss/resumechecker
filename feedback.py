def generate_feedback(resume_name, score, matched, missing):
    fb = f"**Feedback for {resume_name}**\n\n"
    fb += f"Matched Skills ({len(matched)}): {', '.join(matched) if matched else 'None'}\n"
    fb += f"Missing Skills ({len(missing)}): {', '.join(missing) if missing else 'None'}\n\n"
    
    if score >= 80:
        fb += "✅ Excellent match! Strong fit for the role.\n"
    elif score >= 55:
        fb += "⚠️ Moderate match. Consider improving missing skills.\n"
    else:
        fb += "❌ Low match. Significant improvement needed before applying.\n"
    return fb
