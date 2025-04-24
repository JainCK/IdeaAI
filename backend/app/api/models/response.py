from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class Idea(BaseModel):
    """Model for an idea."""
    id: int
    title: str
    description: str
    topic: str
    keywords: List[str]
    avg_rating: float = 0.0
    feedback_count: int = 0
    created_at: datetime
    
    class Config:
        orm_mode = True

class Feedback(BaseModel):
    """Model for feedback."""
    id: int
    idea_id: int
    rating: int
    feedback: Optional[str] = None
    created_at: datetime
    
    class Config:
        orm_mode = True

class SearchResult(BaseModel):
    """Model for search result."""
    id: int
    idea_id: int
    title: str
    content: str
    topic: Optional[str] = None
    keywords: Optional[List[str]] = None
    similarity_score: float
    
    class Config:
        orm_mode = True

class IdeaResponse(BaseModel):
    """Response model for idea generation."""
    ideas: List[Idea]

class SearchResponse(BaseModel):
    """Response model for search."""
    results: List[SearchResult]

class FeedbackResponse(BaseModel):
    """Response model for feedback submission."""
    status: str
    feedback_id: int

class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    timestamp: float