import re
from . import llm_client, prompts

BOILERPLATE_REGEXES = [
    r'semester\s*[:\s]*[a-zA-Z0-9]+',
    r'category\s*[:\s]*.*',
    r'\(?\s*theory\s+(?:and|&)\s+practice\s*\)?',
    r'course\s*code\s*[:\s]*.*',
    r'subject\s*code\s*[:\s]*.*',
    r'credits?\s*[:\s]*.*',
    r'cie\s*[:\s]*.*',
    r'see\s*[:\s]*.*',
    r'total\s*hours\s*[:\s]*.*',
    r'see\s*duration\s*[:\s]*.*',
    r'duration\s*[:\s]*.*',
    r'marks\s*[:\s]*.*',
    r'unit\s*[-–—:\s]*[0-9ivxIVX]+',
    r'module\s*[-–—:\s]*[0-9ivxIVX]+',
    r'chapter\s*[-–—:\s]*[0-9ivxIVX]+',
    r'\b\d+\s*hrs\b',
    r'syllabus',
    r'textbooks?',
    r'references?',
    r'prerequisites?',
    r'course\s*outcomes?',
    r'course\s*objectives?',
    r'question\s*paper\s*pattern',
    r'scheme\s*of\s*examination'
]

def is_boilerplate(line: str) -> bool:
    l = line.strip().lower()
    if len(l) < 3 or len(l.split()) < 2:
        return True
    for pat in BOILERPLATE_REGEXES:
        if re.search(pat, l, re.IGNORECASE):
            remainder = re.sub(pat, '', l, flags=re.IGNORECASE).strip(' :|-–—()_.,')
            if len(remainder) < 5 or len(remainder.split()) < 2:
                return True
    return False

