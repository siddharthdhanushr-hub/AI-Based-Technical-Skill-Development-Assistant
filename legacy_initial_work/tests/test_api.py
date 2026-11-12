"""
Backend API Integration Tests
Author: Member 4 (Siddharth Dhanush R - Project Lead)
Role: Backend Integration, Persistence, MLOps and Reproducibility
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"


def test_curriculum_endpoints():
    # Subjects
    res_sub = client.get("/api/curriculum/subjects")
    assert res_sub.status_code == 200
    subjects = res_sub.json()
    assert len(subjects) >= 2
    assert any(s["subject_id"] == "sub_ml_core" for s in subjects)

    # Topics for valid subject
    res_top = client.get("/api/curriculum/topics/sub_ml_core")
    assert res_top.status_code == 200
    topics = res_top.json()
    assert len(topics) >= 4

    # Non-existent subject
    res_err = client.get("/api/curriculum/topics/non_existent_subject")
    assert res_err.status_code == 404


def test_confidence_assessment_flow():
    # Submit valid confidence < 60 (Weak topic)
    payload = {
        "student_id": "std_test_lead_01",
        "topic_id": "topic_superv_01",
        "confidence_score": 45.0,
        "notes": "Need to clarify loss functions"
    }
    res = client.post("/api/assessment/confidence", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["confidence_band"] == "Low"
    assert data["needs_revision"] is True
    assert data["assessment_id"].startswith("conf_")

    # Rejection of invalid confidence score
    res_invalid = client.post("/api/assessment/confidence", json={
        "student_id": "std_test_lead_01",
        "topic_id": "topic_superv_01",
        "confidence_score": 125.0
    })
    assert res_invalid.status_code in {400, 422}


def test_revision_and_completion_flow():
    # Get revision material
    res_rev = client.get("/api/revision/topic_superv_01")
    assert res_rev.status_code == 200
    rev_data = res_rev.json()
    assert len(rev_data["flashcards"]) >= 2
    assert len(rev_data["key_definitions"]) >= 2

    # Complete revision
    comp_res = client.post("/api/revision/complete", json={
        "student_id": "std_test_lead_01",
        "topic_id": "topic_superv_01",
        "cards_reviewed_count": 3,
        "duration_seconds": 150.0
    })
    assert comp_res.status_code == 201
    assert comp_res.json()["status"] == "recorded"


def test_quiz_lifecycle_and_scoring():
    # Start quiz
    start_res = client.post("/api/quiz/start", json={
        "student_id": "std_test_lead_01",
        "topic_id": "topic_superv_01"
    })
    assert start_res.status_code == 200
    quiz_data = start_res.json()
    attempt_id = quiz_data["attempt_id"]
    questions = quiz_data["questions"]
    assert len(questions) >= 2

    # Verify answers are NOT exposed in start response
    for q in questions:
        assert "correct_option" not in q
        assert "explanation" not in q

    # Submit quiz answers (answer option A for all)
    submit_payload = {
        "attempt_id": attempt_id,
        "student_id": "std_test_lead_01",
        "topic_id": "topic_superv_01",
        "answers": [
            {
                "question_id": q["question_id"],
                "selected_option": "A",
                "response_time_seconds": 18.0
            }
            for q in questions
        ]
    }

    submit_res = client.post("/api/quiz/submit", json=submit_payload)
    assert submit_res.status_code == 200
    sub_data = submit_res.json()
    assert "score_percentage" in sub_data
    assert "readiness_status" in sub_data
    assert "detailed_feedback" in sub_data
    assert len(sub_data["detailed_feedback"]) == len(questions)


def test_readiness_and_progress_endpoints():
    # Topic readiness
    read_res = client.get("/api/readiness/std_test_lead_01/topic_superv_01")
    assert read_res.status_code == 200
    r_data = read_res.json()
    assert r_data["confidence_score"] == 45.0
    assert r_data["attempts_count"] >= 1
    assert r_data["revision_completed"] is True

    # Progress summary
    prog_res = client.get("/api/readiness/progress/std_test_lead_01")
    assert prog_res.status_code == 200
    p_data = prog_res.json()
    assert p_data["topics_assessed"] >= 1
    assert p_data["quizzes_taken"] >= 1
    assert len(p_data["topic_readiness_breakdown"]) >= 5


def test_telemetry_event_ingestion_and_export():
    import uuid
    dynamic_event_id = f"ev_test_int_{uuid.uuid4().hex[:8]}"
    telem_payload = {
        "event_id": dynamic_event_id,
        "timestamp": "2026-10-23T02:00:00Z",
        "student_id": "std_test_lead_01",
        "topic_id": "topic_bias_var_02",
        "event_type": "topic_selected",
        "is_synthetic": False
    }
    res = client.post("/api/telemetry/event", json=telem_payload)
    assert res.status_code == 201

    # Verify retrieval
    res_list = client.get("/api/telemetry/events/std_test_lead_01")
    assert res_list.status_code == 200
    assert any(e["event_id"] == dynamic_event_id for e in res_list.json())


def test_model_inference_endpoint():
    pred_payload = {
        "student_id": "std_test_lead_01",
        "topic_id": "topic_superv_01",
        "confidence_score": 82.0,
        "completed_revision": True,
        "revision_duration_seconds": 180.0,
        "prior_topic_attempts": 1,
        "prior_topic_avg_score": 80.0
    }
    res = client.post("/api/models/predict-mastery", json=pred_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["predicted_band"] in ["Needs Revision", "Developing", "Demonstrated Mastery"]
    assert "class_probabilities" in data
    assert "model_source" in data
