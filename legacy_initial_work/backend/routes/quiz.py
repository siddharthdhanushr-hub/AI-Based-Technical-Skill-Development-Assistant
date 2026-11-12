import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models import QuizAttempt, QuestionResponse, TelemetryEvent
from backend.schemas import (
    QuizStartIn,
    QuizStartOut,
    QuestionOut,
    QuizSubmitIn,
    QuizSubmitOut,
    QuestionFeedbackItem
)
from backend.curriculum_data import QUESTIONS

router = APIRouter(prefix="/quiz", tags=["Quiz"])


@router.post("/start", response_model=QuizStartOut)
def start_quiz(payload: QuizStartIn, db: Session = Depends(get_db)):
    topic_questions = QUESTIONS.get(payload.topic_id)
    if not topic_questions:
        raise HTTPException(status_code=404, detail=f"No questions registered for topic '{payload.topic_id}'")

    attempt_id = f"att_{uuid.uuid4().hex[:12]}"
    now = datetime.utcnow()

    # Log quiz_started event
    telem = TelemetryEvent(
        event_id=f"ev_{uuid.uuid4().hex[:12]}",
        timestamp=now,
        student_id=payload.student_id,
        topic_id=payload.topic_id,
        attempt_id=attempt_id,
        event_type="quiz_started",
        is_synthetic=False
    )
    db.add(telem)
    db.commit()

    # Strip correct_option and explanation for client response
    safe_questions = [
        QuestionOut(
            question_id=q["question_id"],
            text=q["text"],
            options=q["options"]
        )
        for q in topic_questions
    ]

    return QuizStartOut(
        attempt_id=attempt_id,
        topic_id=payload.topic_id,
        questions=safe_questions
    )


@router.post("/submit", response_model=QuizSubmitOut, status_code=status.HTTP_200_OK)
def submit_quiz(payload: QuizSubmitIn, db: Session = Depends(get_db)):
    topic_questions = QUESTIONS.get(payload.topic_id)
    if not topic_questions:
        raise HTTPException(status_code=404, detail=f"Topic '{payload.topic_id}' not found")

    q_map = {q["question_id"]: q for q in topic_questions}
    submitted_answers = {a.question_id: a for a in payload.answers}

    correct_count = 0
    feedback_items = []
    now = datetime.utcnow()

    # Evaluate each question
    for q_id, q_data in q_map.items():
        ans_item = submitted_answers.get(q_id)
        selected = ans_item.selected_option if ans_item else None
        resp_time = ans_item.response_time_seconds if ans_item else 0.0

        is_correct = (selected == q_data["correct_option"])
        if is_correct:
            correct_count += 1

        feedback_items.append(
            QuestionFeedbackItem(
                question_id=q_id,
                selected_option=selected,
                correct_option=q_data["correct_option"],
                is_correct=is_correct,
                explanation=q_data["explanation"]
            )
        )

        # Log individual question answered in telemetry
        telem_q = TelemetryEvent(
            event_id=f"ev_{uuid.uuid4().hex[:12]}",
            timestamp=now,
            student_id=payload.student_id,
            topic_id=payload.topic_id,
            attempt_id=payload.attempt_id,
            question_id=q_id,
            event_type="question_answered",
            selected_option=selected,
            is_correct=is_correct,
            response_time_seconds=resp_time,
            is_synthetic=False
        )
        db.add(telem_q)

    total_q = len(topic_questions)
    score_percentage = round((correct_count / float(total_q)) * 100.0, 1)

    # Determine readiness band
    if score_percentage >= 80.0:
        readiness_status = "Demonstrated Mastery"
        recommendation = "Demonstrated strong grasp! Proceed to the next technical module."
    elif score_percentage >= 60.0:
        readiness_status = "Developing"
        recommendation = "Developing competence. Review explanations and take a second practice attempt."
    else:
        readiness_status = "Needs Revision"
        recommendation = "Foundational gaps detected. Complete flashcards and review concept summaries before retesting."

    # Persist attempt record
    attempt_record = QuizAttempt(
        attempt_id=payload.attempt_id,
        student_id=payload.student_id,
        topic_id=payload.topic_id,
        score_percentage=score_percentage,
        total_questions=total_q,
        correct_count=correct_count,
        readiness_status=readiness_status,
        recommended_action=recommendation,
        created_at=now
    )
    db.add(attempt_record)

    # Persist question responses
    for fb in feedback_items:
        ans_item = submitted_answers.get(fb.question_id)
        resp_time = ans_item.response_time_seconds if ans_item else 0.0
        q_resp = QuestionResponse(
            attempt_id=payload.attempt_id,
            question_id=fb.question_id,
            selected_option=fb.selected_option,
            correct_option=fb.correct_option,
            is_correct=fb.is_correct,
            response_time_seconds=resp_time
        )
        db.add(q_resp)

    # Log quiz_submitted and quiz_result_calculated in telemetry
    db.add(TelemetryEvent(
        event_id=f"ev_{uuid.uuid4().hex[:12]}",
        timestamp=now,
        student_id=payload.student_id,
        topic_id=payload.topic_id,
        attempt_id=payload.attempt_id,
        event_type="quiz_submitted",
        quiz_score=score_percentage,
        is_synthetic=False
    ))

    db.add(TelemetryEvent(
        event_id=f"ev_{uuid.uuid4().hex[:12]}",
        timestamp=now,
        student_id=payload.student_id,
        topic_id=payload.topic_id,
        attempt_id=payload.attempt_id,
        event_type="quiz_result_calculated",
        quiz_score=score_percentage,
        readiness_status=readiness_status,
        is_synthetic=False
    ))

    db.commit()

    return QuizSubmitOut(
        attempt_id=payload.attempt_id,
        topic_id=payload.topic_id,
        score_percentage=score_percentage,
        total_questions=total_q,
        correct_count=correct_count,
        detailed_feedback=feedback_items,
        readiness_status=readiness_status,
        recommended_action=recommendation
    )
