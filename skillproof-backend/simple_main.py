"""
Simple FastAPI Backend - No Database Required
Run with: python -m uvicorn simple_main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
import time

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

# In-memory storage (for demo)
users_db = {}

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("simple_main:app", host="0.0.0.0", port=8000, reload=True)
