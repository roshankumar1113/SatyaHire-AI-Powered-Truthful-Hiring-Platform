"""
Multilingual Interview API Endpoints
Handles multilingual AI interviews in Indian languages
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict

from app.services.multilingual_interviewer import (
    multilingual_interviewer,
    InterviewRequest,
    InterviewResponse,
    SUPPORTED_LANGUAGES,
    LANGUAGE_NAMES
)

router = APIRouter()


class StartInterviewRequest(BaseModel):
    role: str
    experience_level: str  # junior, mid, senior
    language: str
    max_questions: int = 5


class SubmitAnswerRequest(BaseModel):
    role: str
    experience_level: str
    language: str
    max_questions: int
    question_number: int
    previous_question: str
    candidate_answer: str


@router.get("/languages")
async def get_supported_languages():
    """
    Get list of supported interview languages
    
    Returns:
        List of supported languages with codes and names
    """
    return {
        "status": "success",
        "languages": multilingual_interviewer.get_supported_languages(),
        "total": len(SUPPORTED_LANGUAGES)
    }


@router.post("/start")
async def start_multilingual_interview(request: StartInterviewRequest):
    """
    Start a new multilingual interview
    
    Args:
        request: Interview configuration
        
    Returns:
        First interview question in selected language
    """
    try:
        # Validate language
        if not multilingual_interviewer.validate_language(request.language):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language: {request.language}. Supported: {', '.join(SUPPORTED_LANGUAGES)}"
            )
        
        # Generate first question
        response = multilingual_interviewer.generate_first_question(
            role=request.role,
            experience_level=request.experience_level,
            language=request.language,
            max_questions=request.max_questions
        )
        
        return {
            "status": "success",
            "message": f"Interview started in {LANGUAGE_NAMES.get(request.language, request.language)}",
            "data": {
                "question": response.question,
                "difficulty": response.difficulty,
                "interview_status": response.interview_status,
                "question_number": 1,
                "total_questions": request.max_questions,
                "language": request.language
            }
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start interview: {str(e)}")


@router.post("/submit-answer")
async def submit_answer(request: SubmitAnswerRequest):
    """
    Submit answer and get evaluation + next question
    
    Args:
        request: Answer submission with interview context
        
    Returns:
        Evaluation of answer and next question
    """
    try:
        # Validate language
        if not multilingual_interviewer.validate_language(request.language):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language: {request.language}"
            )
        
        # Evaluate and get next question
        response = multilingual_interviewer.evaluate_and_next_question(
            role=request.role,
            experience_level=request.experience_level,
            language=request.language,
            max_questions=request.max_questions,
            question_number=request.question_number,
            previous_question=request.previous_question,
            candidate_answer=request.candidate_answer
        )
        
        # Prepare response
        result = {
            "status": "success",
            "data": {
                "question": response.question,
                "difficulty": response.difficulty,
                "interview_status": response.interview_status,
                "question_number": request.question_number + 1,
                "total_questions": request.max_questions,
                "language": request.language
            }
        }
        
        # Add evaluation if present
        if response.evaluation:
            result["data"]["evaluation"] = {
                "score": response.evaluation.score,
                "strengths": response.evaluation.strengths,
                "improvements": response.evaluation.improvements,
                "corrected_answer": response.evaluation.corrected_answer
            }
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process answer: {str(e)}")


@router.post("/generate-question")
async def generate_custom_question(request: InterviewRequest):
    """
    Generate a custom interview question
    
    Args:
        request: Full interview request
        
    Returns:
        Generated question
    """
    try:
        response = multilingual_interviewer.conduct_interview(request)
        
        return {
            "status": "success",
            "data": {
                "question": response.question,
                "difficulty": response.difficulty,
                "interview_status": response.interview_status
            }
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate question: {str(e)}")


@router.get("/language-info/{language_code}")
async def get_language_info(language_code: str):
    """
    Get information about a specific language
    
    Args:
        language_code: Language code (e.g., 'hindi', 'tamil')
        
    Returns:
        Language information
    """
    if language_code.lower() not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=404,
            detail=f"Language not found: {language_code}"
        )
    
    return {
        "status": "success",
        "data": {
            "code": language_code.lower(),
            "name": LANGUAGE_NAMES.get(language_code.lower(), language_code.capitalize()),
            "native_name": LANGUAGE_NAMES.get(language_code.lower(), language_code.capitalize()),
            "supported": True
        }
    }


@router.get("/experience-levels")
async def get_experience_levels():
    """
    Get supported experience levels
    
    Returns:
        List of experience levels
    """
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


@router.get("/health")
async def multilingual_interview_health():
    """
    Health check for multilingual interview service
    
    Returns:
        Service health status
    """
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


@router.post("/test-prompt")
async def test_prompt(request: InterviewRequest):
    """
    Test the AI prompt generation (for debugging)
    
    Args:
        request: Interview request
        
    Returns:
        Generated prompts
    """
    try:
        system_prompt = multilingual_interviewer._get_system_prompt()
        user_prompt = multilingual_interviewer._get_user_prompt(request)
        
        return {
            "status": "success",
            "data": {
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "language": request.language,
                "role": request.role
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
