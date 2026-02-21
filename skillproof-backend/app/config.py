from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    # App
    APP_NAME: str = "SkillProof AI"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/skillproof"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000"]
    
    # AI API Keys (Multiple keys for rotation and fallback)
    OPENAI_API_KEYS: str = ""  # Comma-separated: sk-key1,sk-key2,sk-key3
    GEMINI_API_KEYS: str = ""  # Comma-separated: gemini_key1,gemini_key2
    ANTHROPIC_API_KEYS: str = ""  # Comma-separated: anthropic_key1,anthropic_key2
    
    # AI Configuration
    DEFAULT_AI_PROVIDER: str = "openai"  # openai, gemini, anthropic
    AI_MODEL: str = "gpt-3.5-turbo"
    AI_TEMPERATURE: float = 0.7
    AI_MAX_TOKENS: int = 1000
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def get_openai_keys(self) -> List[str]:
        """Parse comma-separated OpenAI keys"""
        if not self.OPENAI_API_KEYS:
            return []
        return [key.strip() for key in self.OPENAI_API_KEYS.split(",") if key.strip()]
    
    def get_gemini_keys(self) -> List[str]:
        """Parse comma-separated Gemini keys"""
        if not self.GEMINI_API_KEYS:
            return []
        return [key.strip() for key in self.GEMINI_API_KEYS.split(",") if key.strip()]
    
    def get_anthropic_keys(self) -> List[str]:
        """Parse comma-separated Anthropic keys"""
        if not self.ANTHROPIC_API_KEYS:
            return []
        return [key.strip() for key in self.ANTHROPIC_API_KEYS.split(",") if key.strip()]

@lru_cache()
def get_settings():
    return Settings()
