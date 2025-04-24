import torch
import numpy as np
from typing import Union, List

from app.ml.model import get_model_manager

def generate_embedding(text: str) -> np.ndarray:
    """Generate an embedding vector for the given text."""
    model_manager = get_model_manager()
    
    # Get models
    tokenizer = model_manager.get_embedding_tokenizer()
    model = model_manager.get_embedding_model()
    
    # Tokenize input
    inputs = tokenizer(
        text, 
        return_tensors="pt", 
        truncation=True, 
        padding=True, 
        max_length=512
    ).to(model.device)
    
    # Generate embeddings
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Use mean pooling to get a single vector
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
    
    return embeddings

def batch_generate_embeddings(texts: List[str]) -> List[np.ndarray]:
    """Generate embeddings for multiple texts."""
    return [generate_embedding(text) for text in texts]

def compute_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """Compute cosine similarity between two embeddings."""
    # Normalize vectors
    embedding1_norm = embedding1 / np.linalg.norm(embedding1)
    embedding2_norm = embedding2 / np.linalg.norm(embedding2)
    
    # Compute cosine similarity
    similarity = np.dot(embedding1_norm, embedding2_norm)
    
    return float(similarity)

def compute_text_similarity(text1: str, text2: str) -> float:
    """Compute semantic similarity between two texts."""
    embedding1 = generate_embedding(text1)
    embedding2 = generate_embedding(text2)
    
    return compute_similarity(embedding1, embedding2)