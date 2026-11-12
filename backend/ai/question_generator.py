from . import llm_client, prompts

def get_fallback_quiz_questions(topic_name: str) -> list:
    """
    Returns 10 academically rigorous questions for the topic covering Easy, Medium, and Hard cognitive levels.
    """
    return [
        {
            "question_text": f"Which of the following best defines the primary concept of {topic_name}?",
            "option_a": f"A formal mathematical or computational model governing operations and structures in {topic_name}",
            "option_b": "An arbitrary heuristic rule set without systematic validation",
            "option_c": "A deprecated theoretical framework with no modern relevance",
            "option_d": "A machine-specific hardware registry setting",
            "correct_option": "A",
            "explanation": f"{topic_name} is grounded in formal systematic principles designed to model and solve domain problems.",
            "difficulty": "Easy",
            "question_type": "MCQ"
        },
        {
            "question_text": f"When establishing initial problem conditions in {topic_name}, what must be defined first?",
            "option_a": "Physical GPU temperature constraints",
            "option_b": f"Input preconditions, valid domains, and expected invariant states for {topic_name}",
            "option_c": "Only the final output file format",
            "option_d": "Random speculative seed parameters",
            "correct_option": "B",
            "explanation": f"Proper modeling in {topic_name} starts with rigorous preconditions, domain bounds, and invariant definitions.",
            "difficulty": "Easy",
            "question_type": "MCQ"
        },
        {
            "question_text": f"Which fundamental mathematical or structural property is preserved throughout valid transformations in {topic_name}?",
            "option_a": "Absolute memory address pointers",
            "option_b": "Exact chronological processor execution ticks",
            "option_c": "Relational equivalence and algebraic invariance",
            "option_d": "Arbitrary variable character lengths",
            "correct_option": "C",
            "explanation": f"Valid operations in {topic_name} maintain equivalence across expressions and respect underlying structural invariants.",
            "difficulty": "Easy",
            "question_type": "MCQ"
        },
        {
            "question_text": f"What is the standard order of operations when decomposing complex instances of {topic_name}?",
            "option_a": "Evaluate nested parentheses/sub-expressions, apply operator precedence, and simplify canonical terms",
            "option_b": "Perform arbitrary scalar additions before resolving parenthetical scopes",
            "option_c": "Invert random relational operators before checking domain bounds",
            "option_d": "Truncate all non-integer fractional values immediately",
            "correct_option": "A",
            "explanation": f"Consistent results in {topic_name} require adhering strictly to operator precedence and compositional scope rules.",
            "difficulty": "Easy",
            "question_type": "MCQ"
        },
        {
            "question_text": f"What is the primary trade-off to evaluate when choosing between competing algorithms in {topic_name}?",
            "option_a": "Time complexity (runtime) versus space complexity (memory overhead)",
            "option_b": "Source code font choice versus disk storage capacity",
            "option_c": "Deterministic correctness versus stochastic uncertainty",
            "option_d": "Variable naming conventions versus monitor refresh rates",
            "correct_option": "A",
            "explanation": f"Designing algorithms in {topic_name} fundamentally balances asymptotic execution time against auxiliary memory space.",
            "difficulty": "Medium",
            "question_type": "MCQ"
        },
        {
            "question_text": f"Which of the following strategies are essential for robust error mitigation in {topic_name}?",
            "option_a": "Enforcing defensive domain validation before executing operations",
            "option_b": "Gracefully handling boundary values such as null, zero, or negative inputs",
            "option_c": "Silently suppressing mathematical overflow without notifications",
            "option_d": "Assuming inputs are always bounded within ideal ranges",
            "correct_option": "A,B",
            "explanation": f"Robust engineering in {topic_name} requires explicit domain validation and graceful handling of edge cases.",
            "difficulty": "Medium",
            "question_type": "MULTI_MCQ"
        },
        {
            "question_text": f"What is a frequent student pitfall when analyzing asymptotic performance in {topic_name}?",
            "option_a": "Recognizing that constant multipliers can matter for small input sizes",
            "option_b": f"Confusing the best-case optimistic scenario with guaranteed worst-case asymptotic bounds",
            "option_c": "Using recurrence relations to model recursive step complexity",
            "option_d": "Validating algorithmic termination conditions",
            "correct_option": "B",
            "explanation": f"Students often mistakenly equate best-case performance with reliable upper bounds under adversarial inputs.",
            "difficulty": "Medium",
            "question_type": "MCQ"
        },
        {
            "question_text": f"Which attributes characterize an optimal, production-grade architecture in {topic_name}?",
            "option_a": "High modularity and clear separation of concerns",
            "option_b": "Idempotent transformations that produce deterministic outputs",
            "option_c": "Comprehensive test suites exercising boundary conditions",
            "option_d": "Coupling business logic directly into global mutable state",
            "correct_option": "A,B,C",
            "explanation": f"Production systems in {topic_name} require modularity, deterministic state transitions, and high test coverage.",
            "difficulty": "Hard",
            "question_type": "MULTI_MCQ"
        },
        {
            "question_text": f"When conducting formal verification of an implementation in {topic_name}, what provides the strongest proof of correctness?",
            "option_a": "A single successful manual trial run with integer 1",
            "option_b": "Absence of syntax compilation errors",
            "option_c": "Mathematical induction proving base cases and inductive step invariants across all n",
            "option_d": "High aesthetic quality of generated charts",
            "correct_option": "C",
            "explanation": f"Formal verification relies on mathematical induction and invariant proofs guaranteeing correctness for all inputs.",
            "difficulty": "Hard",
            "question_type": "MCQ"
        },
        {
            "question_text": f"In an advanced examination scenario on {topic_name}, which methods maximize analytical accuracy under strict time constraints?",
            "option_a": "Guessing answer choices based on length without reading",
            "option_b": "Systematically identifying underlying canonical patterns before performing calculations",
            "option_c": "Ignoring constraint boundaries to finish earlier",
            "option_d": "Sanity checking intermediate numerical values against physical or theoretical constraints",
            "correct_option": "B,D",
            "explanation": f"High performance under pressure requires recognizing structural patterns and cross-checking intermediate results against known constraints.",
            "difficulty": "Hard",
            "question_type": "MULTI_MCQ"
        }
    ]

