"""
Interview Model
Database model for interview sessions
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class Interview(Base):
    """Interview session model"""
    __tablename__ = "interviews"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Interview configuration
    role = Column(String(255), nullable=False)
    experience_level = Column(String(50), nullable=False)  # junior, mid, senior
    language = Column(String(50), default="english", nullable=False)  # 👈 LANGUAGE FIELD
    max_questions = Column(Integer, default=5)
    
    # Interview status
    status = Column(String(50), default="IN_PROGRESS")  # IN_PROGRESS, COMPLETED, PAUSED
    current_question_number = Column(Integer, default=1)
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    
    # Duration in seconds
    total_duration = Column(Integer, default=0)
    
    # Video/Audio URLs
    video_url = Column(Text, nullable=True)
    audio_url = Column(Text, nullable=True)
    
    # Scores
    technical_score = Column(Float, nullable=True)
    communication_score = Column(Float, nullable=True)
    emotion_score = Column(Float, nullable=True)
    overall_score = Column(Float, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="interviews")
    questions = relationship("InterviewQuestion", back_populates="interview", cascade="all, delete-orphan")
    answers = relationship("InterviewAnswer", back_populates="interview", cascade="all, delete-orphan")
    emotions = relationship("EmotionAnalysis", back_populates="interview", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Interview(id={self.id}, role={self.role}, language={self.language}, status={self.status})>"


class InterviewQuestion(Base):
    """Interview question model"""
    __tablename__ = "interview_questions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    interview_id = Column(UUID(as_uuid=True), ForeignKey("interviews.id"), nullable=False)
    
    question_number = Column(Integer, nullable=False)
    question_text = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    difficulty = Column(String(50), nullable=True)  # easy, medium, hard
    expected_duration = Column(Integer, default=120)  # seconds
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    interview = relationship("Interview", back_populates="questions")
    answer = relationship("InterviewAnswer", back_populates="question", uselist=False)
    
    def __repr__(self):
        return f"<InterviewQuestion(id={self.id}, number={self.question_number}, difficulty={self.difficulty})>"


class InterviewAnswer(Base):
    """Interview answer model"""
    __tablename__ = "interview_answers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    interview_id = Column(UUID(as_uuid=True), ForeignKey("interviews.id"), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("interview_questions.id"), nullable=False)
    
    # Answer content
    transcript = Column(Text, nullable=False)
    audio_url = Column(Text, nullable=True)
    
    # Timing
    duration = Column(Float, nullable=False)  # seconds
    
    # Evaluation
    score = Column(Float, nullable=True)  # 0-10
    confidence = Column(Float, default=0.95)  # transcription confidence
    strengths = Column(Text, nullable=True)
    improvements = Column(Text, nullable=True)
    corrected_answer = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    interview = relationship("Interview", back_populates="answers")
    question = relationship("InterviewQuestion", back_populates="answer")
    
    def __repr__(self):
        return f"<InterviewAnswer(id={self.id}, score={self.score})>"


class EmotionAnalysis(Base):
    """Emotion analysis model"""
    __tablename__ = "emotion_analysis"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    interview_id = Column(UUID(as_uuid=True), ForeignKey("interviews.id"), nullable=False)
    
    # Timestamp
    timestamp = Column(DateTime, nullable=False)
    
    # Emotion data
    emotion = Column(String(50), nullable=False)  # happy, sad, angry, neutral, etc.
    confidence = Column(Float, nullable=False)
    
    # Face detection
    face_detected = Column(Boolean, default=True)
    blink_count = Column(Integer, default=0)
    
    # Additional metadata (JSON)
    metadata = Column(Text, nullable=True)  # Store as JSON string
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    interview = relationship("Interview", back_populates="emotions")
    
    def __repr__(self):
        return f"<EmotionAnalysis(id={self.id}, emotion={self.emotion}, confidence={self.confidence})>"
