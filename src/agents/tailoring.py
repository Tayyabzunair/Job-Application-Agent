"""
Tailoring Agent.
Uses the JD analysis, gap analysis, and the candidate's real resume content
to produce JD-optimized resume bullets, a tailored summary, and a cover letter.
Grounded strictly in the candidate's actual experience (no fabrication).
"""
from src.llm import get_llm
from src.schemas import JDAnalysis, GapAnalysis, TailoredContent
from src.rag.retriever import retrieve_relevant


def tailor_application(jd: JDAnalysis, gap: GapAnalysis) -> TailoredContent:
    """
    Generates tailored resume bullets, a professional summary, and a cover
    letter based on the JD and the candidate's genuine experience.
    """
    llm = get_llm(temperature=0.4)  # slightly higher temp for natural writing
    structured_llm = llm.with_structured_output(TailoredContent, method="json_mode")

    # Retrieve the candidate's most relevant experience for this role
    query = f"{jd.role_title}: " + ", ".join(jd.must_have_skills)
    resume_chunks = retrieve_relevant(query, k=6)
    resume_context = "\n\n".join(resume_chunks)

    prompt = f"""You are an expert resume writer and career coach.
Rewrite the candidate's experience to strongly match the target job,
optimizing for ATS keywords while staying 100% truthful.

CRITICAL RULES:
- Use ONLY facts, projects, and skills found in the candidate's resume below.
- NEVER invent experience, companies, numbers, or skills the candidate lacks.
- Naturally weave in the JD's keywords where they genuinely apply.
- Emphasize the matched skills; do NOT claim the missing skills.
- Bullets must start with strong action verbs and be concise and impactful.
- The cover letter must be professional, specific to this role, and ~3 short paragraphs.
- Put all output in valid JSON only.

--- TARGET JOB ---
Role: {jd.role_title}
Seniority: {jd.seniority}
Must-have skills: {', '.join(jd.must_have_skills)}
Nice-to-have skills: {', '.join(jd.nice_to_have_skills)}
Important ATS keywords: {', '.join(jd.key_ats_keywords)}

--- SKILL GAP CONTEXT ---
Matched skills (emphasize these): {', '.join(gap.matched_skills)}
Missing skills (do NOT claim these): {', '.join(gap.missing_skills)}

--- CANDIDATE'S REAL EXPERIENCE (use only this) ---
{resume_context}

Respond ONLY with a valid JSON object matching this structure:
{{
  "tailored_bullets": ["bullet 1", "bullet 2", "bullet 3", "bullet 4"],
  "professional_summary": "2-3 sentence tailored summary here",
  "cover_letter": "full cover letter text here",
  "keywords_used": ["keyword1", "keyword2"]
}}
"""

    result = structured_llm.invoke(prompt)
    return result
