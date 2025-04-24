from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional, Dict, Any

from app.api.models.request import SearchRequest
from app.api.models.response import SearchResponse
from app.db.session import get_db, DBSession
from app.rag.retriever import DocumentRetriever

router = APIRouter(prefix="/search", tags=["search"])

@router.post("/", response_model=SearchResponse)
async def search_ideas(request: SearchRequest, db: DBSession = Depends(get_db)):
    """Search for ideas based on semantic similarity."""
    # Perform semantic search
    retriever = DocumentRetriever()
    results = retriever.search(
        query=request.query,
        top_k=request.num_results,
        similarity_threshold=request.similarity_threshold,
        filters=request.filters
    )
    
    # Fetch additional details if needed
    if results:
        conn = db.get_postgres_connection()
        cursor = conn.cursor()
        
        idea_ids = [result["idea_id"] for result in results]
        placeholder = ", ".join(["%s"] * len(idea_ids))
        
        cursor.execute(
            f"""
            SELECT id, title, description, topic, keywords, avg_rating, feedback_count
            FROM ideas 
            WHERE id IN ({placeholder})
            """,
            idea_ids
        )
        
        idea_details = cursor.fetchall()
        
        # Map idea details to results
        id_to_details = {item["id"]: item for item in idea_details}
        
        for result in results:
            idea_id = result["idea_id"]
            if idea_id in id_to_details:
                details = id_to_details[idea_id]
                result["title"] = details["title"]
                result["topic"] = details["topic"]
                result["keywords"] = details["keywords"]
    
    return {"results": results}

@router.post("/similar/{idea_id}", response_model=SearchResponse)
async def find_similar_ideas(
    idea_id: int, 
    top_k: int = 5, 
    similarity_threshold: float = 0.7,
    db: DBSession = Depends(get_db)
):
    """Find ideas similar to a specific idea."""
    # First get the idea
    conn = db.get_postgres_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM ideas WHERE id = %s", (idea_id,))
    idea = cursor.fetchone()
    
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    # Use the idea as the query
    query = f"{idea['title']} {idea['description']}"
    
    # Perform search
    retriever = DocumentRetriever()
    results = retriever.search(
        query=query,
        top_k=top_k + 1,  # +1 because the idea itself will be included
        similarity_threshold=similarity_threshold
    )
    
    # Filter out the original idea
    results = [r for r in results if r["idea_id"] != idea_id][:top_k]
    
    return {"results": results}