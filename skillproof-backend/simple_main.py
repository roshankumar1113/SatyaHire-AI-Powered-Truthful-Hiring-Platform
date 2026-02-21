"""
Simple FastAPI Backend - No Database Required
Run with: python -m uvicorn simple_main:app --reload
"""

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import time
import uuid

app = FastAPI(
    title="SatyaHire AI",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class UserSignup(BaseModel):
    email: EmailStr
    password: str
    role: str
    company_name: Optional[str] = None
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: str
    email: str
    role: str
    is_active: bool = True
    is_verified: bool = False

class TextToSpeechRequest(BaseModel):
    text: str
    voice: Optional[str] = "en-US-Neural2-F"
    speed: Optional[float] = 1.0

class StartInterviewRequest(BaseModel):
    user_id: str

class SubmitAnswerRequest(BaseModel):
    session_id: str
    transcript: str
    duration: float
    confidence: float = 0.95

# In-memory storage (for demo)
users_db = {}
interview_sessions = {}

# Default interview questions
DEFAULT_QUESTIONS = [
    {
        "id": 1,
        "text": "Hello! I'm your AI interviewer. Can you please introduce yourself and tell me about your background?",
        "category": "introduction",
        "difficulty": "easy",
        "expected_duration": 120
    },
    {
        "id": 2,
        "text": "What motivated you to apply for this position?",
        "category": "motivation",
        "difficulty": "easy",
        "expected_duration": 90
    },
    {
        "id": 3,
        "text": "Can you describe a challenging project you've worked on and how you overcame obstacles?",
        "category": "experience",
        "difficulty": "medium",
        "expected_duration": 180
    },
    {
        "id": 4,
        "text": "What are your key technical skills and how have you applied them in real-world scenarios?",
        "category": "technical",
        "difficulty": "medium",
        "expected_duration": 150
    },
    {
        "id": 5,
        "text": "Where do you see yourself in the next 3-5 years?",
        "category": "career_goals",
        "difficulty": "easy",
        "expected_duration": 120
    }
]

@app.get("/")
async def root():
    return {
        "message": "SatyaHire AI Backend",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": time.time()
    }

@app.post("/api/v1/auth/signup", response_model=UserResponse)
async def signup(user_data: UserSignup):
    """Create new user account"""
    
    # Check if user exists
    if user_data.email in users_db:
        return {"detail": "Email already registered"}, 400
    
    # Create user
    user_id = f"user_{len(users_db) + 1}"
    users_db[user_data.email] = {
        "id": user_id,
        "email": user_data.email,
        "password": user_data.password,  # In production, hash this!
        "role": user_data.role,
        "company_name": user_data.company_name,
        "full_name": user_data.full_name,
    }
    
    return UserResponse(
        id=user_id,
        email=user_data.email,
        role=user_data.role,
        is_active=True,
        is_verified=False
    )

@app.post("/api/v1/auth/login", response_model=Token)
async def login(credentials: UserLogin):
    """Login and get JWT tokens"""
    
    # Check if user exists
    if credentials.email not in users_db:
        return {"detail": "Invalid credentials"}, 401
    
    user = users_db[credentials.email]
    
    # Verify password (in production, use bcrypt!)
    if user["password"] != credentials.password:
        return {"detail": "Invalid credentials"}, 401
    
    # Generate tokens (in production, use real JWT!)
    access_token = f"access_token_{user['id']}_{int(time.time())}"
    refresh_token = f"refresh_token_{user['id']}_{int(time.time())}"
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

@app.get("/api/v1/auth/me", response_model=UserResponse)
async def get_current_user():
    """Get current user info"""
    
    # For demo, return first user or create one
    if not users_db:
        return UserResponse(
            id="demo_user",
            email="demo@example.com",
            role="candidate",
            is_active=True,
            is_verified=False
        )
    
    first_user = list(users_db.values())[0]
    return UserResponse(
        id=first_user["id"],
        email=first_user["email"],
        role=first_user["role"],
        is_active=True,
        is_verified=False
    )

@app.post("/api/v1/resume/parse")
async def parse_resume():
    """Parse resume (demo)"""
    return {
        "skills": ["Python", "JavaScript", "React", "FastAPI"],
        "experience": "3 years",
        "confidence": 0.85
    }

# ============================================
# VOICE & AUDIO ENDPOINTS
# ============================================

@app.post("/api/v1/voice/text-to-speech")
async def text_to_speech(request: TextToSpeechRequest):
    """Convert text to speech"""
    return {
        "status": "success",
        "message": "Text-to-speech endpoint ready",
        "text": request.text,
        "voice": request.voice,
        "note": "Use browser's Web Speech API for now"
    }

@app.post("/api/v1/voice/speech-to-text")
async def speech_to_text(audio: UploadFile = File(...)):
    """Convert speech to text"""
    audio_data = await audio.read()
    return {
        "transcript": "Sample transcript from audio",
        "confidence": 0.95,
        "duration": 5.0,
        "size": len(audio_data)
    }

@app.get("/api/v1/voice/voice-test")
async def voice_test():
    """Test voice endpoints"""
    return {
        "status": "online",
        "endpoints": {
            "text_to_speech": "/api/v1/voice/text-to-speech",
            "speech_to_text": "/api/v1/voice/speech-to-text"
        },
        "features": [
            "Text-to-Speech conversion",
            "Speech-to-Text transcription",
            "Audio quality analysis"
        ]
    }

@app.get("/api/v1/voice/supported-voices")
async def get_supported_voices():
    """Get available TTS voices"""
    return {
        "voices": [
            {"id": "en-US-Neural2-F", "name": "Female US English", "language": "en-US", "gender": "female"},
            {"id": "en-US-Neural2-M", "name": "Male US English", "language": "en-US", "gender": "male"},
            {"id": "en-GB-Neural2-F", "name": "Female UK English", "language": "en-GB", "gender": "female"},
            {"id": "en-IN-Neural2-F", "name": "Female Indian English", "language": "en-IN", "gender": "female"}
        ]
    }

# ============================================
# INTERVIEW MANAGEMENT ENDPOINTS
# ============================================

@app.post("/api/v1/interview/start")
async def start_interview(request: StartInterviewRequest):
    """Start a new interview session"""
    session_id = f"session_{uuid.uuid4().hex[:12]}"
    
    interview_sessions[session_id] = {
        "session_id": session_id,
        "user_id": request.user_id,
        "started_at": time.time(),
        "status": "active",
        "current_question": 0,
        "questions": DEFAULT_QUESTIONS,
        "answers": [],
        "total_duration": 0.0
    }
    
    return {
        "status": "success",
        "session_id": session_id,
        "started_at": time.time(),
        "total_questions": len(DEFAULT_QUESTIONS),
        "current_question": DEFAULT_QUESTIONS[0]
    }

@app.get("/api/v1/interview/session/{session_id}")
async def get_session(session_id: str):
    """Get interview session details"""
    if session_id not in interview_sessions:
        return {"detail": "Session not found"}, 404
    
    session = interview_sessions[session_id]
    return {
        "session_id": session["session_id"],
        "user_id": session["user_id"],
        "status": session["status"],
        "current_question": session["current_question"],
        "total_questions": len(session["questions"]),
        "answered": len(session["answers"]),
        "total_duration": session["total_duration"]
    }

@app.get("/api/v1/interview/question/{session_id}")
async def get_current_question(session_id: str):
    """Get current question"""
    if session_id not in interview_sessions:
        return {"detail": "Session not found"}, 404
    
    session = interview_sessions[session_id]
    current_idx = session["current_question"]
    
    if current_idx >= len(session["questions"]):
        return {"detail": "No more questions"}, 404
    
    return session["questions"][current_idx]

@app.post("/api/v1/interview/submit-answer")
async def submit_answer(request: SubmitAnswerRequest):
    """Submit answer for current question"""
    if request.session_id not in interview_sessions:
        return {"detail": "Session not found"}, 404
    
    session = interview_sessions[request.session_id]
    current_idx = session["current_question"]
    
    # Save answer
    session["answers"].append({
        "question_id": session["questions"][current_idx]["id"],
        "transcript": request.transcript,
        "duration": request.duration,
        "confidence": request.confidence,
        "timestamp": time.time()
    })
    
    session["total_duration"] += request.duration
    session["current_question"] += 1
    
    # Check if complete
    if session["current_question"] >= len(session["questions"]):
        session["status"] = "completed"
        next_question = None
    else:
        next_question = session["questions"][session["current_question"]]
    
    progress = {
        "total_questions": len(session["questions"]),
        "answered": len(session["answers"]),
        "remaining": len(session["questions"]) - len(session["answers"]),
        "progress_percentage": (len(session["answers"]) / len(session["questions"]) * 100)
    }
    
    return {
        "status": "success",
        "message": "Answer submitted successfully",
        "progress": progress,
        "next_question": next_question,
        "interview_complete": session["status"] == "completed"
    }

@app.get("/api/v1/interview/progress/{session_id}")
async def get_progress(session_id: str):
    """Get interview progress"""
    if session_id not in interview_sessions:
        return {"detail": "Session not found"}, 404
    
    session = interview_sessions[session_id]
    total = len(session["questions"])
    answered = len(session["answers"])
    
    return {
        "session_id": session_id,
        "status": session["status"],
        "total_questions": total,
        "answered": answered,
        "remaining": total - answered,
        "progress_percentage": (answered / total * 100) if total > 0 else 0,
        "total_duration": session["total_duration"]
    }

@app.post("/api/v1/interview/complete/{session_id}")
async def complete_interview(session_id: str):
    """Complete interview"""
    if session_id not in interview_sessions:
        return {"detail": "Session not found"}, 404
    
    session = interview_sessions[session_id]
    session["status"] = "completed"
    
    avg_confidence = sum(a["confidence"] for a in session["answers"]) / len(session["answers"]) if session["answers"] else 0
    
    return {
        "status": "success",
        "message": "Interview completed successfully",
        "summary": {
            "session_id": session_id,
            "user_id": session["user_id"],
            "total_questions": len(session["questions"]),
            "total_answers": len(session["answers"]),
            "total_duration": session["total_duration"],
            "average_confidence": avg_confidence,
            "status": "completed"
        }
    }

@app.get("/api/v1/interview/health")
async def interview_health():
    """Interview service health check"""
    return {
        "status": "healthy",
        "service": "interview",
        "active_sessions": len([s for s in interview_sessions.values() if s["status"] == "active"]),
        "total_sessions": len(interview_sessions)
    }

# ============================================
# AI ENDPOINTS
# ============================================

@app.post("/api/v1/ai/generate-question")
async def generate_question():
    """Generate AI interview question"""
    return {
        "question": "Can you tell me about a time when you had to solve a complex technical problem?",
        "category": "problem_solving",
        "difficulty": "medium"
    }

@app.post("/api/v1/ai/analyze-answer")
async def analyze_answer():
    """Analyze candidate answer"""
    return {
        "score": 8.5,
        "feedback": "Good answer with specific examples",
        "strengths": ["Clear communication", "Technical depth"],
        "improvements": ["Could add more metrics"]
    }

@app.get("/api/v1/ai/health")
async def ai_health():
    """AI service health check"""
    return {
        "status": "healthy",
        "service": "ai",
        "providers": ["openai", "gemini", "anthropic"],
        "features": ["question_generation", "answer_analysis"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("simple_main:app", host="0.0.0.0", port=8000, reload=True)