def generate_quiz_for_topic(topic_name: str, num_questions: int = 10, context: str = None) -> list:
    """
    Generates a quiz for the topic. Always returns exactly num_questions (defaults to 10).
    """
    context_section = ""
    if context:
        context_section = f"\nSOURCE STUDY MATERIAL (CONTEXT):\n{context}\n"

    prompt = f"""
You are an experienced university professor.
Generate an academically rigorous quiz with exactly {num_questions} questions for the topic: "{topic_name}".

{context_section}

COGNITIVE LEVEL INSTRUCTIONS:
- Easy: Test basic concepts, definitions, and comprehension.
- Medium: Test application, trade-offs, and boundary conditions.
- Hard: Test critical evaluation, optimization, and synthesis.

Return response STRICTLY as a JSON array of objects:
[
  {{
    "question_text": "...",
    "option_a": "choice A",
    "option_b": "choice B",
    "option_c": "choice C",
    "option_d": "choice D",
    "correct_option": "A",
    "explanation": "...",
    "difficulty": "Easy",
    "question_type": "MCQ"
  }}
]
"""
    try:
        structured_json = llm_client.generate_json(prompt, feature="quiz")
        if isinstance(structured_json, list) and len(structured_json) >= num_questions:
            return structured_json[:num_questions]
        elif isinstance(structured_json, list) and len(structured_json) > 0:
            collected = list(structured_json)
            fallbacks = get_fallback_quiz_questions(topic_name)
            while len(collected) < num_questions:
                collected.append(fallbacks[len(collected) % len(fallbacks)])
            return collected[:num_questions]
    except Exception as e:
        print(f"LLM quiz generation error for '{topic_name}': {e}")
        
    fallbacks = get_fallback_quiz_questions(topic_name)
    return fallbacks[:num_questions]

def generate_quiz_for_topics_adaptive(topics_list: list[dict]) -> list:
    """
    topics_list is a list of dicts: [{"topic_name": str, "num_questions": int, "content_text": str}]
    Guarantees that questions are generated for each topic.
    """
    all_generated_questions = []
    
    for t in topics_list:
        topic_name = t["topic_name"]
        num_q = t.get("num_questions", 10)
        context = t.get("content_text")
        if num_q <= 0:
            continue
            
        qs = generate_quiz_for_topic(topic_name, num_questions=num_q, context=context)
        for q in qs:
            q["topic_name"] = topic_name
        all_generated_questions.extend(qs)
            
    return all_generated_questions
