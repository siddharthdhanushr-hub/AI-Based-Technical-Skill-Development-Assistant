"""
Model Inference & Fallback Prediction Service
Author: Member 2 (Shreyash Singh)
Role: Feature Engineering, Baseline Modeling, Model Comparison, and Evaluation

Provides a reliable inference contract for the backend API and frontend,
featuring deterministic rule-based fallbacks if model artifacts are unavailable.
"""

import os
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
import joblib

TARGET_NAMES = ["Needs Revision", "Developing", "Demonstrated Mastery"]


class MasteryPredictor:
    """
    Inference wrapper for predicting pre-quiz student mastery bands.
    Automatically engages a transparent rule-based heuristic if the
    trained model artifact is unavailable.
    """

    def __init__(self, model_path: Optional[str] = None):
        if model_path is None:
            # Default to standard model location
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            model_path = os.path.join(project_root, "models", "mastery_classifier.joblib")

        self.model_path = model_path
        self.model = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
            except Exception as e:
                print(f"[MasteryPredictor Warning] Failed to load model from {self.model_path}: {e}. Engaging fallback.")
                self.model = None
        else:
            self.model = None

    def predict_readiness(
        self,
        student_id: str,
        topic_id: str,
        confidence_score: float,
        completed_revision: bool = False,
        revision_duration_seconds: float = 0.0,
        prior_topic_attempts: int = 0,
        prior_topic_avg_score: float = 50.0,
        prior_global_attempts: int = 0,
        prior_global_avg_score: float = 50.0
    ) -> Dict[str, Any]:
        """
        Predicts expected mastery band prior to attempting a quiz.
        Uses ML pipeline if available; otherwise falls back to calibrated deterministic rules.
        """
        # ML Inference Path
        if self.model is not None:
            try:
                features_df = pd.DataFrame([{
                    "topic_id": topic_id,
                    "confidence_score": float(confidence_score),
                    "completed_revision": int(completed_revision),
                    "revision_duration_seconds": float(revision_duration_seconds),
                    "prior_topic_attempts": int(prior_topic_attempts),
                    "prior_topic_avg_score": float(prior_topic_avg_score),
                    "prior_global_attempts": int(prior_global_attempts),
                    "prior_global_avg_score": float(prior_global_avg_score)
                }])

                pred_class_idx = int(self.model.predict(features_df)[0])
                predicted_label = TARGET_NAMES[pred_class_idx]

                # Probabilities if supported by classifier
                probs = {}
                if hasattr(self.model, "predict_proba"):
                    proba_vals = self.model.predict_proba(features_df)[0]
                    probs = {TARGET_NAMES[i]: round(float(proba_vals[i]), 4) for i in range(len(TARGET_NAMES))}

                return {
                    "student_id": student_id,
                    "topic_id": topic_id,
                    "predicted_band": predicted_label,
                    "class_probabilities": probs,
                    "model_source": "trained_baseline_model",
                    "is_fallback": False,
                    "recommended_action": self._get_recommendation(predicted_label, completed_revision)
                }
            except Exception as e:
                print(f"[MasteryPredictor Warning] Inference error: {e}. Executing fallback path.")

        # Deterministic Calibrated Fallback Rule
        return self._rule_based_fallback(
            student_id, topic_id, confidence_score, completed_revision, prior_topic_avg_score
        )

    def _rule_based_fallback(
        self,
        student_id: str,
        topic_id: str,
        confidence: float,
        completed_rev: bool,
        prior_avg: float
    ) -> Dict[str, Any]:
        """
        Transparent rule-based fallback based on confidence and revision completion.
        """
        effective_score = confidence * 0.7 + (prior_avg * 0.3)
        if completed_rev:
            effective_score += 10.0  # modest revision benefit

        if effective_score >= 80.0:
            band = "Demonstrated Mastery"
        elif effective_score >= 60.0:
            band = "Developing"
        else:
            band = "Needs Revision"

        return {
            "student_id": student_id,
            "topic_id": topic_id,
            "predicted_band": band,
            "class_probabilities": {
                "Needs Revision": 0.2 if band != "Needs Revision" else 0.7,
                "Developing": 0.6 if band == "Developing" else 0.2,
                "Demonstrated Mastery": 0.2 if band != "Demonstrated Mastery" else 0.7,
            },
            "model_source": "calibrated_rule_fallback",
            "is_fallback": True,
            "recommended_action": self._get_recommendation(band, completed_rev)
        }

    def _get_recommendation(self, band: str, completed_rev: bool) -> str:
        if band == "Needs Revision":
            if not completed_rev:
                return "Complete the concept summary and interactive flashcards before taking the quiz."
            return "Re-read key definitions and attempt a practice quiz attempt."
        elif band == "Developing":
            return "Review flashcards for targeted recall and proceed to the topic quiz."
        else:
            return "High readiness detected. Take the quiz directly to validate your mastery."
