import os
from pypdf import PdfReader
from openai import OpenAI

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

def read_pdf(path):
    text = ""
    try:
        reader = PdfReader(path)
        for page in reader.pages:
            text += page.extract_text() or ""
    except:
        pass
    return text


def load_resumes(folder="resumes"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    resumes = []
    for f in os.listdir(folder):
        if f.endswith(".pdf"):
            resumes.append({
                "name": f.replace(".pdf", ""),
                "text": read_pdf(os.path.join(folder, f))
            })
    return resumes


def extract_skills(text):
    skills = [
        "python", "java", "sql", "machine learning",
        "deep learning", "docker", "aws", "react", "django"
    ]
    text = text.lower()
    return [s for s in skills if s in text]


def rank_candidates(job_desc, resumes):
    jd_skills = extract_skills(job_desc)
    results = []

    for r in resumes:
        rs_skills = extract_skills(r["text"])
        matched = list(set(jd_skills) & set(rs_skills))

        results.append({
            "candidate": r["name"],
            "score": len(matched),
            "matched": matched
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)


def ai_recommend(job_desc, resumes):
    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a recruiter assistant AI. "
                    "Explain why the GIVEN candidate is a good fit. "
                    "Do NOT compare with other candidates. "
                    "Do NOT recommend alternatives. "
                    "Do NOT reject anyone. "
                    "Keep it concise (4–5 bullet points)."
                )
            },
            {
                "role": "user",
                "content": f"""
Job Description:
{job_desc}

Candidate Resumes:
{[r['text'][:700] for r in resumes[:3]]}

Give a final recommendation.
"""
            }
        ]
    )
    return response.choices[0].message.content






















