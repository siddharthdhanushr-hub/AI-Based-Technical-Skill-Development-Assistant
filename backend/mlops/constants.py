"""
MLOps Constants, 21st-Century Skill Taxonomy & Phase 1/Phase 2 Benchmark Metadata
Derived from the AI-Based Technical Skill Development Assistant pipeline.
"""

from typing import Dict, List, Any

# All 17 technical disciplines from the Kaggle/Mendeley benchmark (N=8,528 students)
SKILL_COLUMNS: List[str] = [
    "database_fundamentals",
    "computer_architecture",
    "distributed_computing_systems",
    "cyber_security",
    "networking",
    "software_development",
    "programming_skills",
    "project_management",
    "computer_forensics_fundamentals",
    "technical_communication",
    "ai_ml",
    "software_engineering",
    "business_analysis",
    "communication_skills",
    "data_science",
    "troubleshooting_skills",
    "graphics_designing",
]

# The 10 Curated 21st-Century Relevant Technical Skills (Evaluator Directive Focus)
CENTURY_21_SKILLS: List[Dict[str, Any]] = [
    {
        "id": "ai_ml",
        "name": "AI & Machine Learning",
        "category": "Advanced Intelligence",
        "icon": "🤖",
        "description": "Generative AI, neural architectures, scikit-learn/PyTorch, predictive modeling, and LLM orchestration.",
        "benchmark_weight": 0.45
    },
    {
        "id": "data_science",
        "name": "Data Science & Big Data",
        "category": "Data Engineering",
        "icon": "📊",
        "description": "Data analytics, pandas/numpy manipulation, feature engineering, exploratory statistical analysis.",
        "benchmark_weight": 0.45
    },
    {
        "id": "software_development",
        "name": "Full-Stack Software Development",
        "category": "Software Engineering",
        "icon": "💻",
        "description": "RESTful API construction, asynchronous backends, modern frontend components, and state lifecycle.",
        "benchmark_weight": 0.40
    },
    {
        "id": "programming_skills",
        "name": "Core Coding & Algorithms",
        "category": "Foundations",
        "icon": "⚡",
        "description": "Data structures, algorithms, Big-O computational efficiency, and robust multi-paradigm programming.",
        "benchmark_weight": 0.35
    },
    {
        "id": "cyber_security",
        "name": "Cyber Security & DevSecOps",
        "category": "Security & Resilience",
        "icon": "🛡️",
        "description": "Vulnerability assessment, authentication, cryptography, zero-trust architecture, and cloud security.",
        "benchmark_weight": 0.50
    },
    {
        "id": "distributed_computing_systems",
        "name": "Cloud & Distributed Systems",
        "category": "Cloud Infrastructure",
        "icon": "☁️",
        "description": "Microservices, container orchestration, horizontal scalability, load balancing, and consensus protocols.",
        "benchmark_weight": 0.35
    },
    {
        "id": "database_fundamentals",
        "name": "Modern Database Systems",
        "category": "Data Engineering",
        "icon": "🗄️",
        "description": "Relational schema design, ACID transactions, SQL indexing, NoSQL document stores, vector querying.",
        "benchmark_weight": 0.18
    },
    {
        "id": "software_engineering",
        "name": "Architecture, Testing & CI/CD",
        "category": "Software Engineering",
        "icon": "⚙️",
        "description": "Design patterns, unit/integration testing (pytest), automated CI/CD pipelines, code quality gates.",
        "benchmark_weight": 0.25
    },
    {
        "id": "troubleshooting_skills",
        "name": "Observability & SRE Troubleshooting",
        "category": "Security & Resilience",
        "icon": "🔍",
        "description": "Root-cause diagnostics, production telemetry, distributed tracing, error handling, system resilience.",
        "benchmark_weight": 0.15
    },
    {
        "id": "technical_communication",
        "name": "Technical Communication & Agile",
        "category": "Foundations",
        "icon": "📋",
        "description": "Architecture documentation, agile sprint planning, code review critique, technical problem articulation.",
        "benchmark_weight": 0.35
    }
]

# The 7 Excluded Legacy Skills with Evaluator Justification
EXCLUDED_LEGACY_SKILLS: Dict[str, str] = {
    "computer_architecture": "Focuses on low-level microprocessor/silicon design; non-core for 21st-century software & cloud assessment screening.",
    "computer_forensics_fundamentals": "Traditional disk/file forensics; modern security engineering is unified under cyber_security.",
    "networking": "Legacy physical cabling and telecommunications; modern networking is handled under cloud distributed systems.",
    "project_management": "Traditional waterfall project management; modern software engineering uses agile technical communication.",
    "business_analysis": "Corporate non-technical business consulting; distinct from software engineering assessment screening.",
    "communication_skills": "General conversational speech; redundant with and replaced by engineering-tailored technical_communication.",
    "graphics_designing": "Visual arts and UI graphics; distinct from core computer science and software engineering proficiencies."
}

