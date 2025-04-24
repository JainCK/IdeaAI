from typing import List, Dict, Any, Optional, Union
import numpy as np

from app.db.session import DBSession
from app.ml.embeddings import generate_embedding

class DocumentRetriever:
    """Handles retrieval of documents from the vector database."""
    
    def __init__(self):
        db_session = DBSession()
        self.supabase = db_session.get_supabase_client()
    
    def search(self, 
              query: str, 
              top_k: int = 5, 
              similarity_threshold: float = 0.7,
              filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        try:
            # Generate query embedding
            query_embedding = generate_embedding(query)
            
            # Convert numpy array to Python list for JSON serialization
            query_embedding_list = query_embedding.tolist()
            
            # Prepare filter params if provided
            filter_params = {}
            if filters:
                filter_params["filters"] = filters
            
            # Execute semantic search
            response = self.supabase.rpc(
                "match_documents",
                {
                    "query_embedding": query_embedding_list,
                    "match_threshold": similarity_threshold,
                    "match_count": top_k,
                    "table_name": "idea_embeddings",
                    **filter_params
                }
            ).execute()
            
            if hasattr(response, 'data'):
                return response.data
            return []
            
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []
    
    def get_document(self, idea_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific document by its ID."""
        try:
            response = self.supabase.table("idea_embeddings").select("*").eq("idea_id", idea_id).execute()
            
            if hasattr(response, 'data') and len(response.data) > 0:
                return response.data[0]
            return None
            
        except Exception as e:
            print(f"Error getting document: {e}")
            return None