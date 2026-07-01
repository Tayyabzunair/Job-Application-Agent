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
