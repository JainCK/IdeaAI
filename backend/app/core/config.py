import os
from pydantic import BaseSettings, AnyHttpUrl
from typing import List, Optional, Dict, Any, Union
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Idea Generation API"
    PROJECT_DESCRIPTION: str = "A LLM-based idea generation platform with RAG capabilities"
    PROJECT_VERSION: str = "1.0.0"
    
    # Server settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # CORS settings
    CORS_ORIGINS: List[AnyHttpUrl] = ["*"]  
    
    # Database configuration
    NEON_DB_URL: str = os.getenv("NEON_DB_URL", "")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # Rate limiting configuration
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "60"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
    
    # ML Model configurations
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    EMBEDDING_DIMENSION: int = int(os.getenv("EMBEDDING_DIMENSION", "384"))
    GENERATION_MODEL: str = os.getenv("GENERATION_MODEL", "google/flan-t5-base")
    
    # Default generation parameters
    DEFAULT_MAX_LENGTH: int = int(os.getenv("DEFAULT_MAX_LENGTH", "200"))
    DEFAULT_NUM_IDEAS: int = int(os.getenv("DEFAULT_NUM_IDEAS", "5"))
    DEFAULT_CREATIVITY: float = float(os.getenv("DEFAULT_CREATIVITY", "0.7"))
    
    # Cache settings
    MODEL_CACHE_SIZE: int = int(os.getenv("MODEL_CACHE_SIZE", "2"))
    
    class Config:
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()