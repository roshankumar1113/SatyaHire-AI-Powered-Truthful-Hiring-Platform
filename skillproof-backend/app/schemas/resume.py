"""
Pydantic schemas for Resume API
"""

from pydantic import BaseModel, EmailStr
from typing import List, Dict, Optional
from datetime import datetime


class SkillDetail(BaseModel):
    name: str
    category: str
    confidence: float


class ParsedResumeData(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    skills: List[SkillDetail]
    categorized_skills: Dict[str, List[str]]
    total_skills: int
    top_skills: List[SkillDetail]
    skill_summary: str
    years_of_experience: int
    seniority_level: str
    experience_range: str


class ResumeUploadResponse(BaseModel):
    file_id: str
    filename: str
    file_path: str
    uploaded_at: str
    parsed_data: ParsedResumeData
    parsing_accuracy: float
    processing_time_ms: int


class ResumeParseResponse(BaseModel):
    skills: List[SkillDetail]
    categorized_skills: Dict[str, List[str]]
    total_skills: int
    top_skills: List[SkillDetail]
    years_of_experience: int
    seniority_level: str


class SkillMatchRequest(BaseModel):
    candidate_skills: List[str]
    required_skills: List[str]


class SkillMatchResponse(BaseModel):
    match_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    additional_skills: List[str]
    matched_count: int
    required_count: int
    recommendation: str
