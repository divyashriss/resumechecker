import re
from collections import Counter
from extractor import clean_text

def score_resume(keywords, resume_text, weights=None, freq_boost=True):
    resume_clean = clean_text(resume_text)
    total_weight = 0.0
    achieved = 0.0
    matched = []
    missing = []
    tokens = resume_clean.split()
    token_counter = Counter(tokens) if freq_boost else None

    for k in keywords:
        k_clean = clean_text(k)
        w = float(weights.get(k, 1.0)) if weights else 1.0
        total_weight += w
        pattern = r'\b' + re.escape(k_clean) + r'\b'
        if re.search(pattern, resume_clean):
            matched.append(k)
            bonus = 0.0
            if freq_boost and token_counter:
                parts = k_clean.split()
                counts = [token_counter.get(p,0) for p in parts]
                count_phrase = min(counts) if counts else 0
                if count_phrase > 1:
                    bonus = 0.15 * (count_phrase - 1) * w
            achieved += w + bonus
        else:
            missing.append(k)

    score = round((achieved / total_weight) * 100, 2) if total_weight > 0 else 0.0
    if score >= 80:
        verdict, color = "High", "green"
    elif score >= 55:
        verdict, color = "Medium", "orange"
    else:
        verdict, color = "Low", "red"

    details = {
        "total_weight": total_weight,
        "achieved_weight": round(achieved,2)
    }
    return score, verdict, color, matched, missing, details
