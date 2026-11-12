from . import llm_client

def _build_fallback_questions_for_topic(topic: str) -> list:
    return [
        {
            "question_text": f"Which statement best captures the core conceptual foundation of {topic}?",
            "option_a": f"It formalizes underlying rules, mathematical logic, and analytical models for {topic}.",
            "option_b": "It is an unverified empirical heuristic without analytical backing.",
            "option_c": "It applies exclusively to deprecated legacy computing platforms.",
            "option_d": "It requires zero consideration of computational resources or state.",
            "correct_option": "A",
            "explanation": f"{topic} is built upon formal principles designed to guarantee consistent, verifiable problem-solving.",
            "difficulty": "Easy",
            "topic": topic
        },
        {
            "question_text": f"When establishing the initial problem formulation in {topic}, what is standard practice?",
            "option_a": "Ignore boundary constraints until production runtime.",
            "option_b": f"Precisely define input preconditions, expected invariants, and postconditions for {topic}.",
            "option_c": "Assume all input instances are trivial and uniformly distributed.",
            "option_d": "Avoid verifying type correctness or mathematical domains.",
            "correct_option": "B",
            "explanation": f"Rigorous engineering in {topic} requires explicit definition of preconditions, invariants, and expected outcomes.",
            "difficulty": "Easy",
            "topic": topic
        },
        {
            "question_text": f"What primary trade-off must be analyzed when selecting an approach in {topic}?",
            "option_a": "Time efficiency versus memory overhead and implementation complexity.",
            "option_b": "Correctness versus random non-deterministic output.",
            "option_c": "Source code line count versus processor clock speed.",
            "option_d": "Network bandwidth versus screen resolution.",
            "correct_option": "A",
            "explanation": f"Selecting the optimal technique in {topic} involves balancing asymptotic runtime, memory footprint, and architectural maintainability.",
            "difficulty": "Medium",
            "topic": topic
        },
        {
            "question_text": f"Which scenario represents a common misconception when studying {topic}?",
            "option_a": "Recognizing that asymptotic complexity only bounds large-scale growth.",
            "option_b": "Validating edge conditions such as null, empty, or singular inputs.",
            "option_c": f"Assuming best-case performance is guaranteed across all adversarial inputs in {topic}.",
            "option_d": "Decomposing complex instances into manageable modular sub-problems.",
            "correct_option": "C",
            "explanation": f"Students frequently mistake optimistic best-case behavior for guaranteed worst-case bounds in {topic}.",
            "difficulty": "Medium",
            "topic": topic
        },
        {
            "question_text": f"In {topic}, how should unexpected inputs or edge anomalies be mitigated?",
            "option_a": "Bypass exception handlers to preserve raw processor speed.",
            "option_b": "Incorporate defensive validation checks and enforce strict contract bounds.",
            "option_c": "Silently terminate execution without logging diagnostic state.",
            "option_d": "Hardcode speculative values for all unrecognized parameters.",
            "correct_option": "B",
            "explanation": f"Robust implementations in {topic} employ defensive assertion checks, explicit contracts, and graceful error handling.",
            "difficulty": "Medium",
            "topic": topic
        },
        {
            "question_text": f"What is the mathematical or theoretical rationale behind asymptotic analysis in {topic}?",
            "option_a": "To predict performance trends as the input magnitude scales toward infinity.",
            "option_b": "To measure exact CPU cycle counts on a specific manufacturer's silicon.",
            "option_c": "To convert continuous differential equations into discrete boolean values.",
            "option_d": "To eliminate the necessity of algorithmic profiling and empirical testing.",
            "correct_option": "A",
            "explanation": f"Asymptotic notations (O, Omega, Theta) describe limiting behavior independent of machine-dependent constants.",
            "difficulty": "Hard",
            "topic": topic
        },
        {
            "question_text": f"When refactoring an inefficient sub-routine within {topic}, which strategy yields the greatest performance improvement?",
            "option_a": "Loop unrolling without addressing underlying nested algorithmic loops.",
            "option_b": "Replacing descriptive identifiers with single-character variable names.",
            "option_c": "Switching to an optimal algorithmic paradigm that reduces exponential/polynomial complexity.",
            "option_d": "Allocating redundant auxiliary arrays across each recursion depth.",
            "correct_option": "C",
            "explanation": f"Algorithmic paradigm improvements (e.g., dynamic programming, divide-and-conquer) fundamentally reduce asymptotic order of growth.",
            "difficulty": "Hard",
            "topic": topic
        },
        {
            "question_text": f"Which design invariant is critical for maintaining data integrity throughout workflows in {topic}?",
            "option_a": "Maintaining state consistency across asynchronous transformations and mutations.",
            "option_b": "Permitting arbitrary uncontrolled side-effects across all helper functions.",
            "option_c": "Restricting data models strictly to global mutable state arrays.",
            "option_d": "Eliminating idempotency in iterative numerical recalculations.",
            "correct_option": "A",
            "explanation": f"Data integrity in {topic} relies on preserving state consistency, purity where applicable, and atomicity.",
            "difficulty": "Hard",
            "topic": topic
        },
        {
            "question_text": f"How do advanced practitioners verify the empirical correctness of implementations in {topic}?",
            "option_a": "Comprehensive automated unit testing, fuzzing edge cases, and formal invariant validation.",
            "option_b": "Single-case manual inspection under idealized conditions.",
            "option_c": "Relying strictly on runtime exception suppression.",
            "option_d": "Assuming theoretical proof guarantees absence of implementation bugs.",
            "correct_option": "A",
            "explanation": f"Verification in {topic} combines formal invariant proofs with automated unit tests and stress testing with boundary cases.",
            "difficulty": "Medium",
            "topic": topic
        },
        {
            "question_text": f"In a competitive examination setting, what is the most effective approach for complex problems in {topic}?",
            "option_a": "Begin coding immediately without identifying known sub-patterns.",
            "option_b": f"Identify foundational patterns, state constraints, formulate the mathematical relation, and systematically solve.",
            "option_c": "Skip checking intermediate steps and verify only the final numerical magnitude.",
            "option_d": "Guess based on distractor option symmetry.",
            "correct_option": "B",
            "explanation": f"High exam performance in {topic} requires systematic pattern identification, constraint verification, and step-by-step reasoning.",
            "difficulty": "Hard",
            "topic": topic
        }
    ]

