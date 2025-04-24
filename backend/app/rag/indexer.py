from typing import Dict, Any, List, Optional, Union
import numpy as np

from app.db.session import DBSession
from app.ml.embeddings import generate_embedding

class DocumentIndexer:
    """Handles indexing of documents in the vector database."""
    
    def __init__(self):
        db_session = DBSession()
        self.supabase = db_session.get_supabase_client()
    
    def index_document(self, 
                      idea_id: int, 
                      title: str, 
                      content: str, 
                      metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Index a document in the vector database."""
        try:
            # Combine text for embedding generation
            text_to_embed = f"{title} {content}"
            embedding = generate_embedding(text_to_embed)
            
            # Prepare data for insertion
            data = {
                "idea_id": idea_id,
                "title": title,
                "content": content,
                "embedding": embedding.tolist()
            }
            
            # Add metadata if provided
            if metadata:
                for key, value in metadata.items():
                    data[key] = value
            
            # Insert into Supabase
            response = self.supabase.table("idea_embeddings").insert(data).execute()
            
            return True if hasattr(response, 'data') else False
        
        except Exception as e:
            print(f"Error indexing document: {e}")
            return False
    
    def batch_index_documents(self, documents: List[Dict[str, Any]]) -> List[bool]:
        """Index multiple documents in batch."""
        results = []
        for doc in documents:
            success = self.index_document(
                doc["idea_id"],
                doc["title"],
                doc["content"],
                doc.get("metadata")
            )
            results.append(success)
        return results
    
    def update_document(self, 
                       idea_id: int, 
                       title: Optional[str] = None, 
                       content: Optional[str] = None,
                       metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Update an existing document in the vector database."""
        try:
            # Fetch existing document
            response = self.supabase.table("idea_embeddings").select("*").eq("idea_id", idea_id).execute()
            
            if not hasattr(response, 'data') or len(response.data) == 0:
                return False
            
            # Prepare update data
            update_data = {}
            if title is not None or content is not None:
                # Get current values if not provided
                current_doc = response.data[0]
                current_title = current_doc.get("title", "")
                current_content = current_doc.get("content", "")
                
                title = title if title is not None else current_title
                content = content if content is not None else current_content
                
                # Generate new embedding
                text_to_embed = f"{title} {content}"
                embedding = generate_embedding(text_to_embed)
                
                update_data["title"] = title
                update_data["content"] = content
                update_data["embedding"] = embedding.tolist()
            
            # Add metadata updates if provided
            if metadata:
                for key, value in metadata.items():
                    update_data[key] = value
            
            # Update document
            if update_data:
                response = self.supabase.table("idea_embeddings").update(update_data).eq("idea_id", idea_id).execute()
                return True if hasattr(response, 'data') else False
            
            return True  # Nothing to update
            
        except Exception as e:
            print(f"Error updating document: {e}")
            return False
    
    def delete_document(self, idea_id: int) -> bool:
        """Delete a document from the vector database."""
        try:
            response = self.supabase.table("idea_embeddings").delete().eq("idea_id", idea_id).execute()
            return True if hasattr(response, 'data') else False
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False