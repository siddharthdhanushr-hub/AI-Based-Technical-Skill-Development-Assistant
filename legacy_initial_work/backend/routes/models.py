from fastapi import APIRouter
from backend.schemas import PredictMasteryIn, PredictMasteryOut
from src.models.predictor import MasteryPredictor

router = APIRouter(prefix="/models", tags=["Machine Learning"])

# Initialize singleton inference service
predictor = MasteryPredictor()


@router.post("/predict-mastery", response_model=PredictMasteryOut)
def predict_topic_mastery(payload: PredictMasteryIn):
    result = predictor.predict_readiness(
        student_id=payload.student_id,
        topic_id=payload.topic_id,
        confidence_score=payload.confidence_score,
        completed_revision=payload.completed_revision,
        revision_duration_seconds=payload.revision_duration_seconds,
        prior_topic_attempts=payload.prior_topic_attempts,
        prior_topic_avg_score=payload.prior_topic_avg_score
    )

    return PredictMasteryOut(
        student_id=result["student_id"],
        topic_id=result["topic_id"],
        predicted_band=result["predicted_band"],
        class_probabilities=result["class_probabilities"],
        model_source=result["model_source"],
        is_fallback=result["is_fallback"],
        recommended_action=result["recommended_action"]
    )
