"""
Gap Analyzer Agent.
Compares the JD requirements against the candidate's actual resume
content (retrieved via RAG) and reports matched / missing / partial skills.
"""
from src.llm import get_llm
from src.schemas import JDAnalysis, GapAnalysis
from src.rag.retriever import retrieve_relevant


def analyze_gap(jd: JDAnalysis) -> GapAnalysis:
    """
    Takes the structured JD analysis, retrieves relevant resume content,
    and produces a skill-gap comparison.
    """
    llm = get_llm(temperature=0.1)  # low temp for consistent, factual output
    structured_llm = llm.with_structured_output(GapAnalysis, method="json_mode")

    # Build a query from the JD skills to retrieve matching resume content
    query = f"{jd.role_title} skills: " + ", ".join(
        jd.must_have_skills + jd.nice_to_have_skills
    )
    resume_chunks = retrieve_relevant(query, k=5)
    resume_context = "\n\n".join(resume_chunks)

    prompt = f"""You are an expert technical recruiter and career advisor.
Compare the JOB REQUIREMENTS against the CANDIDATE'S RESUME and identify
which required skills the candidate has, which are missing, and which are
partially covered.

STRICT OUTPUT RULES:
- Each list (matched/missing/partial) must contain ONLY plain skill names.
- Do NOT add explanations, notes, or commentary inside the lists.
- Every list item must be a single short skill string (e.g. "Docker", "AWS").
- A skill goes in exactly ONE list: matched, missing, or partial.
- "matched" = clear evidence in the resume.
- "missing" = required by the JD but NOT in the resume.
- "partial" = something related but not an exact match.
- Do NOT invent skills the candidate does not have.
- Put all reasoning ONLY in the 'recommendation' field, never in the skill lists.
- match_score is an integer from 0 to 100 based on real skill coverage.

--- JOB REQUIREMENTS ---
Role: {jd.role_title}
Seniority: {jd.seniority}
Must-have skills: {', '.join(jd.must_have_skills)}
Nice-to-have skills: {', '.join(jd.nice_to_have_skills)}

--- CANDIDATE'S RESUME (relevant parts) ---
{resume_context}

Respond ONLY with a valid JSON object matching this structure:
{{
  "matched_skills": ["skill1", "skill2"],
  "missing_skills": ["skill3"],
  "partial_skills": ["skill4"],
  "match_score": 80,
  "recommendation": "short advice text here"
}}
"""

    result = structured_llm.invoke(prompt)
    return result
