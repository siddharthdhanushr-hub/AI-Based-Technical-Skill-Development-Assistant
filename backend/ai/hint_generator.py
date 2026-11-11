from . import llm_client

def generate_hints(topic_name: str, num_hints: int = 3) -> list:
    """
    Generates study hints/tips for a topic using centralized vLLM.
    """
    prompt = f"""
    You are an experienced university professor helping students study effectively.
    Generate {num_hints} practical study hints/tips for the topic: "{topic_name}".
    
    Each hint should be a short, actionable piece of advice that helps a student
    understand or remember the topic better.
    
    Return the response STRICTLY as a JSON array of strings:
    ["Hint 1 text...", "Hint 2 text...", "Hint 3 text..."]
    """
    
    result = llm_client.generate_json(prompt, feature="hint")
    
    if isinstance(result, list) and len(result) > 0:
        return result
    
    return [
        f"Break down {topic_name} into its core components and master one part at a time.",
        f"Work through practical examples to solidify your conceptual understanding of {topic_name}.",
        f"Review boundary conditions and common pitfalls relevant to {topic_name}."
    ][:num_hints]
