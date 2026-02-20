from fastapi import APIRouter
from app.api.v1.endpoints import auth, resume

api_router = APIRouter()

api_router.include_router(auth.router, tags=["Authentication"])
api_router.include_router(resume.router, tags=["Resume"])