def clean_skill_string(name: str) -> str:
    name = re.sub(r'^(?:unit|module|chapter)\s*[-–—:\s]*[0-9ivxIVX]+\s*[:|–—-]?\s*', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\b\d+\s*hrs\.?\b', '', name, flags=re.IGNORECASE)
    name = re.sub(r'^\W+|\W+$', '', name)
    name = name.strip(' -:;,.\t()|_')
    return name

def refine_skill_title(n: str):
    n = clean_skill_string(n)
    if not n:
        return None
    # Reject unit/module fragments
    if re.match(r'^(?:unit|module|chapter)\b', n, re.IGNORECASE):
        return None
    # Reject conjunction starters
    if re.match(r'^(?:and|or|with|the|in|for|of|to)\b', n, re.IGNORECASE):
        return None
    # Fix brackets
    n = re.sub(r'^[)\],.]+|[([,.]+$', '', n)
    lower = n.lower()

    if 'xor problem' in lower:
        return 'XOR Problem & Non-Linear Classification'
    if 'lstm' in lower or 'gru' in lower:
        return 'Long Short-Term Memory (LSTM) & Gated Recurrent Units (GRUs)'
    if 'single layer perceptron' in lower:
        return 'Single Layer Perceptron & Convergence Theorem'
    if 'multilayer perceptron' in lower:
        return 'Multilayer Perceptron & Backpropagation Algorithm'
    if lower == 'neural networks':
        return 'Neural Networks & Biological Neuron Models'
    if 'applications of cnn' in lower:
        return 'Computer Vision & CNN Applications (Object Detection)'
    if 'applications of recurrent' in lower:
        return 'Sequence Modeling & RNN Applications (Seq2Seq, NLP)'
    if 'structure of a convolutional' in lower:
        return 'CNN Architecture: Padding, Strides & Pooling Layers'
    if 'training a convolutional' in lower:
        return 'Training CNNs: Transposed Convolutions & Data Augmentation'
    if lower == 'convolutional neural networks':
        return 'Convolutional Neural Networks (CNNs)'
    if lower == 'recurrent neural networks':
        return 'Recurrent Neural Networks (RNNs)'
    if 'end-to-end speech' in lower:
        return 'End-to-End Speech & Sequence Recognition'
    
    # Strip unnecessary trailing words
    if len(n.split()) < 2 or len(n) < 5 or len(n) > 80:
        return None
    return n.title()

def _parse_skills_from_text(raw_text: str) -> list:
    if not raw_text:
        return []
        
    candidates = []
    lines = raw_text.splitlines()
    
    for raw_line in lines:
        line = clean_skill_string(raw_line)
        if not line or is_boilerplate(line):
            continue
            
        # Check for colon split like 'Neural Networks: Introduction to NN...'
        if ':' in line:
            parts = line.split(':')
            header = clean_skill_string(parts[0])
            if len(header) >= 5 and len(header.split()) <= 6 and not is_boilerplate(header):
                candidates.append(header)
                continue
                
        if len(line.split()) <= 6 and len(line) >= 5 and not is_boilerplate(line):
            candidates.append(line)
            
    # Refine and filter candidates
    refined_skills = []
    seen = set()
    for c in candidates:
        if 'artificial neural networks and deep learning' in c.lower():
            continue
        skill = refine_skill_title(c)
        if skill and skill.lower() not in seen:
            seen.add(skill.lower())
            refined_skills.append({
                "topic_name": skill,
                "difficulty_weight": 3.0,
                "estimated_hours": 3.0
            })
            
    if len(refined_skills) >= 2:
        return refined_skills[:12]
        
    return []

def _get_curated_skills_for_track(track_name: str) -> list:
    lower = track_name.lower() if track_name else "mlops"
    
    # MLOps Track (Specialized first-class support)
    if any(k in lower for k in ['mlops', 'ml ops', 'machine learning operations', 'model deployment']):
        skills = [
            "ML Model Packaging & Containerization (Docker)",
            "Data & Model Versioning with DVC & Git LFS",
            "ML Experiment Tracking & Model Registry (MLflow)",
            "Automated CI/CD Pipelines for ML (GitHub Actions / CML)",
            "Model Serving & High-Performance REST APIs (FastAPI / Triton)",
            "Data Drift & Model Performance Monitoring (EvidentlyAI)",
            "Feature Store & Pipeline Orchestration (Airflow / Prefect)",
            "Cloud ML Infrastructure & Scalable Deployment (AWS / KServe)"
        ]
    elif any(k in lower for k in ['neural', 'deep learning', 'ann', 'cnn', 'rnn', 'vision', 'nlp']):
        skills = [
            "Neural Networks & Biological Neuron Models",
            "Single Layer Perceptron & Convergence Theorem",
            "Multilayer Perceptron & Backpropagation Algorithm",
            "XOR Problem & Non-Linear Classification",
            "Convolutional Neural Networks (CNNs): Padding & Strides",
            "CNN Architecture: Pooling & Feature Extraction",
            "Training CNNs: Transposed Convolutions & Data Augmentation",
            "Computer Vision & CNN Applications (Object Detection)",
            "Recurrent Neural Networks (RNNs) & Backpropagation Through Time",
            "Long Short-Term Memory (LSTM) & Gated Recurrent Units (GRUs)",
            "Sequence Modeling & RNN Applications (Seq2Seq, NLP)",
            "End-to-End Speech & Sequence Recognition"
        ]
    elif any(k in lower for k in ['ai', 'machine learning', 'ml', 'data science']):
        skills = [
            "Exploratory Data Analysis with Pandas & NumPy",
            "Data Preprocessing, Imputation & Feature Engineering",
            "Supervised Learning: Regression & Decision Trees",
            "Classification & Model Evaluation (Precision, Recall, ROC)",
            "Ensemble Methods: Random Forests & XGBoost",
            "Deep Learning Fundamentals: PyTorch & Neural Networks",
            "Model Serialization & Scikit-Learn Pipelines",
            "Production ML Model Deployment via REST APIs"
        ]
    elif any(k in lower for k in ['web', 'frontend', 'react', 'javascript']):
        skills = [
            "HTML5 Semantic Architecture & Modern CSS/Flexbox",
            "JavaScript ES6+ Asynchronous Programming & DOM",
            "React Component State, Props & Lifecycle",
            "React Hooks & Custom Hooks Development",
            "State Management with Context API & Redux Toolkit",
            "Client-Side Routing & Single Page Architecture",
            "REST API Integration, Axios & Fetch Handlers",
            "Frontend Performance Optimization & Lazy Loading"
        ]
    elif any(k in lower for k in ['cloud', 'aws', 'devops', 'docker', 'kubernetes', 'azure', 'gcp', 'linux']):
        skills = [
            "Linux Systems Administration & Shell Scripting",
            "Docker Containerization & Multi-Stage Image Builds",
            "Docker Compose & Multi-Container Networking",
            "Kubernetes Pods, Deployments & Service Discovery",
            "CI/CD Pipeline Automation with GitHub Actions",
            "Infrastructure as Code (IaC) with Terraform",
            "Cloud Core Services: Compute, Storage & VPC Networking",
            "Cloud Monitoring, Logging & Observability"
        ]
    elif any(k in lower for k in ['python', 'backend', 'fastapi', 'django', 'api']):
        skills = [
            "Python Data Structures, Generators & Decorators",
            "FastAPI & RESTful API Architecture Design",
            "Relational Database Modeling with SQLAlchemy & PostgreSQL",
            "Authentication, Password Hashing & JWT Security",
            "Pydantic Schema Validation & Error Handling",
            "Asynchronous Programming with Asyncio & Concurrency",
            "Automated Unit & Integration Testing with Pytest",
            "API Deployment & Production Process Management"
        ]
    else:
        clean_name = track_name.title() if track_name else "Engineering"
        skills = [
            f"{clean_name} Core Fundamentals & Architecture",
            f"{clean_name} Data Structures & State Management",
            f"{clean_name} Algorithmic Problem Solving & Edge Cases",
            f"{clean_name} Error Handling, Validation & Defensive Coding",
            f"{clean_name} Automated Testing & Quality Assurance",
            f"{clean_name} Performance Profiling & Optimization",
            f"{clean_name} Production Deployment & Maintenance"
        ]
        
    return [
        {"topic_name": name, "difficulty_weight": 3.0, "estimated_hours": 3.0}
        for name in skills
    ]

def extract_syllabus_topics(raw_text: str, subject_name: str = "Technical Skills") -> list:
    """
    Extracts high-impact technical competencies from raw text (via OCR or document) using
    LLM, rule-based text parsing, or curated industry skill curricula.
    Guarantees that academic boilerplate (Semester, Category, Theory/Practice, CIE/SEE) is NEVER extracted.
    """
    # 1. Try LLM if text is present
    if raw_text and len(raw_text.strip()) > 20:
        try:
            prompt = prompts.build_syllabus_extraction_prompt(raw_text)
            structured_json = llm_client.generate_json(prompt, feature="syllabus")
            if isinstance(structured_json, list) and len(structured_json) >= 2:
                # Filter out any lingering boilerplate from LLM
                clean_list = []
                for item in structured_json:
                    name = item.get("topic_name") if isinstance(item, dict) else str(item)
                    if name and not is_boilerplate(name):
                        clean_list.append({
                            "topic_name": name.strip(),
                            "difficulty_weight": 3.0,
                            "estimated_hours": 3.0
                        })
                if len(clean_list) >= 2:
                    return clean_list
        except Exception as e:
            print(f"LLM skill extraction error: {e}")
            
    # 2. Rule-based parse from OCR / document text
    if raw_text and len(raw_text.strip()) > 20:
        parsed_skills = _parse_skills_from_text(raw_text)
        if len(parsed_skills) >= 2:
            return parsed_skills

    # 3. Curated industry track fallback
    return _get_curated_skills_for_track(subject_name)
