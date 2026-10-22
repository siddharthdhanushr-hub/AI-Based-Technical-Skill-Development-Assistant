"""
Integration & Contract Verification Tests for Frontend Curriculum & Telemetry
Author: Member 3 (Siddharth Chandrashekar C)
Role: Student Frontend, Revision, Flashcards and Quiz Experience
"""

import os
import re
import pytest

from src.features import VALID_TOPICS


def test_frontend_build_artifact_exists():
    """Verifies that the React production bundle compiles to valid HTML & assets."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dist_html = os.path.join(project_root, "frontend", "dist", "index.html")
    assert os.path.exists(dist_html), f"Frontend build output missing at {dist_html}. Run 'npm run build'."

    with open(dist_html, "r", encoding="utf-8") as f:
        html_content = f.read()

    assert "<div id=\"root\"></div>" in html_content
    assert "AI-Based Technical Skill Development Assistant" in html_content


def test_frontend_topic_identifiers_match_ml_contracts():
    """Verifies that topic IDs exposed in frontend/src/api.js match VALID_TOPICS in ML/Data modules."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    api_js_path = os.path.join(project_root, "frontend", "src", "api.js")
    assert os.path.exists(api_js_path)

    with open(api_js_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract all topic_id: '...' occurrences in api.js
    found_topics = set(re.findall(r"topic_id:\s*['\"]([^'\"]+)['\"]", content))

    for canonical_topic in VALID_TOPICS:
        assert canonical_topic in found_topics, (
            f"Canonical topic '{canonical_topic}' missing from frontend/src/api.js fallback curriculum!"
        )


def test_frontend_quiz_structure_hygiene():
    """Checks that question keys, options, and explanations in frontend api.js have correct schema."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    api_js_path = os.path.join(project_root, "frontend", "src", "api.js")

    with open(api_js_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Ensure every question has correct_option in A, B, C, D
    correct_options = re.findall(r"correct_option:\s*['\"]([A-D])['\"]", content)
    assert len(correct_options) >= 5, "Expected at least 5 validated quiz questions in api.js"

    # Ensure explanations exist
    explanations = re.findall(r"explanation:\s*['\"]([^'\"]+)['\"]", content)
    assert len(explanations) == len(correct_options)
