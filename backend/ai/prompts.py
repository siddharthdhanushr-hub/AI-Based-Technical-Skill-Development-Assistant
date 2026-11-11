def build_syllabus_extraction_prompt(raw_text: str) -> str:
    return f"""
    You are an expert AI technical skills curriculum architect.
    Extract the core practical, technical engineering skills and competencies from the provided document/OCR text.

    STRICT NEGATIVE RULES - NEVER EXTRACT THE FOLLOWING:
    - Academic administrative metadata (e.g. "Semester: V", "Sem 5", "Category: Professional Core Course", "Course Code: AI2Z531A", "CIE", "SEE Marks", "Credits", "Hours", "Duration").
    - Generic format labels (e.g. "(Theory and Practice)", "Theory", "Lab", "Practical", "Lecture").
    - Unit or Module numbers (e.g. "Unit-I", "Unit - 11", "Module 1", "Chapter 2").
    - Boilerplate sections (e.g. "Course Objectives", "Course Outcomes", "Textbooks", "References", "Syllabus").

    WHAT TO EXTRACT:
    - Real, specific technical concepts, algorithms, frameworks, and engineering competencies.
    - If the document is about Neural Networks / Deep Learning, extract the concrete skills (e.g., "Single Layer Perceptrons & Convergence Theorem", "Multilayer Perceptrons & Backpropagation", "Convolutional Neural Networks (CNNs)", "Recurrent Neural Networks (RNNs)", "LSTM & Gated Recurrent Units (GRUs)", "Object Detection & Computer Vision").
    - Return between 6 and 10 high-value technical competencies.

    Return the response STRICTLY as a JSON array of skill objects:
    [
      {{"topic_name": "Specific Technical Skill", "difficulty_weight": 3.0, "estimated_hours": 3.0}}
    ]

    Raw Text:
    {raw_text}
    """