def generate_mocktest(topic_names: list, num_questions: int = 10) -> list:
    """
    Generates a full mock test across multiple topics using centralized vLLM.
    Returns a mix of easy, medium, and hard MCQs. Always returns num_questions.
    """
    if not topic_names:
        topic_names = ["General Study Topics"]
        
    topics_str = ", ".join(topic_names)
    
    prompt = f"""
    You are an experienced university professor creating a mock exam.
    Generate a mock test with exactly {num_questions} Multiple Choice Questions (MCQs) covering these topics: {topics_str}.
    
    Rules:
    1. Mix difficulty levels: approximately 30% Easy, 40% Medium, 30% Hard.
    2. Spread questions evenly across the given topics.
    3. Each question must have four choices (option_a, option_b, option_c, option_d) and a correct_option (A, B, C, or D).
    
    Return the response STRICTLY as a JSON array:
    [
      {{
        "question_text": "...",
        "option_a": "...",
        "option_b": "...",
        "option_c": "...",
        "option_d": "...",
        "correct_option": "A",
        "explanation": "...",
        "difficulty": "Easy",
        "topic": "..."
      }}
    ]
    """
    
    try:
        result = llm_client.generate_json(prompt, feature="mocktest")
        if isinstance(result, list) and len(result) >= num_questions:
            return result[:num_questions]
        elif isinstance(result, list) and len(result) > 0:
            # Pad with fallbacks if LLM returned fewer than requested
            collected = list(result)
            while len(collected) < num_questions:
                t = topic_names[len(collected) % len(topic_names)]
                fallback_pool = _build_fallback_questions_for_topic(t)
                collected.append(fallback_pool[len(collected) % len(fallback_pool)])
            return collected[:num_questions]
    except Exception as e:
        print(f"LLM mocktest generation error: {e}")
        
    # Full reliable fallback generation
    questions = []
    pool_per_topic = {t: _build_fallback_questions_for_topic(t) for t in topic_names}
    
    idx = 0
    while len(questions) < num_questions:
        topic = topic_names[idx % len(topic_names)]
        pool = pool_per_topic[topic]
        q = pool[(idx // len(topic_names)) % len(pool)]
        questions.append(q)
        idx += 1
        
    return questions[:num_questions]
