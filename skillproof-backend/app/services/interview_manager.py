"""
Interview Session Manager
Manages interview sessions, questions, and responses
"""
from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel


class InterviewQuestion(BaseModel):
    id: int
    text: str
    category: str
    difficulty: str
    expected_duration: int  # seconds


class InterviewAnswer(BaseModel):
    question_id: int
    transcript: str
    audio_url: Optional[str] = None
    duration: float
    confidence: float
    timestamp: datetime


class InterviewSession(BaseModel):
    session_id: str
    user_id: str
    started_at: datetime
    status: str  # 'active', 'completed', 'paused'
    current_question: int
    questions: List[InterviewQuestion]
    answers: List[InterviewAnswer]
    total_duration: float


class InterviewManager:
    """
    Manage interview sessions and flow
    """
    
    def __init__(self):
        self.sessions: Dict[str, InterviewSession] = {}
        self.default_questions = self._load_default_questions()
    
    def _load_default_questions(self) -> List[InterviewQuestion]:
        """Load default interview questions"""
        return [
            InterviewQuestion(
                id=1,
                text="Hello! I'm your AI interviewer. Can you please introduce yourself and tell me about your background?",
                category="introduction",
                difficulty="easy",
                expected_duration=120
            ),
            InterviewQuestion(
                id=2,
                text="What motivated you to apply for this position?",
                category="motivation",
                difficulty="easy",
                expected_duration=90
            ),
            InterviewQuestion(
                id=3,
                text="Can you describe a challenging project you've worked on and how you overcame obstacles?",
                category="experience",
                difficulty="medium",
                expected_duration=180
            ),
            InterviewQuestion(
                id=4,
                text="What are your key technical skills and how have you applied them in real-world scenarios?",
                category="technical",
                difficulty="medium",
                expected_duration=150
            ),
            InterviewQuestion(
                id=5,
                text="Where do you see yourself in the next 3-5 years?",
                category="career_goals",
                difficulty="easy",
                expected_duration=120
            )
        ]
    
    def create_session(self, user_id: str, session_id: str) -> InterviewSession:
        """
        Create a new interview session
        
        Args:
            user_id: User identifier
            session_id: Unique session identifier
            
        Returns:
            InterviewSession object
        """
        session = InterviewSession(
            session_id=session_id,
            user_id=user_id,
            started_at=datetime.now(),
            status="active",
            current_question=0,
            questions=self.default_questions,
            answers=[],
            total_duration=0.0
        )
        self.sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[InterviewSession]:
        """Get interview session by ID"""
        return self.sessions.get(session_id)
    
    def get_current_question(self, session_id: str) -> Optional[InterviewQuestion]:
        """Get current question for session"""
        session = self.get_session(session_id)
        if not session:
            return None
        
        if session.current_question < len(session.questions):
            return session.questions[session.current_question]
        return None
    
    def submit_answer(
        self,
        session_id: str,
        transcript: str,
        duration: float,
        confidence: float,
        audio_url: Optional[str] = None
    ) -> bool:
        """
        Submit answer for current question
        
        Args:
            session_id: Session identifier
            transcript: Answer transcript
            duration: Answer duration in seconds
            confidence: Transcription confidence
            audio_url: Optional audio file URL
            
        Returns:
            True if successful, False otherwise
        """
        session = self.get_session(session_id)
        if not session:
            return False
        
        current_q = self.get_current_question(session_id)
        if not current_q:
            return False
        
        answer = InterviewAnswer(
            question_id=current_q.id,
            transcript=transcript,
            audio_url=audio_url,
            duration=duration,
            confidence=confidence,
            timestamp=datetime.now()
        )
        
        session.answers.append(answer)
        session.total_duration += duration
        session.current_question += 1
        
        # Check if interview is complete
        if session.current_question >= len(session.questions):
            session.status = "completed"
        
        return True
    
    def get_next_question(self, session_id: str) -> Optional[InterviewQuestion]:
        """Get next question in sequence"""
        session = self.get_session(session_id)
        if not session:
            return None
        
        return self.get_current_question(session_id)
    
    def get_progress(self, session_id: str) -> Dict:
        """
        Get interview progress
        
        Returns:
            Dictionary with progress information
        """
        session = self.get_session(session_id)
        if not session:
            return {}
        
        total_questions = len(session.questions)
        answered = len(session.answers)
        
        return {
            "session_id": session_id,
            "status": session.status,
            "total_questions": total_questions,
            "answered": answered,
            "remaining": total_questions - answered,
            "progress_percentage": (answered / total_questions * 100) if total_questions > 0 else 0,
            "total_duration": session.total_duration,
            "current_question_number": session.current_question + 1
        }
    
    def pause_session(self, session_id: str) -> bool:
        """Pause interview session"""
        session = self.get_session(session_id)
        if session and session.status == "active":
            session.status = "paused"
            return True
        return False
    
    def resume_session(self, session_id: str) -> bool:
        """Resume paused session"""
        session = self.get_session(session_id)
        if session and session.status == "paused":
            session.status = "active"
            return True
        return False
    
    def complete_session(self, session_id: str) -> Dict:
        """
        Complete interview session and return summary
        
        Returns:
            Summary dictionary
        """
        session = self.get_session(session_id)
        if not session:
            return {}
        
        session.status = "completed"
        
        return {
            "session_id": session_id,
            "user_id": session.user_id,
            "started_at": session.started_at.isoformat(),
            "completed_at": datetime.now().isoformat(),
            "total_questions": len(session.questions),
            "total_answers": len(session.answers),
            "total_duration": session.total_duration,
            "average_confidence": sum(a.confidence for a in session.answers) / len(session.answers) if session.answers else 0,
            "status": "completed"
        }


# Singleton instance
interview_manager = InterviewManager()
