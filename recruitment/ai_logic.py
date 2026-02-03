

import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("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"),
    base_url="https://openrouter.ai/api/v1"
)


# ----------------------------------
# RESUME DIRECTORY (FIXED PATH)
# ----------------------------------
BASE_DIR = os.path.dirname(__file__)          # recruitment/
RESUME_DIR = os.path.join(BASE_DIR, "resumes")

# ----------------------------------
# PDF READER
# ----------------------------------
def read_pdf(path: str) -> str:
    text = ""
    try:
        reader = PdfReader(path)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception:
        pass
    return text


# ----------------------------------
# LOAD RESUMES (PDF DATASET)
# ----------------------------------
def load_resumes():
    resumes = []

    if not os.path.exists(RESUME_DIR):
        return resumes

    for file in os.listdir(RESUME_DIR):
        if not file.lower().endswith(".pdf"):
            continue

        path = os.path.join(RESUME_DIR, file)
        text = read_pdf(path)

        if text.strip():
            resumes.append({
                "name": file,
                "text": text
            })

    return resumes


# ----------------------------------
# SKILL EXTRACTION (RULE BASED)
# ----------------------------------
def extract_skills(text: str):
    skills = [
        "python", "java", "sql", "machine learning",
        "deep learning", "docker", "aws",
        "react", "django"
    ]

    text = text.lower()
    return [s for s in skills if s in text]


# ----------------------------------
# CANDIDATE RANKING
# ----------------------------------
def rank_candidates(job_desc: str, resumes: list):
    jd_skills = extract_skills(job_desc)
    results = []

    for r in resumes:
        resume_skills = extract_skills(r["text"])
        matched = list(set(jd_skills) & set(resume_skills))

        results.append({
            "candidate": r["name"],
            "score": len(matched),
            "matched": matched
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)


# ----------------------------------
# AI RECOMMENDATION (LLM)
# ----------------------------------
def ai_recommend(job_desc, resumes):
    if not resumes:
        return "No resumes available for AI analysis."

    prompt = f"""
Job Description:
{job_desc}

Candidate Resumes:
{[r['text'][:500] for r in resumes[:3]]}

Explain why the BEST candidate is a good fit.
Use 4–5 bullet points.
"""

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[
            {"role": "system", "content": "You are an AI recruiter assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content
