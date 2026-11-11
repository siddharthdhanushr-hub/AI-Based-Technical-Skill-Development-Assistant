from . import llm_client

def generate_project_ideas(track_name: str, skill_names: list = None) -> list:
    """
    Generates industry-relevant, portfolio-ready hands-on project ideas for technical skill development.
    """
    skills_context = ", ".join(skill_names) if skill_names else track_name
    prompt = f"""
    You are a principal technical hiring manager and tech lead.
    Generate 3 real-world portfolio project ideas for someone developing skills in: "{track_name}".
    Key skills: {skills_context}
    
    Rules:
    - Project 1: Beginner / Foundational (Clear focus, immediate practical utility)
    - Project 2: Intermediate (Full-stack or multi-component integration)
    - Project 3: Production-Grade / Senior (Scalability, cloud deployment, telemetry, architectural trade-offs)
    
    Return STRICTLY as a JSON array:
    [
      {{
        "title": "Project Name",
        "level": "Junior Developer / Beginner",
        "tech_stack": "e.g., Python, FastAPI, SQLite, Docker",
        "description": "Comprehensive summary of what the project does and its purpose.",
        "key_deliverables": ["Deliverable 1", "Deliverable 2", "Deliverable 3"],
        "portfolio_impact": "How this showcases technical competence on a resume or GitHub profile."
      }}
    ]
    """
    try:
        result = llm_client.generate_json(prompt, feature="general")
        if isinstance(result, list) and len(result) >= 3:
            return result[:3]
    except Exception as e:
        print(f"LLM project generation error: {e}")

    # High quality domain fallbacks tailored to the track
    clean_track = track_name.title() if track_name else "Technical Engineering"
    lower = track_name.lower() if track_name else ""

    if any(k in lower for k in ['web', 'frontend', 'react', 'javascript']):
        return [
            {
                "title": "Interactive Developer Analytics & Code Snippet Vault",
                "level": "Junior Developer / Beginner",
                "tech_stack": "React 19, JavaScript ES6+, CSS Flexbox/Grid, LocalStorage API",
                "description": "A single-page application for developers to catalog syntax snippets, tag them by language, search instantly, and test snippets with live preview formatting.",
                "key_deliverables": [
                    "Dynamic component state management with customized React hooks",
                    "Instant debounced keyword and category filtering",
                    "Dark/Light theme toggle with persistent user preferences",
                    "Responsive mobile-first layout with zero UI framework dependencies"
                ],
                "portfolio_impact": "Demonstrates mastery of core React lifecycles, DOM manipulation, responsive CSS, and state management."
            },
            {
                "title": "Real-Time Collaborative Kanban Board & Task Tracker",
                "level": "Mid-Level Professional",
                "tech_stack": "React, TypeScript, Redux Toolkit, WebSockets / REST API, Tailwind CSS",
                "description": "An interactive project management dashboard featuring drag-and-drop columns, optimistic UI updates, user assignment, and activity audit timelines.",
                "key_deliverables": [
                    "Drag-and-drop interface with reorderable task queues",
                    "Global state orchestration with Redux Toolkit and normalized state shapes",
                    "Robust client-side input validation and error boundary fallbacks",
                    "Modular REST API integration with Axios interceptors"
                ],
                "portfolio_impact": "Proves ability to construct complex, highly interactive SPAs with scalable state management and clean component architecture."
            },
            {
                "title": "Enterprise Cloud Telemetry Dashboard & Performance Profiler",
                "level": "Senior / Production Grade",
                "tech_stack": "Next.js / React, TypeScript, Chart.js / D3, Redis Caching, Docker",
                "description": "A mission-critical observability portal that visualizes live microservice throughput, latency percentiles (p95/p99), and system resource graphs.",
                "key_deliverables": [
                    "High-frequency time-series data visualization with canvas/SVG rendering",
                    "Code-splitting, route-based lazy loading, and bundle size minimization",
                    "Comprehensive automated test coverage using Vitest and React Testing Library",
                    "Containerized multi-stage Docker build ready for Kubernetes deployment"
                ],
                "portfolio_impact": "Exemplifies senior-level frontend engineering, performance optimization, data visualization, and cloud-native practices."
            }
        ]
    elif any(k in lower for k in ['ai', 'machine learning', 'ml', 'data']):
        return [
            {
                "title": "Automated Customer Sentiment & Feedback Classifier",
                "level": "Junior Developer / Beginner",
                "tech_stack": "Python 3.11, Pandas, Scikit-Learn, Streamlit, NLTK",
                "description": "An end-to-end NLP tool that ingests text reviews, performs tokenization and TF-IDF vectorization, and predicts sentiment category with confidence scores.",
                "key_deliverables": [
                    "Data preprocessing pipeline with outlier removal and lemmatization",
                    "Logistic Regression & Naive Bayes comparative benchmarking",
                    "Interactive Streamlit user interface with live prediction visualizer",
                    "Comprehensive evaluation metrics (Confusion Matrix, Precision/Recall/F1)"
                ],
                "portfolio_impact": "Validates foundational data wrangling, model training, and accessible prototype presentation."
            },
            {
                "title": "Predictive Churn Forecasting Engine with Explainable AI",
                "level": "Mid-Level Professional",
                "tech_stack": "Python, XGBoost, Scikit-Learn, FastAPI, SHAP, Docker",
                "description": "A production-oriented machine learning service that predicts customer churn risk from behavioral metrics, outputting feature importance and SHAP explainability values.",
                "key_deliverables": [
                    "Feature engineering pipeline handling categorical encoding and scaling",
                    "Hyperparameter tuning using Bayesian search cross-validation",
                    "FastAPI inference microservice with automated Pydantic schema validation",
                    "Model explainability visualizations explaining 'why' predictions were made"
                ],
                "portfolio_impact": "Shows technical recruiters you understand practical, production-level ML with API deployment and model explainability."
            },
            {
                "title": "Real-Time Feature Store & Continuous Model Retraining Pipeline",
                "level": "Senior / Production Grade",
                "tech_stack": "Python, MLflow, Docker, PostgreSQL, Prometheus, GitHub Actions CI/CD",
                "description": "An enterprise MLOps platform featuring model versioning, automated drift detection, data validation gates, and automated deployment canary testing.",
                "key_deliverables": [
                    "Automated MLflow tracking server for experiment metrics and artifact registry",
                    "Data drift detection alerting when production distribution shifts",
                    "Automated CI/CD pipeline triggering automated regression tests on push",
                    "Production Prometheus metrics exposing model latency and prediction distribution"
                ],
                "portfolio_impact": "Highlights enterprise MLOps capability, systems engineering, CI/CD automation, and reliable ML deployment."
            }
        ]
    else:
        # Generalized high-impact technical portfolio projects
        return [
            {
                "title": f"{clean_track} Automated Diagnostic CLI & Developer Utility",
                "level": "Junior Developer / Beginner",
                "tech_stack": "Python / Node.js, Shell Scripting, SQLite, GitHub",
                "description": f"A dedicated command-line developer utility that inspects, validates, and reports on core operational health within the {clean_track} domain.",
                "key_deliverables": [
                    "Command-line argument parser with automated help documentation",
                    "Structured data validation and defensive error boundary handling",
                    "Formatted terminal reports with color-coded status output",
                    "Automated unit testing with 90%+ branch coverage"
                ],
                "portfolio_impact": "Demonstrates strong foundational code hygiene, CLI tool design, and automated test-driven development."
            },
            {
                "title": f"{clean_track} Enterprise REST API Microservice & Ingestion Engine",
                "level": "Mid-Level Professional",
                "tech_stack": "FastAPI / Express, SQLAlchemy / Prisma, PostgreSQL, Docker, JWT",
                "description": f"A scalable, production-grade backend service powering data workflows, state mutations, and secure operations for {clean_track}.",
                "key_deliverables": [
                    "Strict RESTful API contract specifications with Swagger / OpenAPI docs",
                    "Role-based access control (RBAC) and JWT security tokens",
                    "Relational schema indexing with migration history tracking",
                    "Containerized Docker setup with multi-environment configuration"
                ],
                "portfolio_impact": "Proves ability to build resilient, secure, and production-ready microservices adhering to modern standards."
            },
            {
                "title": f"{clean_track} High-Throughput Event-Driven Architecture with Cloud Deployment",
                "level": "Senior / Production Grade",
                "tech_stack": "Docker, Kubernetes, Redis / Kafka, Cloud VPC, CI/CD Pipeline",
                "description": f"A distributed, highly available technical system designed to process asynchronous event streams, cache high-frequency states, and auto-scale under load.",
                "key_deliverables": [
                    "Asynchronous background worker queues with exponential backoff retries",
                    "In-memory Redis caching with cache-invalidation strategies",
                    "End-to-end CI/CD workflow testing, container building, and deployment",
                    "Healthcheck endpoints, distributed tracing, and Prometheus metrics"
                ],
                "portfolio_impact": "Exemplifies senior-level systems design, scalability considerations, observability, and cloud engineering."
            }
        ]

