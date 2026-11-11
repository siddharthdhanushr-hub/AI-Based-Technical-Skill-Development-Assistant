"""
Synthetic Bootstrap Dataset Generator
Author: Member 1 (Shreyas)
Role: Data Acquisition, Data Quality, Schema Validation, and EDA

Generates a documented, reproducible synthetic dataset of student learning telemetry events.
This bootstrap dataset resolves the Phase 1 cold-start problem before real students
interact with the live website.

CRITICAL ETHICAL & SCIENTIFIC CAVEATS:
1. This dataset is SYNTHETIC and marked with `is_synthetic = True` on every row.
2. It must NOT be represented as empirical observations from human learners.
3. Model evaluation metrics derived from this data validate pipeline reproducibility,
   not real-world pedagogical efficacy.
"""

import os
import random
import uuid
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Fixed seed for strict mathematical reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

TOPICS = [
    {"topic_id": "topic_superv_01", "name": "Supervised Learning & Loss Functions", "difficulty": 0.45},
    {"topic_id": "topic_bias_var_02", "name": "Bias-Variance Tradeoff", "difficulty": 0.50},
    {"topic_id": "topic_eval_metrics_03", "name": "Classification Metrics & Imbalance", "difficulty": 0.65},
    {"topic_id": "topic_tree_ensembles_04", "name": "Decision Trees & Ensembles", "difficulty": 0.55},
    {"topic_id": "topic_dvc_version_01", "name": "Data & Pipeline Versioning (DVC)", "difficulty": 0.50},
    {"topic_id": "topic_mlflow_track_02", "name": "Experiment Tracking (MLflow)", "difficulty": 0.52},
]


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + np.exp(-x))


