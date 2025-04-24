from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional

from app.api.models.request import IdeaRequest, IdeaWithCustomizationRequest
from app.api.models.response import IdeaResponse, Idea
from app.db.session import get_db, DBSession
from app.ml.generator import generate_ideas
from app.rag.indexer import DocumentIndexer

router = APIRouter(prefix="/ideas", tags=["ideas"])

@router.post("/", response_model=IdeaResponse)
async def create_ideas(request: IdeaWithCustomizationRequest, db: DBSession = Depends(get_db)):
    """Generate creative ideas based on input parameters."""
    # Generate ideas
    ideas = generate_ideas(
        topic=request.topic,
        keywords=request.keywords,
        contexts=request.contexts,
        num_ideas=request.num_ideas,
        creativity=request.creativity,
        max_length=request.max_length,
        customization=request.customization.dict() if request.customization else None
    )
    
    # Store ideas in PostgreSQL
    conn = db.get_postgres_connection()
    cursor = conn.cursor()
    
    stored_ideas = []
    indexer = DocumentIndexer()
    
    for idea in ideas:
        cursor.execute(
            """
            INSERT INTO ideas (title, description, topic, keywords)
            VALUES (%s, %s, %s, %s)
            RETURNING id, title, description, topic, keywords, created_at, avg_rating, feedback_count
            """,
            (idea["title"], idea["description"], request.topic, request.keywords)
        )
        stored_idea = cursor.fetchone()
        stored_ideas.append(dict(stored_idea))
        
        # Index for RAG
        indexer.index_document(
            idea_id=stored_idea["id"],
            title=idea["title"],
            content=idea["description"],
            metadata={
                "topic": request.topic,
                "keywords": request.keywords
            }
        )
    
    conn.commit()
    
    return {"ideas": stored_ideas}

@router.get("/", response_model=IdeaResponse)
async def get_ideas(
    skip: int = 0, 
    limit: int = 10, 
    topic: Optional[str] = None, 
    min_rating: Optional[float] = None,
    db: DBSession = Depends(get_db)
):
    """Get ideas with optional filtering."""
    conn = db.get_postgres_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM ideas WHERE 1=1"
    params = []
    
    if topic:
        query += " AND topic = %s"
        params.append(topic)
    
    if min_rating is not None:
        query += " AND avg_rating >= %s"
        params.append(min_rating)
    
    query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
    params.extend([limit, skip])
    
    cursor.execute(query, params)
    ideas = cursor.fetchall()
    
    return {"ideas": [dict(idea) for idea in ideas]}

@router.get("/{idea_id}", response_model=dict)
async def get_idea(idea_id: int, db: DBSession = Depends(get_db)):
    """Get a specific idea by ID with its feedback."""
    conn = db.get_postgres_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM ideas WHERE id = %s", (idea_id,))
    idea = cursor.fetchone()
    
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    # Get feedback
    cursor.execute("SELECT * FROM feedback WHERE idea_id = %s", (idea_id,))
    feedback = cursor.fetchall()
    
    return {
        "idea": dict(idea),
        "feedback": [dict(f) for f in feedback]
    }

@router.delete("/{idea_id}", response_model=dict)
async def delete_idea(idea_id: int, db: DBSession = Depends(get_db)):
    """Delete an idea and its associated data."""
    conn = db.get_postgres_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM ideas WHERE id = %s", (idea_id,))
    idea = cursor.fetchone()
    
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    # Delete from PostgreSQL (cascade will delete feedback)
    cursor.execute("DELETE FROM ideas WHERE id = %s", (idea_id,))
    
    # Delete from Vector DB
    indexer = DocumentIndexer()
    indexer.delete_document(idea_id)
    
    conn.commit()
    
    return {"status": "success", "message": "Idea deleted successfully"}

@router.get("/topics", response_model=dict)
async def get_topics(db: DBSession = Depends(get_db)):
    """Get all unique topics."""
    conn = db.get_postgres_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT topic FROM ideas ORDER BY topic")
    topics = cursor.fetchall()
    
    return {"topics": [t["topic"] for t in topics]}