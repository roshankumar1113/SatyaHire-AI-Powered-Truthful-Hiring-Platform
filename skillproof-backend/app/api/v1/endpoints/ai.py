"""
AI Endpoints - Interview question generation and answer analysis
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.ml.ai_client import get_ai_client, AIClientError, AIProvider

router = APIRouter()


class GenerateQuestionRequest(BaseModel):
    job_description: str
    candidate_background: str
    question_number: int


class AnalyzeAnswerRequest(BaseModel):
    question: str
    answer: str
    job_requirements: str


class GenerateTextRequest(BaseModel):
    prompt: str
    provider: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


@router.post("/generate-question")
async def generate_interview_question(request: GenerateQuestionRequest):
    """
    Generate AI interview question based on job description and candidate background.
    
    Example:
    ```json
    {
        "job_description": "Senior Python Developer with FastAPI experience",
        "candidate_background": "5 years Python, 2 years FastAPI",
        "question_number": 1
    }
    ```
    """
    try:
        ai_client = get_ai_client()
        
        question = ai_client.generate_interview_question(
            job_description=request.job_description,
            candidate_background=request.candidate_background,
            question_number=request.question_number,
        )
        
        return {
            "success": True,
            "question": question,
            "question_number": request.question_number,
        }
    
    except AIClientError as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating question: {str(e)}")


@router.post("/analyze-answer")
async def analyze_interview_answer(request: AnalyzeAnswerRequest):
    """
    Analyze candidate's interview answer using AI.
    
    Example:
    ```json
    {
        "question": "Tell me about your Python experience",
        "answer": "I have 5 years of Python experience...",
        "job_requirements": "Senior Python Developer"
    }
    ```
    """
    try:
        ai_client = get_ai_client()
        
        analysis = ai_client.analyze_interview_answer(
            question=request.question,
            answer=request.answer,
            job_requirements=request.job_requirements,
        )
        
        return {
            "success": True,
            "analysis": analysis,
        }
    
    except AIClientError as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing answer: {str(e)}")


@router.post("/generate-text")
async def generate_text(request: GenerateTextRequest):
    """
    Generate text using AI with custom prompt.
    
    Example:
    ```json
    {
        "prompt": "Write a professional email...",
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "max_tokens": 500
    }
    ```
    """
    try:
        ai_client = get_ai_client()
        
        # Convert provider string to enum if provided
        provider = None
        if request.provider:
            try:
                provider = AIProvider(request.provider)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid provider: {request.provider}")
        
        text = ai_client.generate_text(
            prompt=request.prompt,
            provider=provider,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        
        return {
            "success": True,
            "text": text,
            "provider": request.provider or "default",
        }
    
    except AIClientError as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")


@router.get("/status")
async def get_ai_status():
    """
    Get AI client status and available providers.
    
    Returns information about:
    - Available AI providers
    - Default provider
    - Model configuration
    - Key manager status
    """
    try:
        ai_client = get_ai_client()
        status = ai_client.get_status()
        
        return {
            "success": True,
            "status": status,
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting status: {str(e)}")


@router.get("/health")
async def ai_health_check():
    """
    Quick health check for AI services.
    Tests if at least one provider is available.
    """
    try:
        ai_client = get_ai_client()
        providers = ai_client.key_manager.get_available_providers()
        
        if not providers:
            return {
                "success": False,
                "message": "No AI providers configured",
                "healthy": False,
            }
        
        return {
            "success": True,
            "message": f"AI services healthy with {len(providers)} provider(s)",
            "healthy": True,
            "providers": [p.value for p in providers],
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"AI services unhealthy: {str(e)}",
            "healthy": False,
        }
