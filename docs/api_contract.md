# API Contracts & Endpoint Specifications

This document defines the formal request and response schemas shared across Member 3 (Frontend), Member 4 (Backend Integration), and Members 1 & 2 (Data Pipelines & Modeling).

---

## Base URL
- Local Development: `http://localhost:8000/api`

---

## 1. Curriculum & Topics

### `GET /curriculum/subjects`
Returns the list of available courses and subjects.
- **Response `200 OK`**:
```json
[
  {
    "subject_id": "ml-101",
    "subject_name": "Machine Learning Fundamentals",
    "description": "Core concepts in supervised and unsupervised learning",
    "topics_count": 5
  }
]
```

### `GET /curriculum/topics/{subject_id}`
Returns topics for a given subject.
- **Response `200 OK`**:
```json
[
  {
    "topic_id": "topic-supervised-learning",
    "topic_name": "Supervised Learning Fundamentals",
    "subject_id": "ml-101",
    "description": "Classification, regression, labeled data principles",
    "difficulty": "Medium",
    "estimated_minutes": 25
  }
]
```

---

## 2. Topic Confidence Assessment

### `POST /assessment/confidence`
Submits a self-reported topic confidence score (0–100 scale).
- **Request Body**:
```json
{
  "student_id": "std_anon_001",
  "topic_id": "topic-supervised-learning",
  "confidence_score": 45.0,
  "notes": "Need to clarify loss functions"
}
```
- **Validation**:
  - `confidence_score`: float between 0.0 and 100.0 inclusive.
- **Response `201 Created`**:
```json
{
  "assessment_id": "conf_88a91b",
  "student_id": "std_anon_001",
  "topic_id": "topic-supervised-learning",
  "confidence_score": 45.0,
  "confidence_band": "Low",
  "needs_revision": true,
  "threshold_applied": 60.0,
  "timestamp": "2026-10-23T01:20:00Z"
}
```

---

## 3. Targeted Revision & Flashcards

### `GET /revision/{topic_id}`
Fetches curated revision content and flashcards for a specific topic.
- **Response `200 OK`**:
```json
{
  "topic_id": "topic-supervised-learning",
  "topic_name": "Supervised Learning Fundamentals",
  "summary": "Supervised learning algorithms model the relationship between input features and target labels...",
  "key_definitions": [
    {"term": "Features", "definition": "Individual measurable properties of the phenomenon being observed."},
    {"term": "Loss Function", "definition": "Mathematical function measuring discrepancy between predicted and true labels."}
  ],
  "common_misconceptions": [
    "High training accuracy does not guarantee generalizability (overfitting risk)."
  ],
  "flashcards": [
    {
      "card_id": "fc_01",
      "front": "What distinguishes regression from classification?",
      "back": "Regression predicts continuous numerical outputs; classification predicts discrete categorical classes."
    }
  ]
}
```

### `POST /revision/complete`
Logs completion of a revision session.
- **Request Body**:
```json
{
  "student_id": "std_anon_001",
  "topic_id": "topic-supervised-learning",
  "cards_reviewed_count": 5,
  "duration_seconds": 180
}
```
- **Response `200 OK`**:
```json
{
  "status": "recorded",
  "event_id": "ev_rev_771b"
}
```

---

## 4. Topic Quiz Engine

### `POST /quiz/start`
Initializes a new quiz attempt for a topic.
- **Request Body**:
```json
{
  "student_id": "std_anon_001",
  "topic_id": "topic-supervised-learning",
  "question_count": 5
}
```
- **Response `200 OK`**:
```json
{
  "attempt_id": "att_99182a",
  "topic_id": "topic-supervised-learning",
  "questions": [
    {
      "question_id": "q_sl_01",
      "text": "Which metric is appropriate for evaluating an imbalanced binary classification dataset?",
      "options": ["A. Accuracy", "B. ROC-AUC / F1-Score", "C. Mean Absolute Error", "D. R-squared"],
      "difficulty": "Medium"
    }
  ]
}
```

### `POST /quiz/submit`
Submits student answers and computes validated score and readiness.
- **Request Body**:
```json
{
  "attempt_id": "att_99182a",
  "student_id": "std_anon_001",
  "topic_id": "topic-supervised-learning",
  "answers": [
    {
      "question_id": "q_sl_01",
      "selected_option": "B",
      "response_time_seconds": 22.5
    }
  ]
}
```
- **Response `200 OK`**:
```json
{
  "attempt_id": "att_99182a",
  "topic_id": "topic-supervised-learning",
  "score_percentage": 80.0,
  "total_questions": 5,
  "correct_count": 4,
  "detailed_feedback": [
    {
      "question_id": "q_sl_01",
      "selected_option": "B",
      "correct_option": "B",
      "is_correct": true,
      "explanation": "ROC-AUC and F1-score account for false positives and false negatives, making them robust to class imbalance."
    }
  ],
  "readiness_status": "Nearly Ready",
  "recommended_action": "Review incorrect questions and proceed to next module"
}
```

---

## 5. Topic Grip & Readiness

### `GET /readiness/{student_id}/{topic_id}`
Fetches the synthesized readiness status combining self-reported confidence and demonstrated quiz performance.
- **Response `200 OK`**:
```json
{
  "student_id": "std_anon_001",
  "topic_id": "topic-supervised-learning",
  "confidence_score": 45.0,
  "confidence_band": "Low",
  "latest_quiz_score": 80.0,
  "best_quiz_score": 80.0,
  "attempts_count": 1,
  "revision_completed": true,
  "readiness_status": "Developing",
  "recommended_next_action": "Retake quiz after 24h to consolidate retention"
}
```
