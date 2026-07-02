from pydantic import BaseModel, Field
from typing import List, TypedDict, Optional


class JDAnalysis(BaseModel):
    """JD Analyzer ka structured output."""
    role_title: str = Field(description="Job role/title, e.g. 'AI Engineer'")
    seniority: str = Field(description="e.g. 'Junior', 'Mid', 'Senior', 'Fresher'")
    must_have_skills: List[str] = Field(description="Required/must-have skills")
    nice_to_have_skills: List[str] = Field(description="Preferred/bonus skills")
    key_ats_keywords: List[str] = Field(
        description="Important keywords for ATS matching"
    )
    summary: str = Field(description="1-2 line summary of what they want")
class GapAnalysis(BaseModel):
    """Output of the Gap Analyzer: how the resume matches the JD."""
    matched_skills: List[str] = Field(
        description="Skills required by the JD that the candidate clearly has"
    )
    missing_skills: List[str] = Field(
        description="Skills required by the JD that are NOT found in the resume"
    )
    partial_skills: List[str] = Field(
        description="Skills the candidate has partially or in a related form"
    )
    match_score: int = Field(
        description="Overall fit score from 0 to 100 based on skill coverage"
    )
    recommendation: str = Field(
        description="Short advice on how to strengthen the application for this JD"
    )
class TailoredContent(BaseModel):
    """Output of the Tailoring Agent: JD-optimized resume bullets + cover letter."""
    tailored_bullets: List[str] = Field(
        description="Resume bullet points rewritten to match the JD, using its keywords naturally"
    )
    professional_summary: str = Field(
        description="A 2-3 sentence professional summary tailored to this specific job"
    )
    cover_letter: str = Field(
        description="A personalized cover letter for this specific job"
    )
    keywords_used: List[str] = Field(
        description="JD keywords that were naturally incorporated into the content"
    )
class CriticReview(BaseModel):
    """Output of the Critic Agent: fact-checks the tailored content."""
    is_truthful: bool = Field(
        description="True if all claims are grounded in the resume, False if any fabrication is found"
    )
    fabricated_claims: List[str] = Field(
        description="Specific claims that are NOT supported by the candidate's resume (empty if none)"
    )
    exaggerations: List[str] = Field(
        description="Claims that overstate the candidate's actual experience (empty if none)"
    )
    verdict: str = Field(
        description="Short overall assessment: APPROVED, NEEDS_REVISION, or REJECTED"
    )
    feedback: str = Field(
        description="Brief explanation of the review findings"
    )
from typing import TypedDict, Optional


class AgentState(TypedDict):
    """Shared state passed between all nodes in the LangGraph."""
    jd_text: str                          # raw job description input
    jd: Optional[JDAnalysis]              # output of JD Analyzer
    gap: Optional[GapAnalysis]            # output of Gap Analyzer
    tailored: Optional[TailoredContent]   # output of Tailoring Agent
    review: Optional[CriticReview]        # output of Critic Agent
    ats: Optional[dict]                   # output of ATS Scorer
    retry_count: int                      # how many times we retried tailoring
class AgentState(TypedDict):
    """Shared state passed between all nodes in the LangGraph."""
    jd_text: str                          # raw job description input
    jd: Optional[JDAnalysis]              # output of JD Analyzer
    gap: Optional[GapAnalysis]            # output of Gap Analyzer
    tailored: Optional[TailoredContent]   # output of Tailoring Agent
    review: Optional[CriticReview]        # output of Critic Agent
    ats: Optional[dict]                   # output of ATS Scorer
    retry_count: int                      # how many times we retried tailoring