def generate_bootstrap_events(num_students: int = 50) -> pd.DataFrame:
    """
    Simulates learning sessions across students and topics with stochastic realism.
    """
    events = []
    base_time = datetime(2026, 10, 1, 9, 0, 0)

    for i in range(1, num_students + 1):
        student_id = f"std_sim_{i:03d}"
        # Latent underlying aptitude of the student (unobserved in real life)
        student_aptitude = float(np.clip(np.random.normal(0.55, 0.18), 0.15, 0.95))
        # Self-assessment calibration bias (positive = overconfident, negative = modest/underconfident)
        calibration_bias = float(np.random.normal(0.0, 0.12))

        # Each student explores 2 to 5 topics
        topics_selected = random.sample(TOPICS, k=random.randint(2, min(5, len(TOPICS))))

        for topic in topics_selected:
            session_time = base_time + timedelta(
                days=random.randint(0, 14),
                hours=random.randint(0, 12),
                minutes=random.randint(0, 59)
            )

            topic_id = topic["topic_id"]
            topic_difficulty = topic["difficulty"]

            # Event 1: Topic Selected
            events.append({
                "event_id": f"ev_{uuid.uuid4().hex[:12]}",
                "timestamp": session_time.isoformat() + "Z",
                "student_id": student_id,
                "topic_id": topic_id,
                "event_type": "topic_selected",
                "attempt_id": None,
                "question_id": None,
                "confidence_score": None,
                "selected_option": None,
                "is_correct": None,
                "response_time_seconds": None,
                "quiz_score": None,
                "revision_status": None,
                "readiness_status": None,
                "is_synthetic": True
            })

            # Event 2: Self-Reported Confidence (0 to 100)
            # Confidence is derived from aptitude + calibration bias + random noise
            raw_conf = (student_aptitude + calibration_bias) * 100.0 + random.uniform(-10.0, 10.0)
            confidence_score = float(np.clip(round(raw_conf, 1), 5.0, 98.0))

            session_time += timedelta(seconds=random.randint(15, 45))
            events.append({
                "event_id": f"ev_{uuid.uuid4().hex[:12]}",
                "timestamp": session_time.isoformat() + "Z",
                "student_id": student_id,
                "topic_id": topic_id,
                "event_type": "confidence_assessment_submitted",
                "attempt_id": None,
                "question_id": None,
                "confidence_score": confidence_score,
                "selected_option": None,
                "is_correct": None,
                "response_time_seconds": None,
                "quiz_score": None,
                "revision_status": None,
                "readiness_status": None,
                "is_synthetic": True
            })

            # Check if revision is triggered (threshold < 60) or optional
            needs_revision = confidence_score < 60.0
            completed_revision = False
            revision_boost = 0.0

            if needs_revision or random.random() < 0.25:
                # Event 3: Revision Opened
                session_time += timedelta(seconds=random.randint(10, 30))
                events.append({
                    "event_id": f"ev_{uuid.uuid4().hex[:12]}",
                    "timestamp": session_time.isoformat() + "Z",
                    "student_id": student_id,
                    "topic_id": topic_id,
                    "event_type": "revision_opened",
                    "attempt_id": None,
                    "question_id": None,
                    "confidence_score": None,
                    "selected_option": None,
                    "is_correct": None,
                    "response_time_seconds": None,
                    "quiz_score": None,
                    "revision_status": "opened",
                    "readiness_status": None,
                    "is_synthetic": True
                })

                # Event 4: Revision Completed
                rev_duration = random.randint(90, 320)
                session_time += timedelta(seconds=rev_duration)
                completed_revision = True
                revision_boost = 0.12  # modest boost in empirical comprehension

                events.append({
                    "event_id": f"ev_{uuid.uuid4().hex[:12]}",
                    "timestamp": session_time.isoformat() + "Z",
                    "student_id": student_id,
                    "topic_id": topic_id,
                    "event_type": "revision_completed",
                    "attempt_id": None,
                    "question_id": None,
                    "confidence_score": None,
                    "selected_option": None,
                    "is_correct": None,
                    "response_time_seconds": float(rev_duration),
                    "quiz_score": None,
                    "revision_status": "completed",
                    "readiness_status": None,
                    "is_synthetic": True
                })

            # Student takes a quiz (1 to 2 attempts)
            num_attempts = 1 if confidence_score >= 70 and not needs_revision else random.choice([1, 2])

            for attempt_num in range(1, num_attempts + 1):
                attempt_id = f"att_{student_id[-3:]}_{topic_id[-4:]}_{attempt_num}"
                session_time += timedelta(seconds=random.randint(15, 60))

                # Event 5: Quiz Started
                events.append({
                    "event_id": f"ev_{uuid.uuid4().hex[:12]}",
                    "timestamp": session_time.isoformat() + "Z",
                    "student_id": student_id,
                    "topic_id": topic_id,
                    "event_type": "quiz_started",
                    "attempt_id": attempt_id,
                    "question_id": None,
                    "confidence_score": None,
                    "selected_option": None,
                    "is_correct": None,
                    "response_time_seconds": None,
                    "quiz_score": None,
                    "revision_status": None,
                    "readiness_status": None,
                    "is_synthetic": True
                })

                # Answer 5 questions
                correct_answers_count = 0
                attempt_boost = 0.08 * (attempt_num - 1)  # practice effect on repeated attempt

                for q_idx in range(1, 6):
                    question_id = f"q_{topic_id[-6:]}_{q_idx:02d}"
                    # Probability of answering correctly modeled as logistic function
                    # theta = student_aptitude + revision_boost + attempt_boost - topic_difficulty
                    logit = 3.2 * (student_aptitude + revision_boost + attempt_boost - topic_difficulty)
                    p_correct = float(np.clip(sigmoid(logit), 0.10, 0.95))

                    is_correct = bool(random.random() < p_correct)
                    if is_correct:
                        correct_answers_count += 1

                    resp_time = round(random.uniform(12.0, 65.0), 1)
                    session_time += timedelta(seconds=int(resp_time) + 2)

                    # Options assignment
                    correct_opt = random.choice(["A", "B", "C", "D"])
                    if is_correct:
                        selected_opt = correct_opt
                    else:
                        other_opts = [o for o in ["A", "B", "C", "D"] if o != correct_opt]
                        selected_opt = random.choice(other_opts)

                    # Event 6: Question Answered
                    events.append({
                        "event_id": f"ev_{uuid.uuid4().hex[:12]}",
                        "timestamp": session_time.isoformat() + "Z",
                        "student_id": student_id,
                        "topic_id": topic_id,
                        "event_type": "question_answered",
                        "attempt_id": attempt_id,
                        "question_id": question_id,
                        "confidence_score": None,
                        "selected_option": selected_opt,
                        "is_correct": is_correct,
                        "response_time_seconds": resp_time,
                        "quiz_score": None,
                        "revision_status": None,
                        "readiness_status": None,
                        "is_synthetic": True
                    })

                quiz_score = round((correct_answers_count / 5.0) * 100.0, 1)

                # Event 7: Quiz Submitted
                session_time += timedelta(seconds=random.randint(5, 15))
                events.append({
                    "event_id": f"ev_{uuid.uuid4().hex[:12]}",
                    "timestamp": session_time.isoformat() + "Z",
                    "student_id": student_id,
                    "topic_id": topic_id,
                    "event_type": "quiz_submitted",
                    "attempt_id": attempt_id,
                    "question_id": None,
                    "confidence_score": None,
                    "selected_option": None,
                    "is_correct": None,
                    "response_time_seconds": None,
                    "quiz_score": quiz_score,
                    "revision_status": None,
                    "readiness_status": None,
                    "is_synthetic": True
                })

                # Determine readiness category based on explicit rules
                if quiz_score >= 80.0:
                    readiness = "Demonstrated Mastery"
                elif quiz_score >= 60.0:
                    readiness = "Developing"
                else:
                    readiness = "Needs Revision"

                # Event 8: Quiz Result Calculated
                events.append({
                    "event_id": f"ev_{uuid.uuid4().hex[:12]}",
                    "timestamp": session_time.isoformat() + "Z",
                    "student_id": student_id,
                    "topic_id": topic_id,
                    "event_type": "quiz_result_calculated",
                    "attempt_id": attempt_id,
                    "question_id": None,
                    "confidence_score": None,
                    "selected_option": None,
                    "is_correct": None,
                    "response_time_seconds": None,
                    "quiz_score": quiz_score,
                    "revision_status": None,
                    "readiness_status": readiness,
                    "is_synthetic": True
                })

                # Event 9: Recommendation Displayed
                events.append({
                    "event_id": f"ev_{uuid.uuid4().hex[:12]}",
                    "timestamp": (session_time + timedelta(seconds=2)).isoformat() + "Z",
                    "student_id": student_id,
                    "topic_id": topic_id,
                    "event_type": "recommendation_displayed",
                    "attempt_id": attempt_id,
                    "question_id": None,
                    "confidence_score": None,
                    "selected_option": None,
                    "is_correct": None,
                    "response_time_seconds": None,
                    "quiz_score": None,
                    "revision_status": None,
                    "readiness_status": readiness,
                    "is_synthetic": True
                })

    df = pd.DataFrame(events)
    return df


if __name__ == "__main__":
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "raw")
    os.makedirs(output_dir, exist_ok=True)
    output_csv = os.path.join(output_dir, "student_interactions_bootstrap.csv")

    print(f"Generating synthetic bootstrap dataset with seed={RANDOM_SEED}...")
    df_events = generate_bootstrap_events(num_students=50)

    df_events.to_csv(output_csv, index=False)
    print(f"Successfully generated {len(df_events)} interaction events across {df_events['student_id'].nunique()} students.")
    print(f"Output saved to: {output_csv}")
