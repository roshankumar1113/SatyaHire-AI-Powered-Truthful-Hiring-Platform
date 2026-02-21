"""
Interview Schemas
Pydantic models for interview API requests/responses
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# Supported languages
SUPPORTED_LANGUAGES = [
    "english", "hindi", "tamil", "telugu",
    "kannada", "malayalam", "marathi",
    "gujarati", "bengali", "punjabi", "urdu"
]

# Experience levels
EXPERIENCE_LEVELS = ["junior", "mid", "senior"]

# Interview status
INTERVIEW_STATUS = ["IN_PROGRESS", "COMPLETED", "PAUSED"]


class InterviewBase(BaseModel):
    """Base interview schema"""
    role: str = Field(..., min_length=1, max_length=255)
    experience_level: str = Field(..., description="junior, mid, or senior")
    language: str = Field(default="english", description="Interview language")
    max_questions: int = Field(default=5, ge=1, le=20)
    
    @validator('experience_level')
    def validate_experience_level(cls, v):
        if v not in EXPERIENCE_LEVELS:
            raise ValueError(f"Experience level must be one of: {', '.join(EXPERIENCE_LEVELS)}")
        return v
    
    @validator('language')
    def validate_language(cls, v):
        if v.lower() not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Language must be one of: {', '.join(SUPPORTED_LANGUAGES)}")
        return v.lower()


class InterviewCreate(InterviewBase):
    """Schema for creating an interview"""
    user_id: UUID


class InterviewUpdate(BaseModel):
    """Schema for updating an interview"""
    status: Optional[str] = None
    current_question_number: Optional[int] = None
    completed_at: Optional[datetime] = None
    total_duration: Optional[int] = None
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    technical_score: Optional[float] = None
    communication_score: Optional[float] = None
    emotion_score: Optional[float] = None
    overall_score: Optional[float] = None
    
    @validator('status')
    def validate_status(cls, v):
        if v and v not in INTERVIEW_STATUS:
            raise ValueError(f"Status must be one of: {', '.join(INTERVIEW_STATUS)}")
        return v


class InterviewResponse(InterviewBase):
    """Schema for interview response"""
    id: UUID
    user_id: UUID
    status: str
    current_question_number: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    total_duration: int
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    technical_score: Optional[float] = None
    communication_score: Optional[float] = None
    emotion_score: Optional[float] = None
    overall_score: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class InterviewQuestionBase(BaseModel):
    """Base interview question schema"""
    question_number: int = Field(..., ge=1)
    question_text: str = Field(..., min_length=1)
    category: Optional[str] = None
    difficulty: Optional[str] = Field(default="medium", description="easy, medium, or hard")
    expected_duration: int = Field(default=120, ge=30, le=600)


class InterviewQuestionCreate(InterviewQuestionBase):
    """Schema for creating an interview question"""
    interview_id: UUID


class InterviewQuestionResponse(InterviewQuestionBase):
    """Schema for interview question response"""
    id: UUID
    interview_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class InterviewAnswerBase(BaseModel):
    """Base interview answer schema"""
    transcript: str = Field(..., min_length=1)
    audio_url: Optional[str] = None
    duration: float = Field(..., ge=0)
    confidence: float = Field(default=0.95, ge=0, le=1)


class InterviewAnswerCreate(InterviewAnswerBase):
    """Schema for creating an interview answer"""
    interview_id: UUID
    question_id: UUID


class InterviewAnswerUpdate(BaseModel):
    """Schema for updating an interview answer"""
    score: Optional[float] = Field(None, ge=0, le=10)
    strengths: Optional[str] = None
    improvements: Optional[str] = None
    corrected_answer: Optional[str] = None


class InterviewAnswerResponse(InterviewAnswerBase):
    """Schema for interview answer response"""
    id: UUID
    interview_id: UUID
    question_id: UUID
    score: Optional[float] = None
    strengths: Optional[str] = None
    improvements: Optional[str] = None
    corrected_answer: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class EmotionAnalysisBase(BaseModel):
    """Base emotion analysis schema"""
    timestamp: datetime
    emotion: str = Field(..., min_length=1, max_length=50)
    confidence: float = Field(..., ge=0, le=1)
    face_detected: bool = True
    blink_count: int = Field(default=0, ge=0)
    metadata: Optional[str] = None


class EmotionAnalysisCreate(EmotionAnalysisBase):
    """Schema for creating emotion analysis"""
    interview_id: UUID


class EmotionAnalysisResponse(EmotionAnalysisBase):
    """Schema for emotion analysis response"""
    id: UUID
    interview_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class InterviewWithDetails(InterviewResponse):
    """Schema for interview with all related data"""
    questions: List[InterviewQuestionResponse] = []
    answers: List[InterviewAnswerResponse] = []
    emotions: List[EmotionAnalysisResponse] = []


class InterviewSummary(BaseModel):
    """Schema for interview summary"""
    interview_id: UUID
    user_id: UUID
    role: str
    language: str
    experience_level: str
    status: str
    total_questions: int
    answered_questions: int
    total_duration: int
    average_score: Optional[float] = None
    technical_score: Optional[float] = None
    communication_score: Optional[float] = None
    emotion_score: Optional[float] = None
    overall_score: Optional[float] = None
    started_at: datetime
    completed_at: Optional[datetime] = None


class InterviewStatistics(BaseModel):
    """Schema for interview statistics"""
    total_interviews: int
    completed_interviews: int
    in_progress_interviews: int
    average_duration: float
    average_score: float
    languages_used: dict
    experience_levels: dict
