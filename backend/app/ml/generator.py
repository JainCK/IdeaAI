from typing import Dict, Any, List, Optional
from app.ml.model import get_model_manager
from app.ml.prompt import create_prompt

def generate_ideas(
    topic: str,
    keywords: List[str],
    contexts: List[str],
    num_ideas: int = 5,
    creativity: float = 0.7,
    max_length: int = 200,
    customization: Optional[Dict[str, Any]] = None
) -> List[Dict[str, str]]:
    """Generate creative ideas based on input parameters."""
    model_manager = get_model_manager()
    generator = model_manager.get_generator()
    
    # Create prompt
    prompt = create_prompt(topic, keywords, contexts, customization)
    
    # Configure generation parameters
    gen_params = {
        "max_length": max_length,
        "temperature": creativity,
        "num_return_sequences": 1,
        "do_sample": True
    }
    
    # Apply custom model parameters if provided
    if customization and "model_params" in customization:
        gen_params.update(customization["model_params"])
    
    # Generate ideas
    results = generator(prompt, **gen_params)
    
    # Process results
    ideas = process_generation_result(results, num_ideas)
    
    return ideas

def process_generation_result(results, num_ideas=5) -> List[Dict[str, str]]:
    """Process raw generation results into structured ideas."""
    try:
        # Extract generated text
        text = results[0]['generated_text']
        
        # Split into ideas
        ideas = []
        for i, idea_text in enumerate(text.split("\n\n")[:num_ideas]):
            if not idea_text.strip():
                continue
                
            parts = idea_text.split(":", 1)
            if len(parts) == 2:
                title, description = parts
            else:
                title = f"Idea {i+1}"
                description = idea_text
                
            ideas.append({
                "title": title.strip(),
                "description": description.strip()
            })
        
        return ideas
    except Exception as e:
        print(f"Error processing generation result: {e}")
        return [{"title": "Generated Idea", "description": results[0]['generated_text']}]