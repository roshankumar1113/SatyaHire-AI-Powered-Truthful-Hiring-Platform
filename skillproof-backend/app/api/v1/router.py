from fastapi import APIRouter
from app.api.v1.endpoints import auth, resume, ai, voice, interview

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(resume.router, prefix="/resume", tags=["Resume"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI Services"])
api_router.include_router(voice.router, prefix="/voice", tags=["Voice & Audio"])
api_router.include_router(interview.router, prefix="/interview", tags=["Interview Management"])
