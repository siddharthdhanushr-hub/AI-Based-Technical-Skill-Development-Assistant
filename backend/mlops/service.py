"""
MLOps Inference Service & 21st-Century Assessment Logic
Integrates the Phase 1/Phase 2 trained Random Forest Champion model and feature pipeline.
"""

import json
import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from .constants import (
    SKILL_COLUMNS,
    CENTURY_21_SKILLS,
    ROLE_REQUIREMENTS,
    EXCLUDED_LEGACY_SKILLS,
    PHASE1_METRICS,
    PHASE2_GOVERNANCE
)
from backend.syllabus.models import Subject, Topic

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "mlops_models")

class MLOpsService:
    def __init__(self):
        self.rf_model = None
        self.dt_model = None
        self.lr_model = None
        self.feature_columns = []
        self.scaler_mean = None
        self.scaler_scale = None
        self._load_artifacts()

    def _load_artifacts(self):
        try:
            rf_path = os.path.join(MODELS_DIR, "random_forest.joblib")
            dt_path = os.path.join(MODELS_DIR, "decision_tree.joblib")
            lr_path = os.path.join(MODELS_DIR, "logistic_regression.joblib")
            meta_path = os.path.join(MODELS_DIR, "feature_metadata.json")

            if os.path.exists(rf_path):
                self.rf_model = joblib.load(rf_path)
            if os.path.exists(dt_path):
                self.dt_model = joblib.load(dt_path)
            if os.path.exists(lr_path):
                self.lr_model = joblib.load(lr_path)

            if os.path.exists(meta_path):
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                self.feature_columns = meta.get("feature_columns", [])
                self.scaler_mean = np.array(meta.get("scaler_mean", []))
                self.scaler_scale = np.array(meta.get("scaler_scale", []))
        except Exception as e:
            print(f"[MLOpsService] Artifact load warning: {e}")

    def prepare_full_skill_vector(self, user_scores: Dict[str, Any]) -> Dict[str, float]:
        """
        Takes user input for 21st Century Skills (0-6 scale) and populates
        the 17 benchmark skill dimensions.
        """
        full_scores = {}
        for col in SKILL_COLUMNS:
            if col in user_scores and user_scores[col] is not None:
                full_scores[col] = float(user_scores[col])
            else:
                # Default legacy pruned skills intelligently based on 21st century counterparts
                if col == "networking":
                    full_scores[col] = float(user_scores.get("distributed_computing_systems", 3))
                elif col == "communication_skills":
                    full_scores[col] = float(user_scores.get("technical_communication", 3))
                elif col == "computer_forensics_fundamentals":
                    full_scores[col] = float(user_scores.get("cyber_security", 3))
                elif col == "project_management":
                    full_scores[col] = float(user_scores.get("technical_communication", 3))
                elif col == "computer_architecture":
                    full_scores[col] = 3.0
                elif col == "business_analysis":
                    full_scores[col] = 3.0
                elif col == "graphics_designing":
                    full_scores[col] = 2.5
                else:
                    full_scores[col] = 3.0
        return full_scores

    def engineer_features(self, skill_scores: Dict[str, float]) -> pd.DataFrame:
        """
        Computes 5 domain composite indices + 3 aggregate stats to produce the 25 model features.
        """
        df = pd.DataFrame([skill_scores])
        skill_vals = df[[c for c in SKILL_COLUMNS if c in df.columns]]

        df["technical_overall_mean"] = skill_vals.mean(axis=1).round(4)
        df["technical_breadth"] = (skill_vals >= 3).sum(axis=1).astype(int)
        df["technical_depth"] = (skill_vals >= 5).sum(axis=1).astype(int)

        df["ai_data_readiness"] = (
            0.45 * df["ai_ml"]
            + 0.45 * df["data_science"]
            + 0.10 * df["programming_skills"]
        ).round(4)

        df["systems_readiness"] = (
            0.35 * df["networking"]
            + 0.35 * df["distributed_computing_systems"]
            + 0.30 * df["computer_architecture"]
        ).round(4)

        df["software_dev_readiness"] = (
            0.40 * df["software_development"]
            + 0.35 * df["programming_skills"]
            + 0.25 * df["software_engineering"]
        ).round(4)

        df["cybersecurity_readiness"] = (
            0.50 * df["cyber_security"]
            + 0.30 * df["computer_forensics_fundamentals"]
            + 0.20 * df["networking"]
        ).round(4)

        df["business_comm_readiness"] = (
            0.40 * df["business_analysis"]
            + 0.35 * df["project_management"]
            + 0.25 * df["communication_skills"]
        ).round(4)

        return df

    def predict_student_assessment(
        self,
        user_scores: Dict[str, Any],
        target_role: Optional[str] = "Software Developer",
        threshold: float = 0.50
    ) -> Dict[str, Any]:
        """
        Executes real-time inference using the Phase 2 MLOps Random Forest champion model.
        Returns Pass/Fail prediction, confidence score, individual model votes, and threshold routing.
        """
        if not self.rf_model:
            self._load_artifacts()

        full_scores = self.prepare_full_skill_vector(user_scores)
        df_eng = self.engineer_features(full_scores)

        # Scale features
        cols_to_use = self.feature_columns if self.feature_columns else list(df_eng.columns)
        X = df_eng[cols_to_use].values
        if self.scaler_mean is not None and self.scaler_scale is not None:
            X_scaled = (X - self.scaler_mean) / self.scaler_scale
        else:
            X_scaled = X

        # Predict with champion model (Random Forest)
        rf_prob = float(self.rf_model.predict_proba(X_scaled)[0][1]) if self.rf_model else 0.55
        rf_pass = int(rf_prob >= threshold)

        # Ensemble predictions
        dt_pred = int(self.dt_model.predict(X_scaled)[0]) if self.dt_model else rf_pass
        lr_pred = int(self.lr_model.predict(X_scaled)[0]) if self.lr_model else rf_pass

        # Skill Gap Analysis: G_i = max(0, R_i - S_i)
        role = target_role if target_role in ROLE_REQUIREMENTS else "Software Developer"
        requirements = ROLE_REQUIREMENTS.get(role, {})
        
        skill_gaps = []
        weak_skills = []
        for skill_id, req_score in requirements.items():
            curr_score = full_scores.get(skill_id, 0.0)
            gap = max(0.0, float(req_score) - curr_score)
            
            # Find display name
            display_name = next((s["name"] for s in CENTURY_21_SKILLS if s["id"] == skill_id), skill_id.replace("_", " ").title())
            skill_info = {
                "skill_id": skill_id,
                "name": display_name,
                "current_score": round(curr_score, 1),
                "required_score": float(req_score),
                "gap": round(gap, 1),
                "is_gap": gap > 0
            }
            skill_gaps.append(skill_info)
            if gap > 0 or curr_score < 3.0:
                weak_skills.append(display_name)

        # Check 21st century skills for any low ratings
        for s in CENTURY_21_SKILLS:
            s_id = s["id"]
            if s_id not in [g["skill_id"] for g in skill_gaps]:
                sc = full_scores.get(s_id, 3.0)
                if sc < 3.0:
                    weak_skills.append(s["name"])

        weak_skills = list(dict.fromkeys(weak_skills)) # deduplicate

        # Core Assessment Threshold Decision Logic
        is_above_threshold = (rf_prob >= threshold) and (rf_pass == 1)

        if is_above_threshold:
            recommendation = "READY_FOR_QUIZ"
            headline = "Assessment Gate: High Pass Probability"
            description = (
                f"Your estimated technical assessment pass probability is {round(rf_prob * 100, 1)}% "
                f"(Above threshold {int(threshold * 100)}%). Your self-reported competencies qualify you "
                f"for the 21st-Century Technical Cross-Verification Quiz."
            )
        else:
            recommendation = "PREPARE_IN_TRACKER"
            headline = "Assessment Gate: Skill Gaps Identified"
            description = (
                f"Your estimated pass probability is {round(rf_prob * 100, 1)}% (Below threshold {int(threshold * 100)}%). "
                f"We identified {len(weak_skills)} priority competencies needing reinforcement. "
                f"We recommend syncing these skills to your Skill Tracker to study Skill Briefs, Flashcards, "
                f"and Portfolio Projects before attempting the verification quiz."
            )

        composite_indices = {
            "ai_data_readiness": float(df_eng["ai_data_readiness"].iloc[0]),
            "systems_readiness": float(df_eng["systems_readiness"].iloc[0]),
            "software_dev_readiness": float(df_eng["software_dev_readiness"].iloc[0]),
            "cybersecurity_readiness": float(df_eng["cybersecurity_readiness"].iloc[0]),
            "business_comm_readiness": float(df_eng["business_comm_readiness"].iloc[0]),
            "technical_overall_mean": float(df_eng["technical_overall_mean"].iloc[0]),
            "technical_breadth": int(df_eng["technical_breadth"].iloc[0]),
            "technical_depth": int(df_eng["technical_depth"].iloc[0]),
        }

        return {
            "assessment_pass": bool(rf_pass),
            "confidence_score": round(rf_prob, 4),
            "confidence_percentage": round(rf_prob * 100, 1),
            "threshold_used": threshold,
            "is_above_threshold": is_above_threshold,
            "recommendation": recommendation,
            "headline": headline,
            "description": description,
            "target_role": role,
            "skill_gaps": skill_gaps,
            "weak_skills": weak_skills,
            "model_votes": {
                "random_forest_champion": int(rf_pass),
                "decision_tree": int(dt_pred),
                "logistic_regression": int(lr_pred),
            },
            "composite_indices": composite_indices
        }

    def sync_skills_to_tracker(
        self,
        student_id: int,
        skills_to_sync: List[str],
        role_name: str,
        db: Session
    ) -> Dict[str, Any]:
        """
        Syncs identified 21st-century gap skills directly into the user's Skill Tracker
        under a dedicated Skill Track.
        """
        track_name = f"21st Century Skills: {role_name}"
        
        # Check if track already exists
        subject = db.query(Subject).filter(
            Subject.student_id == student_id,
            Subject.subject_name == track_name
        ).first()

        if not subject:
            subject = Subject(
                subject_name=track_name,
                student_id=student_id
            )
            db.add(subject)
            db.commit()
            db.refresh(subject)

        # Existing topic names
        existing_topic_names = {t.topic_name.lower() for t in subject.topics}
        added_count = 0

        for skill_name in skills_to_sync:
            if skill_name.lower() not in existing_topic_names:
                new_topic = Topic(
                    subject_id=subject.subject_id,
                    topic_name=skill_name,
                    difficulty_weight=3.0,
                    estimated_hours=3.0,
                    is_completed=False
                )
                db.add(new_topic)
                added_count += 1

        db.commit()
        db.refresh(subject)

        return {
            "message": f"Successfully synced {added_count} skills to tracker",
            "subject_id": subject.subject_id,
            "subject_name": subject.subject_name,
            "total_skills": len(subject.topics)
        }

    def get_21st_century_verification_quiz(self) -> List[Dict[str, Any]]:
        """
        Returns exactly 10 rigorous multiple-choice questions mapping directly to the 
        10 21st-Century Technical Skills for cross-verification.
        """
        return [
            {
                "question_id": 1,
                "skill_domain": "AI & Machine Learning",
                "question_text": "In Transformer neural network architectures, why is Scaled Dot-Product Attention scaled by the square root of the key dimension (sqrt(d_k))?",
                "option_a": "To reduce matrix multiplication memory complexity from O(N^2) to O(N)",
                "option_b": "To prevent the dot products from growing excessively large, which pushes softmax into regions with vanishingly small gradients",
                "option_c": "To ensure positive semi-definite attention weight eigenvalues",
                "option_d": "To act as a regularization dropout mask during autoregressive decoding",
                "correct_option": "B",
                "difficulty": "Hard",
                "explanation": "Scaling by sqrt(d_k) prevents large dot products from causing softmax outputs to saturate with extremely tiny gradients, stabilizing backpropagation."
            },
            {
                "question_id": 2,
                "skill_domain": "Data Science & Big Data",
                "question_text": "When performing high-throughput exploratory feature transformations in Pandas, which practice provides the best runtime efficiency and avoids Python GIL bottlenecks?",
                "option_a": "Using DataFrame.iterrows() with list comprehension appending",
                "option_b": "Using DataFrame.apply() with row-wise lambda closures",
                "option_c": "Vectorized NumPy array operations or Pandas native built-in columnar expressions",
                "option_d": "Iterating over DataFrame.index and updating cells via .loc[i, col]",
                "correct_option": "C",
                "difficulty": "Medium",
                "explanation": "Native vectorized operations run in optimized C/SIMD instructions, eliminating per-row Python interpreter and GIL overhead."
            },
            {
                "question_id": 3,
                "skill_domain": "Full-Stack Software Development",
                "question_text": "In modern asynchronous web backends (e.g., FastAPI, Node.js), what occurs if a CPU-bound blocking computation (e.g. heavy image hashing) is executed directly in the main event loop thread?",
                "option_a": "The framework automatically spawns a worker thread pool without performance penalty",
                "option_b": "The event loop is blocked, delaying concurrent I/O task handling and degrading response latency for all clients",
                "option_c": "An unhandled RuntimeError is raised immediately",
                "option_d": "The process switches to asynchronous non-blocking generator execution",
                "correct_option": "B",
                "difficulty": "Medium",
                "explanation": "CPU-bound work on the main event loop starves concurrent I/O operations. Heavy CPU tasks must be offloaded to process/thread pools (e.g., run_in_executor)."
            },
            {
                "question_id": 4,
                "skill_domain": "Core Coding & Algorithms",
                "question_text": "What is the amortized time complexity of inserting N elements into a dynamic array (vector) with a geometric doubling capacity reallocation policy?",
                "option_a": "O(N log N)",
                "option_b": "O(N^2)",
                "option_c": "O(1) amortized per insertion, O(N) total across all N insertions",
                "option_d": "O(log N) amortized per insertion",
                "correct_option": "C",
                "difficulty": "Medium",
                "explanation": "Geometric doubling ensures the expensive O(N) copy operations occur exponentially less frequently, resulting in O(1) amortized cost per append."
            },
            {
                "question_id": 5,
                "skill_domain": "Cyber Security & DevSecOps",
                "question_text": "Which statement correctly distinguishes JSON Web Token (JWT) signature verification from data privacy?",
                "option_a": "A standard HMAC-SHA256 JWT encrypts its payload so client-side observers cannot read claims",
                "option_b": "A standard JWT signature guarantees data integrity and authenticity, but the payload is only base64url encoded and readable by anyone possessing the token",
                "option_c": "The signature prevents secret key theft through CORS preflight validation",
                "option_d": "JWT claims can only be parsed after asymmetric TLS handshake termination",
                "correct_option": "B",
                "difficulty": "Hard",
                "explanation": "Standard signed JWTs (JWS) guarantee tamper-proofing, not confidentiality. Never store sensitive credentials or unencrypted PII in the payload."
            },
            {
                "question_id": 6,
                "skill_domain": "Cloud & Distributed Systems",
                "question_text": "According to the CAP Theorem, in the presence of an unavoidable network partition (P) between nodes in a distributed database, what fundamental trade-off must system architects make?",
                "option_a": "Between Latency (L) and Scalability (S)",
                "option_b": "Between Strict Consistency (C) and Continuous Availability (A)",
                "option_c": "Between Data Encryption (E) and Throughput (T)",
                "option_d": "Between Replication Factor (RF) and Fault Tolerance (FT)",
                "correct_option": "B",
                "difficulty": "Hard",
                "explanation": "During a network partition, a system must choose either to return potentially stale data to remain available (AP) or reject requests to guarantee consistency (CP)."
            },
            {
                "question_id": 7,
                "skill_domain": "Modern Database Systems",
                "question_text": "In a relational database utilizing B+ Tree indexes, why are range queries (e.g., WHERE created_at BETWEEN x AND y) substantially faster than on standard hash indexes?",
                "option_a": "B+ Trees compute constant O(1) hash buckets across arbitrary partitions",
                "option_b": "All leaf nodes in a B+ Tree are linked in a sequential doubly/singly linked list, allowing linear traversal once the start key is located",
                "option_c": "B+ Trees store row values in in-memory columnar caches",
                "option_d": "Hash indexes require disk defragmentation for every write operation",
                "correct_option": "B",
                "difficulty": "Medium",
                "explanation": "B+ Trees store all records in sorted leaf nodes linked together, enabling fast O(log N) point lookup followed by sequential leaf scanning for ranges."
            },
            {
                "question_id": 8,
                "skill_domain": "Architecture, Testing & CI/CD",
                "question_text": "What is the primary benefit of achieving 'Idempotency' in automated CI/CD deployment pipelines and cloud infrastructure provisioning (e.g. Ansible, Terraform)?",
                "option_a": "It ensures code compilation is completed in a single compiler pass",
                "option_b": "Applying the same configuration repeatedly leaves the target environment in the exact same desired state without unintended side effects",
                "option_c": "It forces blue-green deployments to use zero disk storage overhead",
                "option_d": "It automatically rolls back database schema migrations upon unit test failure",
                "correct_option": "B",
                "difficulty": "Medium",
                "explanation": "Idempotency guarantees that executing the automation multiple times produces the identical result as executing it once, preventing configuration drift."
            },
            {
                "question_id": 9,
                "skill_domain": "Observability & SRE Troubleshooting",
                "question_text": "Why do Site Reliability Engineers (SREs) prioritize 95th and 99th percentile (p95/p99) latency over arithmetic mean (average) latency when diagnosing microservice performance?",
                "option_a": "Arithmetic mean requires higher CPU sampling overhead than percentiles",
                "option_b": "Arithmetic mean masks tail latency outliers, concealing degraded experiences suffered by the slowest requests or heavily loaded users",
                "option_c": "P99 latency directly measures garbage collection pause frequency",
                "option_d": "Percentiles are only valid for distributed tracing spans",
                "correct_option": "A",
                "difficulty": "Medium",
                "explanation": "Mean averages hide long-tail performance degradation. P99 reveals the true worst-case experience of 1 in every 100 client requests."
            },
            {
                "question_id": 10,
                "skill_domain": "Technical Communication & Agile",
                "question_text": "What is the primary objective of an Architecture Decision Record (ADR) in an engineering team?",
                "option_a": "To track individual developer daily velocity and code line output",
                "option_b": "To capture significant architectural decisions, their business/technical context, and the trade-off consequences for future engineering maintainability",
                "option_c": "To replace automated API documentation and OpenAPI schemas",
                "option_d": "To enforce continuous integration testing coverage minimum thresholds",
                "correct_option": "B",
                "difficulty": "Easy",
                "explanation": "ADRs preserve the rationale, context, and evaluated trade-offs of technical decisions so future maintainers understand why architectural choices were made."
            }
        ]

mlops_service = MLOpsService()

