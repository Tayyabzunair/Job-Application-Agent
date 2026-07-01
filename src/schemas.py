from pydantic import BaseModel, Field
from typing import List

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
