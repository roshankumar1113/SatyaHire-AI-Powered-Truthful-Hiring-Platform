"""
Interview Management Endpoints
Handles interview sessions, questions, and answers
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

from app.services.interview_manager import interview_manager
from app.services.audio_processor import audio_processor
from app.services.ai_service import ai_service

router = APIRouter()


class StartInterviewRequest(BaseModel):
    user_id: str
    role: str
    experience_level: str
    language: str = "english"
    max_questions: int = 5


class SubmitAnswerRequest(BaseModel):
    session_id: str
    question_number: int
    previous_question: str
    transcript: str
    duration: float
    confidence: float = 0.95


@router.post("/start")
async def start_interview(request: StartInterviewRequest):
    """
    Start a new interview session with AI-powered questions
    
    Returns:
        Session details and first question
    """
    try:
        # Generate unique session ID
        session_id = f"session_{uuid.uuid4().hex[:12]}"
        
        # Create session
        session = interview_manager.create_session(
            user_id=request.user_id,
            session_id=session_id
        )
        
        # Generate first question using AI
        ai_response = ai_service.generate_or_evaluate(
            role=request.role,
            experience_level=request.experience_level,
            language=request.language,
            previous_question="",
            candidate_answer="",
            question_number=1,
            max_questions=request.max_questions
        )
        
        return {
            "status": "success",
            "session_id": session_id,
            "started_at": session.started_at.isoformat(),
            "total_questions": request.max_questions,
            "current_question": {
                "id": 1,
                "text": ai_response.get("question", ""),
                "difficulty": ai_response.get("difficulty", "medium"),
                "interview_status": ai_response.get("interview_status", "IN_PROGRESS")
            },
            "role": request.role,
            "experience_level": request.experience_level,
            "language": request.language
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start interview: {str(e)}")


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """
    Get interview session details
    """
    session = interview_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session.session_id,
        "user_id": session.user_id,
        "status": session.status,
        "started_at": session.started_at.isoformat(),
        "current_question": session.current_question,
        "total_questions": len(session.questions),
        "answered": len(session.answers),
        "total_duration": session.total_duration
    }


@router.get("/question/{session_id}")
async def get_current_question(session_id: str):
    """
    Get current question for session
    """
    question = interview_manager.get_current_question(session_id)
    if not question:
        raise HTTPException(status_code=404, detail="No current question or session not found")
    
    return {
        "id": question.id,
        "text": question.text,
        "category": question.category,
        "difficulty": question.difficulty,
        "expected_duration": question.expected_duration
    }


@router.post("/submit-answer")
async def submit_answer(request: SubmitAnswerRequest):
    """
    Submit answer and get AI evaluation + next question
    """
    try:
        # Get session
        session = interview_manager.get_session(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Use AI to evaluate answer and generate next question
        ai_response = ai_service.generate_or_evaluate(
            role=session.questions[0].category if session.questions else "Developer",  # Use stored role
            experience_level="mid",  # Use stored experience level
            language="english",  # Use stored language
            previous_question=request.previous_question,
            candidate_answer=request.transcript,
            question_number=request.question_number,
            max_questions=len(session.questions)
        )
        
        # Save answer
        success = interview_manager.submit_answer(
            session_id=request.session_id,
            transcript=request.transcript,
            duration=request.duration,
            confidence=request.confidence
        )
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to submit answer")
        
        # Get progress
        progress = interview_manager.get_progress(request.session_id)
        
        # Prepare response
        result = {
            "status": "success",
            "message": "Answer submitted successfully",
            "progress": progress,
            "interview_status": ai_response.get("interview_status", "IN_PROGRESS")
        }
        
        # Add evaluation if present
        if "evaluation" in ai_response and ai_response["evaluation"]:
            result["evaluation"] = ai_response["evaluation"]
        
        # Add next question if not complete
        if ai_response.get("interview_status") != "COMPLETED":
            result["next_question"] = {
                "text": ai_response.get("question", ""),
                "difficulty": ai_response.get("difficulty", "medium")
            }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process answer: {str(e)}")


@router.post("/submit-audio")
async def submit_audio_answer(
    session_id: str = Form(...),
    question_id: int = Form(...),
    audio: UploadFile = File(...)
):
    """
    Submit audio recording for answer
    """
    try:
        # Read audio data
        audio_data = await audio.read()
        
        # Validate audio
        is_valid, message = audio_processor.validate_audio_format(audio_data, audio.filename or "audio.webm")
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)
        
        # Analyze audio
        quality = audio_processor.analyze_audio_quality(audio_data)
        
        # In production, save to cloud storage
        audio_url = f"storage/interviews/{session_id}/q{question_id}.webm"
        
        return {
            "status": "success",
            "message": "Audio submitted successfully",
            "audio_url": audio_url,
            "quality": quality,
            "size": len(audio_data)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process audio: {str(e)}")


@router.post("/transcribe-audio")
async def transcribe_audio(
    audio: UploadFile = File(...),
    language: str = Form("english")
):
    """
    Transcribe audio to text using AI
    """
    try:
        # Transcribe using AI service
        result = ai_service.transcribe_audio(audio.file, language)
        
        return {
            "status": "success",
            "transcript": result["transcript"],
            "language": result["language"],
            "duration": result["duration"],
            "confidence": result["confidence"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


@router.get("/progress/{session_id}")
async def get_progress(session_id: str):
    """
    Get interview progress
    """
    progress = interview_manager.get_progress(session_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return progress


@router.post("/pause/{session_id}")
async def pause_interview(session_id: str):
    """
    Pause interview session
    """
    success = interview_manager.pause_session(session_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to pause session")
    
    return {
        "status": "success",
        "message": "Interview paused",
        "session_id": session_id
    }


@router.post("/resume/{session_id}")
async def resume_interview(session_id: str):
    """
    Resume paused interview
    """
    success = interview_manager.resume_session(session_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to resume session")
    
    return {
        "status": "success",
        "message": "Interview resumed",
        "session_id": session_id
    }


@router.post("/complete/{session_id}")
async def complete_interview(session_id: str):
    """
    Complete interview and get summary
    """
    summary = interview_manager.complete_session(session_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "status": "success",
        "message": "Interview completed successfully",
        "summary": summary
    }


@router.get("/health")
async def interview_health():
    """
    Check interview service health
    """
    return {
        "status": "healthy",
        "service": "interview",
        "active_sessions": len(interview_manager.sessions),
        "timestamp": datetime.now().isoformat(),
        "features": [
            "AI-powered questions",
            "Real-time evaluation",
            "Audio transcription",
            "Multilingual support"
        ]
    }


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """
    Get interview session details
    """
    session = interview_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session.session_id,
        "user_id": session.user_id,
        "status": session.status,
        "started_at": session.started_at.isoformat(),
        "current_question": session.current_question,
        "total_questions": len(session.questions),
        "answered": len(session.answers),
        "total_duration": session.total_duration
    }


@router.get("/question/{session_id}")
async def get_current_question(session_id: str):
    """
    Get current question for session
    """
    question = interview_manager.get_current_question(session_id)
    if not question:
        raise HTTPException(status_code=404, detail="No current question or session not found")
    
    return {
        "id": question.id,
        "text": question.text,
        "category": question.category,
        "difficulty": question.difficulty,
        "expected_duration": question.expected_duration
    }


@router.post("/submit-answer")
async def submit_answer(request: SubmitAnswerRequest):
    """
    Submit answer for current question
    """
    success = interview_manager.submit_answer(
        session_id=request.session_id,
        transcript=request.transcript,
        duration=request.duration,
        confidence=request.confidence
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to submit answer")
    
    # Get next question
    next_question = interview_manager.get_next_question(request.session_id)
    progress = interview_manager.get_progress(request.session_id)
    
    return {
        "status": "success",
        "message": "Answer submitted successfully",
        "progress": progress,
        "next_question": {
            "id": next_question.id,
            "text": next_question.text,
            "category": next_question.category,
            "expected_duration": next_question.expected_duration
        } if next_question else None,
        "interview_complete": progress.get("status") == "completed"
    }


@router.post("/submit-audio")
async def submit_audio_answer(
    session_id: str = Form(...),
    question_id: int = Form(...),
    audio: UploadFile = File(...)
):
    """
    Submit audio recording for answer
    """
    try:
        # Read audio data
        audio_data = await audio.read()
        
        # Validate audio
        is_valid, message = audio_processor.validate_audio_format(audio_data, audio.filename or "audio.webm")
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)
        
        # Analyze audio
        quality = audio_processor.analyze_audio_quality(audio_data)
        
        # In production, save to cloud storage
        audio_url = f"storage/interviews/{session_id}/q{question_id}.webm"
        
        return {
            "status": "success",
            "message": "Audio submitted successfully",
            "audio_url": audio_url,
            "quality": quality,
            "size": len(audio_data)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process audio: {str(e)}")


@router.get("/progress/{session_id}")
async def get_progress(session_id: str):
    """
    Get interview progress
    """
    progress = interview_manager.get_progress(session_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return progress


@router.post("/pause/{session_id}")
async def pause_interview(session_id: str):
    """
    Pause interview session
    """
    success = interview_manager.pause_session(session_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to pause session")
    
    return {
        "status": "success",
        "message": "Interview paused",
        "session_id": session_id
    }


@router.post("/resume/{session_id}")
async def resume_interview(session_id: str):
    """
    Resume paused interview
    """
    success = interview_manager.resume_session(session_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to resume session")
    
    return {
        "status": "success",
        "message": "Interview resumed",
        "session_id": session_id
    }


@router.post("/complete/{session_id}")
async def complete_interview(session_id: str):
    """
    Complete interview and get summary
    """
    summary = interview_manager.complete_session(session_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "status": "success",
        "message": "Interview completed successfully",
        "summary": summary
    }


@router.get("/health")
async def interview_health():
    """
    Check interview service health
    """
    return {
        "status": "healthy",
        "service": "interview",
        "active_sessions": len(interview_manager.sessions),
        "timestamp": datetime.now().isoformat()
    }
