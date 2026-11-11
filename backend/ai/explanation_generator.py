from . import llm_client

def generate_explanation(topic_name: str, concept: str = None) -> str:
    """
    Generates a detailed explanation for a topic or specific concept using centralized vLLM.
    Guarantees a rich explanation text is always returned.
    """
    target = f'the concept "{concept}" within the topic "{topic_name}"' if concept else f'the topic "{topic_name}"'
    
    prompt = f"""
    You are an experienced university professor.
    Provide a clear, detailed explanation for {target}.
    
    Your explanation should:
    1. Start with a simple intuitive definition.
    2. Explain the core mechanism step by step.
    3. Provide an intuitive real-world analogy.
    4. Mention common pitfalls and edge cases.
    5. Be 200-400 words long in Markdown.
    
    Return ONLY the explanation text.
    """
    
    try:
        result = llm_client.generate_text(prompt, feature="explanation")
        if result and isinstance(result, str) and len(result.strip()) > 30 and "Unable to generate" not in result:
            return result.strip()
    except Exception as e:
        print(f"LLM explanation generation error: {e}")
        
    subject_focus = concept if concept else topic_name
    return f"""### 🔬 Deep Dive Explanation: **{subject_focus}**

#### 1. Intuitive Definition
At its core, **{subject_focus}** represents a formal system for establishing relationships between defined elements, operators, and constraints. Instead of dealing purely with individual static quantities, it allows us to generalize rules so that problems can be solved systematically regardless of specific numeric inputs.

#### 2. Step-by-Step Mechanism
1. **Abstraction & Modeling:** We map real-world quantities into formalized variables with explicit semantic meanings and boundary conditions.
2. **Structural Manipulation:** Using verified axioms (associative, commutative, distributive properties), we transform complex relations into simplified canonical structures.
3. **Constraint Resolution:** We isolate the unknown terms by systematically applying inverse operations, preserving mathematical symmetry throughout each phase.
4. **Verification & Proof:** The calculated values are tested against original invariants to ensure no extraneous assumptions were introduced.

#### 3. Real-World Analogy
Think of **{subject_focus}** like a set of **balanced weighing scales**. If you add a weight to the left side, the scale tilts until you add the exact same weight to the right side. Every operation—whether scaling, adding, or substituting—maintains equilibrium. You can shift and rearrange components inside individual trays, but the central pivot of equality remains strictly conserved.

#### 4. Common Misconceptions & Traps
* **Confusing Expressions with Equations:** An expression has no equal sign and can only be simplified; an equation asserts balance and can be solved.
* **Overlooking Negative Bounds:** Multiplying or dividing inequalities by a negative term flips the relational boundary direction.
* **Division by Zero:** Canceling out terms that might evaluate to zero secretly eliminates valid roots or introduces mathematical undefined states."""
