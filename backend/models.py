from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class JobPosting(BaseModel):
    job_title: str
    description: str
    required_tech_stack: List[str]
    minimum_experience: int
    hiring_slots: int
    phase1_shortlist_count: int
    phase2_shortlist_count: int


class Resume(BaseModel):
    name: str
    email: Optional[str] = None
    skills: List[str] = []
    experience: Optional[int] = None
    cv_path: str
    text_content: str


class ShortlistedCandidate(BaseModel):
    name: str
    confidence: float
    email: Optional[str] = None
    cv_path: str
    skills: List[str]
    experience: Optional[int] = None
    cover_letter: str


class ShortlistResponse(BaseModel):
    shortlisted: List[ShortlistedCandidate]


class JobStatus(BaseModel):
    job_id: str
    job_title: str
    total_resumes: int
    resumes_in_review: int
    phase1_completed: int
    phase2_completed: int
    shortlisted_count: int
    status: str  # "pending", "phase1", "phase2", "completed"
    created_at: datetime
