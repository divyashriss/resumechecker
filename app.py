import streamlit as st
import pandas as pd
import os
from extractor import read_pdf, read_docx, extract_skills, clean_text
from parser import parse_jd, parse_resume
from scorer import score_resume
from feedback import generate_feedback
from resumechecker import semantic_match

st.set_page_config(page_title="🚀 Resume Relevance Checker", layout="wide")
st.title("Resume Relevance & AI Scoring Platform")

# --- Sidebar: Skill Weights ---
st.sidebar.header("Adjust Skill Weights (optional)")
default_weights = {
    "python": 2.5, "sql": 2.0, "pandas": 1.5, "numpy": 1.2,
    "power bi": 1.5, "tableau": 1.5, "machine learning": 2.0, "nlp": 2.0,
    "spark": 1.5, "pyspark": 1.5
}
weights = {}
for k,v in default_weights.items():
    val = st.sidebar.number_input(k, min_value=0.0, max_value=5.0, value=float(v), step=0.1)
    weights[k] = val

# --- Upload JD & Resumes ---
jd_file = st.file_uploader("Upload Job Description (PDF/DOCX)", type=["pdf","docx"])
resumes = st.file_uploader("Upload Resumes (PDF/DOCX) — multiple", type=["pdf","docx"], accept_multiple_files=True)

if st.button("Evaluate ▶️"):
    if not jd_file:
        st.error("Please upload a JD file.")
        st.stop()
    if not resumes:
        st.error("Please upload at least one resume.")
        st.stop()

    # Parse JD
    jd_text = read_pdf(jd_file) if jd_file.type=="application/pdf" else read_docx(jd_file)
    jd_data = parse_jd(jd_text)
    jd_skills = jd_data['skills']

    st.subheader("🔎 Extracted JD Skills")
    st.write(", ".join(jd_skills))

    # Evaluate each resume
    results = []
    for r in resumes:
        rname = r.name
        rtext = read_pdf(r) if r.type=="application/pdf" else read_docx(r)
        resume_data = parse_resume(rtext)

        # Hard skill match score
        score, matched, missing = score_resume(jd_skills, rtext, weights)

        # Semantic match using embeddings
        semantic_score = semantic_match(jd_text, rtext)

        # Combined score (50% hard + 50% semantic)
        final_score = round((score*0.5 + semantic_score*0.5),2)

        verdict = "High" if final_score>=80 else "Medium" if final_score>=55 else "Low"
        feedback = generate_feedback(rname, final_score, matched, missing)

        results.append({
            "Resume": rname,
            "Score": final_score,
            "Verdict": verdict,
            "Matched": "; ".join(matched),
            "Missing": "; ".join(missing),
            "Feedback": feedback
        })

    df = pd.DataFrame(results).sort_values("Score", ascending=False)
    st.subheader("🏆 Candidate Ranking")
    st.dataframe(df[["Resume","Score","Verdict"]])

    st.subheader("📊 Score Distribution")
    st.bar_chart(df.set_index("Resume")["Score"])

    st.subheader("🧾 Detailed Feedback")
    for idx, r in df.iterrows():
        st.markdown(f"### {r['Resume']} — {r['Score']}% — **{r['Verdict']}**")
        st.markdown(r["Feedback"])
        st.write("---")

    st.download_button("💾 Download Full Results CSV", df.to_csv(index=False).encode(), "results.csv", "text/csv")
