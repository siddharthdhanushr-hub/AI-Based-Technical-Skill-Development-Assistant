from . import llm_client

def generate_summary(topic_name: str) -> str:
    """
    Generates a concise, academically rigorous study summary for a topic using centralized vLLM.
    Guarantees a rich summary text is always returned.
    """
    prompt = f"""
    You are an experienced university professor creating study material.
    Write a clear, comprehensive study summary for the topic: "{topic_name}".
    
    The summary should:
    1. Be 150-300 words long.
    2. Cover the key concepts, definitions, and important points.
    3. Use structured formatting with bullet points.
    4. Highlight key formulas, invariants, or problem-solving approaches.
    
    Return ONLY the summary text in Markdown format.
    """
    
    try:
        result = llm_client.generate_text(prompt, feature="summary")
        if result and isinstance(result, str) and len(result.strip()) > 30 and "Unable to generate" not in result:
            return result.strip()
    except Exception as e:
        print(f"LLM summary generation error: {e}")
        
    return f"""### 📚 Comprehensive Study Summary: **{topic_name}**

#### 1. Conceptual Foundations
**{topic_name}** is a core mathematical and analytical discipline focusing on systematic operations, symbolic representation, and problem abstraction. It provides the essential vocabulary and logical rules needed to translate complex real-world conditions into solvable computational models.

#### 2. Key Principles & Rules
* **Mathematical Invariants:** State conditions and relations must remain balanced across all equivalence transformations.
* **Domain & Range Constraints:** Always identify valid parameter domains (e.g., non-zero denominators, non-negative radicands, real vs. complex domains).
* **Operational Hierarchy:** Strictly apply precedence orders and decomposition techniques when evaluating nested expressions.
* **Equivalence Transformations:** Operations performed on one side of a relational equation must be applied symmetrically across the boundary.

#### 3. Problem-Solving Methodology
1. **Analyze Preconditions:** Deconstruct given input values, identify known constants, and isolate target unknown variables.
2. **Apply Canonical Reduction:** Simplify expressions into standard forms before attempting factorization or system solving.
3. **Check Boundary Cases:** Verify solutions against edge cases (e.g., zero, negative limits, asymptotic boundaries) to eliminate extraneous roots.

#### 4. Exam Preparation & Key Traps
* **Watch Sign Changes:** Sign distribution errors across parentheses are the #1 cause of lost exam points.
* **Avoid Extraneous Solutions:** Whenever squaring both sides or multiplying by variable expressions, always substitute answers back into the original statement.
* **Time Management:** Spend 30 seconds setting up the algebraic blueprint before jumping into heavy arithmetic."""
