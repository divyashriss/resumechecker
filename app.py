import streamlit as st
import pandas as pd
import os
from extractor import read_pdf, read_docx, extract_skills, SKILL_SET
from scorer import score_resume
from feedback import generate_feedback
import matplotlib.pyplot as plt

st.set_page_config(page_title="Resume Relevance - Pro", layout="wide")
st.title("🚀 Resume Relevance Checker")

# --- Skill weights
default_weights = {
    "python": 2.5, "sql": 2.0, "pandas": 1.5, "numpy": 1.2,
    "power bi": 1.5, "tableau": 1.5, "machine learning": 2.0,
    "nlp": 2.0, "spark": 1.5, "pyspark": 1.5
}

st.sidebar.header("Adjust Skill Weights (optional)")
weights = {}
for k,v in default_weights.items():
    val = st.sidebar.number_input(k, min_value=0.0, max_value=5.0, value=float(v), step=0.1)
    weights[k] = val

# Upload JD & Resumes
jd_file = st.file_uploader("Upload JD (PDF/DOCX)", type=["pdf","docx"])
resumes = st.file_uploader("Upload Resumes (PDF/DOCX) — multiple", type=["pdf","docx"], accept_multiple_files=True)

if st.button("Evaluate ▶️"):
    if not jd_file or not resumes:
        st.error("Upload both JD and at least one resume to proceed.")
        st.stop()

    # Read JD
    if jd_file.name.endswith(".pdf"):
        jd_text = read_pdf(jd_file)
    else:
        jd_text = read_docx(jd_file)

    jd_skills = extract_skills(jd_text, SKILL_SET)
    st.subheader("🔎 Extracted JD Skills / Phrases")
    st.write(", ".join(jd_skills) if jd_skills else "No skill phrases detected.")

    # Process resumes
    rows = []
    for r in resumes:
        if r.name.endswith(".pdf"):
            rtext = read_pdf(r)
        else:
            rtext = read_docx(r)
        score, verdict, color, matched, missing, details = score_resume(jd_skills, rtext, weights)
        feedback = generate_feedback(r.name, score, matched, missing)

        rows.append({
            "Resume": r.name,
            "Score": score,
            "Verdict": verdict,
            "Matched": "; ".join(matched),
            "Missing": "; ".join(missing),
            "Feedback": feedback
        })

    df = pd.DataFrame(rows).sort_values("Score", ascending=False).reset_index(drop=True)

    st.subheader("🏆 Summary & Ranking")
    st.dataframe(df[["Resume","Score","Verdict"]])

    st.subheader("📊 Score Distribution")
    st.bar_chart(df.set_index("Resume")["Score"])

    st.subheader("🧾 Detailed results")
    for idx, r in df.iterrows():
        st.markdown(f"### {r['Resume']} — {r['Score']}% — **{r['Verdict']}**")
        st.markdown(r["Feedback"])
        st.write("---")

    st.download_button("💾 Download full results CSV", df.to_csv(index=False).encode(), "results.csv", "text/csv")

