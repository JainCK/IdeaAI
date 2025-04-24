from fastapi import APIRouter, Depends, HTTPException

from app.api.models.request import FeedbackRequest
from app.api.models.response import FeedbackResponse
from app.db.session import get_db, DBSession

router = APIRouter(prefix="/feedback", tags=["feedback"])

@router.post("/", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest, db: DBSession = Depends(get_db)):
    """Submit feedback for an idea."""
    conn = db.get_postgres_connection()
    cursor = conn.cursor()
    
    # Check if idea exists
    cursor.execute("SELECT id FROM ideas WHERE id = %s", (request.idea_id,))
    idea = cursor.fetchone()
    
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    # Insert feedback
    cursor.execute(
        """
        INSERT INTO feedback (idea_id, rating, feedback)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (request.idea_id, request.rating, request.feedback)
    )
    feedback_id = cursor.fetchone()["id"]
    
    # Update average rating and feedback count
    cursor.execute(
        """
        UPDATE ideas
        SET 
            avg_rating = (SELECT AVG(rating) FROM feedback WHERE idea_id = %s),
            feedback_count = (SELECT COUNT(*) FROM feedback WHERE idea_id = %s)
        WHERE id = %s
        """,
        (request.idea_id, request.idea_id, request.idea_id)
    )
    
    conn.commit()
    
    return {"status": "Feedback submitted successfully", "feedback_id": feedback_id}

@router.get("/{idea_id}", response_model=dict)
async def get_feedback(idea_id: int, db: DBSession = Depends(get_db)):
    """Get all feedback for a specific idea."""
    conn = db.get_postgres_connection()
    cursor = conn.cursor()
    
    # Check if idea exists
    cursor.execute("SELECT id FROM ideas WHERE id = %s", (idea_id,))
    idea = cursor.fetchone()
    
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    # Get feedback
    cursor.execute("SELECT * FROM feedback WHERE idea_id = %s ORDER BY created_at DESC", (idea_id,))
    feedback = cursor.fetchall()
    
    return {"feedback": [dict(f) for f in feedback]}

@router.delete("/{feedback_id}", response_model=dict)
async def delete_feedback(feedback_id: int, db: DBSession = Depends(get_db)):
    """Delete a specific feedback."""
    conn = db.get_postgres_connection()
    cursor = conn.cursor()
    
    # Check if feedback exists
    cursor.execute("SELECT idea_id FROM feedback WHERE id = %s", (feedback_id,))
    feedback = cursor.fetchone()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    idea_id = feedback["idea_id"]
    
    # Delete feedback
    cursor.execute("DELETE FROM feedback WHERE id = %s", (feedback_id,))
    
    # Update average rating and feedback count
    cursor.execute(
        """
        UPDATE ideas
        SET 
            avg_rating = COALESCE((SELECT AVG(rating) FROM feedback WHERE idea_id = %s), 0),
            feedback_count = (SELECT COUNT(*) FROM feedback WHERE idea_id = %s)
        WHERE id = %s
        """,
        (idea_id, idea_id, idea_id)
    )
    
    conn.commit()
    
    return {"status": "success", "message": "Feedback deleted successfully"}