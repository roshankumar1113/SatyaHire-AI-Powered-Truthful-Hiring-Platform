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

# ============================================
# MULTILINGUAL INTERVIEW ENDPOINTS
# ============================================

SUPPORTED_LANGUAGES = [
    "english", "hindi", "tamil", "telugu",
    "kannada", "malayalam", "marathi",
    "gujarati", "bengali", "punjabi", "urdu"
]

LANGUAGE_NAMES = {
    "english": "English",
    "hindi": "हिंदी",
    "tamil": "தமிழ்",
    "telugu": "తెలుగు",
    "kannada": "ಕನ್ನಡ",
    "malayalam": "മലയാളം",
    "marathi": "मराठी",
    "gujarati": "ગુજરાતી",
    "bengali": "বাংলা",
    "punjabi": "ਪੰਜਾਬੀ",
    "urdu": "اردو"
}

class StartMultilingualInterviewRequest(BaseModel):
    role: str
    experience_level: str
    language: str
    max_questions: int = 5

class SubmitMultilingualAnswerRequest(BaseModel):
    role: str
    experience_level: str
    language: str
    max_questions: int
    question_number: int
    previous_question: str
    candidate_answer: str

@app.get("/api/v1/multilingual/languages")
async def get_supported_languages():
    """Get list of supported interview languages"""
    languages = [
        {
            "code": lang,
            "name": LANGUAGE_NAMES.get(lang, lang.capitalize()),
            "native_name": LANGUAGE_NAMES.get(lang, lang.capitalize())
        }
        for lang in SUPPORTED_LANGUAGES
    ]
    return {
        "status": "success",
        "languages": languages,
        "total": len(SUPPORTED_LANGUAGES)
    }

@app.post("/api/v1/multilingual/start")
async def start_multilingual_interview(request: StartMultilingualInterviewRequest):
    """Start a new multilingual interview"""
    if request.language not in SUPPORTED_LANGUAGES:
        return {
            "status": "error",
            "message": f"Unsupported language: {request.language}"
        }, 400
    
    # Mock first question (in production, call AI service)
    questions = {
        "english": "Can you introduce yourself and tell me about your background?",
        "hindi": "क्या आप अपना परिचय दे सकते हैं और अपनी पृष्ठभूमि के बारे में बता सकते हैं?",
        "tamil": "உங்களை அறிமுகப்படுத்தி உங்கள் பின்னணியைப் பற்றி கூற முடியுமா?",
        "telugu": "మీరు మిమ్మల్ని పరిచయం చేసుకొని మీ నేపథ్యం గురించి చెప్పగలరా?",
    }
    
    question = questions.get(request.language, questions["english"])
    
    return {
        "status": "success",
        "message": f"Interview started in {LANGUAGE_NAMES.get(request.language, request.language)}",
        "data": {
            "question": question,
            "difficulty": "easy",
            "interview_status": "IN_PROGRESS",
            "question_number": 1,
            "total_questions": request.max_questions,
            "language": request.language
        }
    }

@app.post("/api/v1/multilingual/submit-answer")
async def submit_multilingual_answer(request: SubmitMultilingualAnswerRequest):
    """Submit answer and get evaluation + next question"""
    
    # Mock evaluation and next question
    evaluation = {
        "score": 8.0,
        "strengths": "Clear communication and good examples" if request.language == "english" else "स्पष्ट संचार और अच्छे उदाहरण",
        "improvements": "Could add more technical details" if request.language == "english" else "अधिक तकनीकी विवरण जोड़ सकते हैं",
        "corrected_answer": "Model answer would go here"
    }
    
    next_questions = {
        "english": "What are your key technical skills?",
        "hindi": "आपके मुख्य तकनीकी कौशल क्या हैं?",
        "tamil": "உங்கள் முக்கிய தொழில்நுட்ப திறன்கள் என்ன?",
        "telugu": "మీ ముఖ్య సాంకేతిక నైపుణ్యాలు ఏమిటి?",
    }
    
    next_question = next_questions.get(request.language, next_questions["english"])
    
    # Check if interview is complete
    is_complete = request.question_number >= request.max_questions
    
    return {
        "status": "success",
        "data": {
            "evaluation": evaluation,
            "question": next_question if not is_complete else "",
            "difficulty": "medium",
            "interview_status": "COMPLETED" if is_complete else "IN_PROGRESS",
            "question_number": request.question_number + 1,
            "total_questions": request.max_questions,
            "language": request.language
        }
    }

@app.get("/api/v1/multilingual/experience-levels")
async def get_experience_levels():
    """Get supported experience levels"""
    return {
        "status": "success",
        "levels": [
            {
                "code": "junior",
                "name": "Junior (0-2 years)",
                "description": "Entry-level positions, basic technical questions"
            },
            {
                "code": "mid",
                "name": "Mid-Level (2-5 years)",
                "description": "Intermediate positions, moderate complexity questions"
            },
            {
                "code": "senior",
                "name": "Senior (5+ years)",
                "description": "Senior positions, advanced technical and architectural questions"
            }
        ]
    }

@app.get("/api/v1/multilingual/health")
async def multilingual_health():
    """Multilingual interview service health check"""
    return {
        "status": "healthy",
        "service": "multilingual_interview",
        "supported_languages": len(SUPPORTED_LANGUAGES),
        "languages": SUPPORTED_LANGUAGES,
        "features": [
            "Multilingual interviews",
            "AI-powered evaluation",
            "Structured scoring",
            "Real-time feedback",
            "11 Indian languages supported"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("simple_main:app", host="0.0.0.0", port=8000, reload=True)
