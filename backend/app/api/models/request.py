from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union

class IdeaRequest(BaseModel):
    """Request model for idea generation."""
    topic: str
    keywords: List[str] = Field(default_factory=list)
    contexts: List[str] = Field(default_factory=list)
    num_ideas: int = Field(default=5, ge=1, le=20)
    creativity: float = Field(default=0.7, ge=0.1, le=1.0)
    max_length: int = Field(default=200, ge=50, le=500)

class SearchRequest(BaseModel):
    """Request model for idea search."""
    query: str
    num_results: int = Field(default=5, ge=1, le=20)
    similarity_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    filters: Optional[Dict[str, Any]] = None

class FeedbackRequest(BaseModel):
    """Request model for submitting feedback."""
    idea_id: int
    rating: int = Field(ge=1, le=5)
    feedback: Optional[str] = None

class CustomizationOptions(BaseModel):
    """Model for customization options."""
    model_params: Dict[str, Any] = Field(default_factory=dict)
    template_params: Dict[str, Any] = Field(default_factory=dict)
    filters: Dict[str, Any] = Field(default_factory=dict)

class IdeaWithCustomizationRequest(IdeaRequest):
    """Request model with customization options."""
    customization: Optional[CustomizationOptions] = None