from typing import List
from fastapi import APIRouter, HTTPException
from backend.schemas import SubjectOut, TopicOut
from backend.curriculum_data import SUBJECTS, TOPICS

router = APIRouter(prefix="/curriculum", tags=["Curriculum"])


@router.get("/subjects", response_model=List[SubjectOut])
def get_subjects():
    return SUBJECTS


@router.get("/topics", response_model=List[TopicOut])
def get_all_topics():
    return TOPICS


@router.get("/topics/{subject_id}", response_model=List[TopicOut])
def get_topics_by_subject(subject_id: str):
    matched = [t for t in TOPICS if t["subject_id"] == subject_id]
    if not matched:
        raise HTTPException(status_code=404, detail=f"No topics found for subject '{subject_id}'")
    return matched
