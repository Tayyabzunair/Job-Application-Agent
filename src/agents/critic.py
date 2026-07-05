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
    Falls back to a safe default if the model returns malformed output.
    """
    llm = get_llm(temperature=0.0)  # zero temp for strict, consistent checking
    structured_llm = llm.with_structured_output(CriticReview, method="json_mode")

    # Pull a broad view of the candidate's real experience for verification
    query = "skills technologies frameworks projects experience certifications"
    resume_chunks = retrieve_relevant(query, k=12)
    resume_context = "\n\n".join(resume_chunks)

    content_to_review = f"""
BULLETS:
{chr(10).join('- ' + b for b in tailored.tailored_bullets)}

SUMMARY:
{tailored.professional_summary}

COVER LETTER:
{tailored.cover_letter}
"""

    prompt = f"""You are a strict fact-checker and career ethics reviewer.
Verify that the GENERATED CONTENT only makes claims truthfully supported by
the CANDIDATE'S REAL RESUME.

CHECK FOR:
- Fabricated claims: skills, projects, companies, or numbers NOT in the resume.
- Exaggerations: overstating the candidate's actual level or scope.

DO NOT FLAG (these are always fine):
- Any skill that appears ANYWHERE in the resume (including the Skills section).
  Example: if "LangChain" is listed in skills, claiming LangChain experience is VALID.
- The job title being applied for, or general statements of interest/enthusiasm.
- Reasonable rephrasing or professional framing of real experience.
- Standard cover-letter courtesy language.

Only flag something if it is genuinely NOT supported anywhere in the resume.

STRICT OUTPUT RULES:
- Return ONE single valid JSON object and NOTHING else.
- Every list item must be a short plain string. No line breaks inside strings.
- Do NOT split a field name and its value into separate list items.
- 'verdict' must be exactly one of: "APPROVED", "NEEDS_REVISION", "REJECTED".
- Keep 'feedback' to a single short sentence.
- If fully grounded: is_truthful=true, verdict="APPROVED".
- If minor issues: verdict="NEEDS_REVISION".
- If serious fabrication: verdict="REJECTED".

--- CANDIDATE'S REAL RESUME ---
{resume_context}

--- GENERATED CONTENT TO REVIEW ---
{content_to_review}

Respond ONLY with a valid JSON object exactly matching this structure:
{{
  "is_truthful": true,
  "fabricated_claims": ["claim one", "claim two"],
  "exaggerations": ["exaggeration one"],
  "verdict": "APPROVED",
  "feedback": "one short sentence here"
}}
"""

    try:
        result = structured_llm.invoke(prompt)
        return result
    except Exception as e:
        # Safe fallback if the model returns malformed JSON.
        # We default to NEEDS_REVISION so the graph can retry tailoring.
        print(f"  [Critic] Parsing failed, using safe fallback. ({type(e).__name__})")
        return CriticReview(
            is_truthful=False,
            fabricated_claims=[],
            exaggerations=[],
            verdict="NEEDS_REVISION",
            feedback="Automated review could not be parsed; flagged for revision.",
        )
