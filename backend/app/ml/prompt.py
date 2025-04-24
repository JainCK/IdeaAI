from typing import List, Dict, Any, Optional

def create_prompt(
    topic: str, 
    keywords: List[str], 
    contexts: List[str], 
    customization: Optional[Dict[str, Any]] = None
) -> str:
    """Create a prompt for idea generation."""
    # Base prompt template
    prompt = f"Generate creative and innovative ideas related to '{topic}'"
    
    if keywords:
        prompt += f" using these keywords: {', '.join(keywords)}"
    
    if contexts:
        prompt += f". Consider these contexts: {', '.join(contexts)}"
    
    # Add customization parameters
    if customization and "template_params" in customization:
        template_params = customization["template_params"]
        
        if "audience" in template_params:
            prompt += f". Target audience: {template_params['audience']}"
            
        if "goal" in template_params:
            prompt += f". Goal: {template_params['goal']}"
            
        if "constraints" in template_params:
            prompt += f". Constraints: {template_params['constraints']}"
            
        if "tone" in template_params:
            prompt += f". Use a {template_params['tone']} tone"
            
        if "format" in template_params:
            prompt += f". Format each idea as: {template_params['format']}"
    
    # Default format instruction if not specified
    if not customization or not customization.get("template_params", {}).get("format"):
        prompt += ". Provide each idea with a title and a detailed description."
    
    # Additional instructions for better formatting
    prompt += " Separate each idea with a blank line. Format each idea as 'Title: Description'."
    
    return prompt

def create_custom_prompt(
    base_prompt: str, 
    customization: Dict[str, Any]
) -> str:
    """Create a custom prompt based on specific requirements."""
    prompt = base_prompt
    
    # Add any custom elements
    if "prefix" in customization:
        prompt = f"{customization['prefix']} {prompt}"
        
    if "suffix" in customization:
        prompt = f"{prompt} {customization['suffix']}"
        
    if "style" in customization:
        prompt += f" Use a {customization['style']} style."
        
    return prompt