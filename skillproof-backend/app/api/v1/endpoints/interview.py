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

router = APIRouter()


class StartInterviewRequest(BaseModel):
    user_id: str


class SubmitAnswerRequest(BaseModel):
    session_id: str
    transcript: str
    duration: float
    confidence: float = 0.95


@router.post("/start")
async def start_interview(request: StartInterviewRequest):
    """
    Start a new interview session
    
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
        
        # Get first question
        first_question = interview_manager.get_current_question(session_id)
        
        return {
            "status": "success",
            "session_id": session_id,
            "started_at": session.started_at.isoformat(),
            "total_questions": len(session.questions),
            "current_question": {
                "id": first_question.id,
                "text": first_question.text,
                "category": first_question.category,
                "expected_duration": first_question.expected_duration
            } if first_question else None
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
