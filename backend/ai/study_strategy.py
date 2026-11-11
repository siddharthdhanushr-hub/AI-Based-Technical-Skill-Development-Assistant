from . import llm_client

def generate_study_strategy(topic_names: list, days_until_exam: int, hours_per_day: float = 3.0) -> dict:
    """
    Generates a personalized study strategy based on topics and time available using centralized vLLM.
    Guarantees a rich, actionable strategy response.
    """
    if not topic_names:
        topic_names = ["Core Subject Fundamentals"]
        
    topics_str = ", ".join(topic_names)
    days_until_exam = max(1, days_until_exam or 14)
    hours_per_day = float(hours_per_day or 3.0)
    total_hours = round(days_until_exam * hours_per_day, 1)
    
    prompt = f"""
    You are an expert academic advisor helping a student prepare for an exam.
    
    The student needs to study these topics: {topics_str}
    Days until exam: {days_until_exam}
    Available study hours per day: {hours_per_day}
    
    Create a personalized study strategy. Include:
    1. A recommended study order (which topics to tackle first and why).
    2. Time allocation per topic (in hours).
    3. Suggested study techniques for each topic.
    4. A daily study schedule outline.
    5. Tips for revision in the final days.
    
    Return the response as JSON:
    {{
      "strategy_summary": "Brief overall strategy description",
      "topic_order": ["Topic1", "Topic2"],
      "time_allocation": [{{"topic": "Topic1", "hours": 5, "technique": "Active recall + practice problems"}}],
      "daily_plan": [{{"day": 1, "focus": "Topic1", "activities": "Read chapter, solve 10 problems"}}],
      "revision_tips": ["Tip 1", "Tip 2"],
      "motivation": "A short motivational message"
    }}
    """
    
    try:
        result = llm_client.generate_json(prompt, feature="study_strategy")
        if isinstance(result, dict) and "strategy_summary" in result and result.get("strategy_summary") != "Unable to generate strategy. Please try again.":
            return result
    except Exception as e:
        print(f"LLM study strategy generation error: {e}")
    
    # High-quality fallback strategy tailored to the specific topics
    allocated_per_topic = round(total_hours / max(1, len(topic_names)), 1)
    techniques = [
        "Feynman Technique & Core Definition Drills",
        "Active Recall & Boundary Problem Solving",
        "Spaced Repetition & Comparative Analysis",
        "Timed Mock Problem Sets & Error Journaling",
        "Formula Derivation & Rapid Flashcard Drills"
    ]
    
    time_allocations = [
        {
            "topic": topic,
            "hours": allocated_per_topic,
            "technique": techniques[i % len(techniques)]
        }
        for i, topic in enumerate(topic_names)
    ]
    
    daily_plan = []
    days_to_plan = min(days_until_exam, 7)
    for day_i in range(1, days_to_plan + 1):
        assigned_topic = topic_names[(day_i - 1) % len(topic_names)]
        if day_i == days_to_plan:
            activity = f"Full Mock Assessment & comprehensive review of {assigned_topic} weak points."
        elif day_i % 2 == 1:
            activity = f"Deep-dive conceptual theory on {assigned_topic}, followed by 5 practice problems."
        else:
            activity = f"Self-quizzing on {assigned_topic}, error analysis, and formula memorization."
            
        daily_plan.append({
            "day": day_i,
            "focus": assigned_topic,
            "activities": activity
        })
        
    return {
        "strategy_summary": f"Targeted {days_until_exam}-day accelerated study roadmap. With {hours_per_day} hours/day ({total_hours} total study hours), focus primarily on foundational topics before progressing into complex scenario-based problem solving.",
        "topic_order": topic_names,
        "time_allocation": time_allocations,
        "daily_plan": daily_plan,
        "revision_tips": [
            "Use the Pomodoro Technique: 50 minutes high-focus study followed by a 10-minute active mental break.",
            "Maintain an Error Logbook: Document every mistaken question and write down the exact underlying misconception.",
            "Dedicate the final 48 hours purely to high-yield summary review and timed mock tests without cramming new material.",
            "Prioritize active retrieval (self-testing) over passive reading; testing yourself produces 3x better retention."
        ],
        "motivation": "Consistency is your greatest advantage. Dedicating focused blocks each day compounds into effortless mastery by exam day!"
    }