# Industry Tech Career Roles & Benchmark Requirements (0-6 scale)
ROLE_REQUIREMENTS: Dict[str, Dict[str, int]] = {
    "Software Developer": {
        "software_development": 6, "programming_skills": 5, "software_engineering": 5,
        "database_fundamentals": 3, "troubleshooting_skills": 3,
    },
    "AI ML Specialist": {
        "ai_ml": 5, "data_science": 5, "programming_skills": 4,
        "database_fundamentals": 3, "distributed_computing_systems": 3, "software_engineering": 3,
    },
    "Cyber Security Specialist": {
        "cyber_security": 6, "networking": 5, "computer_forensics_fundamentals": 4,
        "troubleshooting_skills": 4, "programming_skills": 3,
    },
    "Database Administrator": {
        "database_fundamentals": 6, "distributed_computing_systems": 4,
        "troubleshooting_skills": 4, "programming_skills": 3, "networking": 3,
    },
    "Application Support Engineer": {
        "distributed_computing_systems": 6, "troubleshooting_skills": 5,
        "software_development": 4, "database_fundamentals": 3,
    },
    "Software tester": {
        "software_engineering": 6, "troubleshooting_skills": 5,
        "programming_skills": 4, "software_development": 3,
    },
    "API Specialist": {
        "programming_skills": 6, "software_development": 5,
        "distributed_computing_systems": 4, "software_engineering": 4,
    },
    "Networking Engineer": {
        "networking": 6, "cyber_security": 4, "troubleshooting_skills": 4,
        "distributed_computing_systems": 4, "computer_architecture": 3,
    },
    "Technical Writer": {
        "technical_communication": 6, "communication_skills": 5, "software_engineering": 3,
    },
    "Project Manager": {
        "project_management": 6, "business_analysis": 5,
        "technical_communication": 5, "communication_skills": 5,
    }
}

ROLE_CLASSES: List[str] = list(ROLE_REQUIREMENTS.keys())

# Core Assessment Weights used in probability calculation (weights sum to 1.0)
CORE_ASSESSMENT_WEIGHTS: Dict[str, float] = {
    "programming_skills":       0.22,
    "database_fundamentals":    0.18,
    "software_development":     0.18,
    "troubleshooting_skills":   0.15,
    "software_engineering":     0.15,
    "networking":               0.12,
}

# Phase 1 Evaluation Benchmark Metrics (1,706 held-out test students)
PHASE1_METRICS = {
    "dataset": {
        "source": "CareerMap — Mendeley Data (DOI: 10.17632/5z68cvxssn.1)",
        "total_records": 8528,
        "train_records": 6822,
        "test_records": 1706,
        "features_count": 25,
        "task": "Binary Classification (Assessment Pass / Fail Screening Gate)"
    },
    "models": {
        "decision_tree": {
            "name": "Decision Tree Classifier",
            "hyperparams": "max_depth=5, min_samples_leaf=10",
            "accuracy": 72.04,
            "precision": 0.7238,
            "recall": 0.6344,
            "f1_score": 0.6762,
            "roc_auc": 0.7885
        },
        "random_forest": {
            "name": "Random Forest Classifier (Champion)",
            "hyperparams": "n_estimators=100, max_depth=7, min_samples_leaf=4, min_samples_split=8",
            "accuracy": 73.51,
            "precision": 0.7211,
            "recall": 0.6917,
            "f1_score": 0.7061,
            "roc_auc": 0.7949,
            "is_champion": True
        },
        "logistic_regression": {
            "name": "Logistic Regression (Baseline)",
            "hyperparams": "C=1.0, solver=lbfgs, max_iter=1000",
            "accuracy": 73.45,
            "precision": 0.7117,
            "recall": 0.7108,
            "f1_score": 0.7113,
            "roc_auc": 0.7974
        }
    },
    "confusion_matrix": {
        "true_negatives": 711,
        "false_positives": 210,
        "false_negatives": 242,
        "true_positives": 543
    },
    "per_class": {
        "fail": {"precision": 0.7461, "recall": 0.7720, "f1": 0.7588, "support": 921},
        "pass": {"precision": 0.7211, "recall": 0.6917, "f1": 0.7061, "support": 785}
    }
}

# Phase 2 Governance & MLOps Infrastructure Details
PHASE2_GOVERNANCE = {
    "version": "2.1.0",
    "mlops_stack": {
        "orchestration": "DVC 3.59 (Data Version Control) with dvc repro",
        "tracking": "MLflow 2.17.2 Experiment & Model Registry",
        "api_framework": "FastAPI 0.128.0 + Pydantic v2",
        "containerization": "Multi-stage Docker (python:3.11-slim, non-root appuser)",
        "ci_cd": "GitHub Actions (Ruff linting, model quality gates, 46/46 unit tests passing)"
    },
    "model_testing": [
        {"test": "Boundary Value Testing", "result": "PASSED (Zero-vector outputs 0, Max-vector outputs 1)"},
        {"test": "Directional Monotonicity", "result": "PASSED (Increasing skills monotonically increases pass prob)"},
        {"test": "Invariance Testing", "result": "PASSED (Perturbing non-core legacy skills retains pass outcome)"},
        {"test": "Inference Latency Benchmark", "result": "PASSED (< 12ms per prediction, benchmark < 50ms)"}
    ],
    "quality_auditor": {
        "uncertainty_window": "[0.45, 0.55]",
        "borderline_behavior": "Flags students needing targeted review",
        "schema_enforcement": "Pydantic bounds [0, 6] on all features"
    }
}

