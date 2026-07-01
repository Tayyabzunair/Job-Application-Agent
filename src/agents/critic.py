"""
Critic Agent.
Fact-checks the tailored content against the candidate's real resume to
catch any fabricated claims or exaggerations. This is the trust/safety layer.
"""
from src.llm import get_llm
from src.schemas import TailoredContent, CriticReview
from src.rag.retriever import retrieve_relevant


def review_content(tailored: TailoredContent) -> CriticReview:
    """
    Verifies that the tailored bullets, summary, and cover letter are fully
    grounded in the candidate's actual resume. Flags any fabrication.
    """
    llm = get_llm(temperature=0.0)  # zero temp for strict, consistent checking
    structured_llm = llm.with_structured_output(CriticReview, method="json_mode")

    # Pull a broad view of the candidate's real experience for verification
    query = "all skills projects experience summary"
    resume_chunks = retrieve_relevant(query, k=8)
    resume_context = "\n\n".join(resume_chunks)

    # Combine all tailored content for review
    content_to_review = f"""
BULLETS:
{chr(10).join('- ' + b for b in tailored.tailored_bullets)}

SUMMARY:
{tailored.professional_summary}

COVER LETTER:
{tailored.cover_letter}
"""

    prompt = f"""You are a strict fact-checker and career ethics reviewer.
Your job is to verify that the GENERATED CONTENT only makes claims that are
truthfully supported by the CANDIDATE'S REAL RESUME.

CHECK FOR:
- Fabricated claims: skills, projects, companies, or numbers NOT in the resume.
- Exaggerations: overstating the candidate's actual level or scope of experience.
- Any technology/tool mentioned as "used" that is not in the resume.

RULES:
- Be strict but fair. Reasonable rephrasing of real experience is fine.
- If the content is fully grounded, set is_truthful = true and verdict = "APPROVED".
- If minor exaggerations exist, verdict = "NEEDS_REVISION".
- If serious fabrications exist, verdict = "REJECTED".
- Only list claims that are genuinely unsupported.

--- CANDIDATE'S REAL RESUME ---
{resume_context}

--- GENERATED CONTENT TO REVIEW ---
{content_to_review}

Respond ONLY with a valid JSON object matching this structure:
{{
  "is_truthful": true,
  "fabricated_claims": [],
  "exaggerations": [],
  "verdict": "APPROVED",
  "feedback": "short explanation here"
}}
"""

    result = structured_llm.invoke(prompt)
    return result
