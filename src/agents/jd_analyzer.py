from src.llm import get_llm
from src.schemas import JDAnalysis

def analyze_jd(job_description: str) -> JDAnalysis:
    """
    Job description ko padh kar structured data nikaalta hai.
    Skills, seniority, keywords — sab JSON form mein.
    """
    llm = get_llm(temperature=0.1)  # low temp = consistent extraction

    # structured output — Gemini ko force karo JDAnalysis format mein dene ko
    structured_llm = llm.with_structured_output(JDAnalysis)

    prompt = f"""You are an expert technical recruiter and ATS specialist.
Analyze the following job description carefully and extract structured information.

Rules:
- Extract ONLY skills that are actually mentioned or clearly implied.
- Separate must-have (required) from nice-to-have (preferred/bonus) skills.
- key_ats_keywords should be the exact terms an ATS would scan for.
- Be precise, do not invent skills.

JOB DESCRIPTION:
\"\"\"
{job_description}
\"\"\"
"""

    result = structured_llm.invoke(prompt)
    return result
