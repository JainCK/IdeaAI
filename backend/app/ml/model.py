import torch
from functools import lru_cache
from transformers import pipeline, AutoTokenizer, AutoModel

from app.core.config import settings

class ModelManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        self._models = {}
    
    @lru_cache(maxsize=settings.MODEL_CACHE_SIZE)
    def get_tokenizer(self, model_name):
        """Get or load a tokenizer."""
        if f"{model_name}_tokenizer" not in self._models:
            self._models[f"{model_name}_tokenizer"] = AutoTokenizer.from_pretrained(model_name)
        return self._models[f"{model_name}_tokenizer"]
    
    @lru_cache(maxsize=settings.MODEL_CACHE_SIZE)
    def get_model(self, model_name, task=None):
        """Get or load a model."""
        key = f"{model_name}_{task}" if task else model_name
        
        if key not in self._models:
            if task:
                self._models[key] = pipeline(task, model=model_name, device=self.device)
            else:
                self._models[key] = AutoModel.from_pretrained(model_name).to(self.device)
        
        return self._models[key]
    
    def get_embedding_model(self):
        """Get the embedding model."""
        return self.get_model(settings.EMBEDDING_MODEL)
    
    def get_embedding_tokenizer(self):
        """Get the embedding tokenizer."""
        return self.get_tokenizer(settings.EMBEDDING_MODEL)
    
    def get_generator(self):
        """Get the text generation pipeline."""
        return self.get_model(settings.GENERATION_MODEL, task="text2text-generation")
    
    def get_generator_tokenizer(self):
        """Get the generator tokenizer."""
        return self.get_tokenizer(settings.GENERATION_MODEL)

def get_model_manager():
    return ModelManager()