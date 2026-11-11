# Data Schema & Interaction Event Specification

This document defines the interaction event stream schema and the relational entity tables for the Technical Skill Development Assistant.

---

## 1. Learning Interaction Telemetry Schema
All student actions generate an immutable, structured event record logged asynchronously.

| Field Name | Type | Allowed Values / Format | Description |
|---|---|---|---|
| `event_id` | String | UUIDv4 (e.g. `ev_9f81a74e...`) | Unique identifier for the learning event |
| `timestamp` | String | ISO 8601 UTC (`YYYY-MM-DDTHH:MM:SSZ`) | Event creation timestamp |
| `student_id` | String | Pseudonymous ID (`std_anon_001`) | Non-PII identifier for the student session |
| `topic_id` | String | Stable slug (e.g. `topic-supervised-learning`) | Identifier of the technical topic |
| `event_type` | String | Enum (see below) | Specific user journey action |
| `confidence_score` | Float | `0.0` – `100.0` or `null` | Self-reported rating if event is confidence-related |
| `attempt_id` | String | UUID or `null` | Associated quiz attempt ID if applicable |
| `question_id` | String | String or `null` | Associated question ID if applicable |
| `selected_option` | String | `A`, `B`, `C`, `D`, `null` | Selected MCQ option |
| `is_correct` | Boolean | `true`, `false`, `null` | Answer correctness |
| `response_time_seconds` | Float | `>= 0.0` or `null` | Time spent on the question or activity |
| `quiz_score` | Float | `0.0` – `100.0` or `null` | Overall attempt score |
| `revision_status` | String | `opened`, `completed`, `null` | Revision phase status |
| `is_synthetic` | Boolean | `true`, `false` | Distinguishes bootstrap data from live interaction |

### Supported Event Types:
1. `topic_selected`
2. `confidence_assessment_submitted`
3. `revision_opened`
4. `revision_completed`
5. `quiz_started`
6. `question_answered`
7. `quiz_submitted`
8. `quiz_result_calculated`
9. `topic_reassessed`
10. `recommendation_displayed`

---

## 2. Topic Readiness Categories & Thresholds
Readiness is strictly evidence-based and distinguishes self-assessment from demonstrated knowledge:

| Readiness Status | Definition & Logic |
|---|---|
| **Not Yet Assessed** | Topic selected or confidence rated, but no quiz attempt completed. |
| **Needs Revision** | Quiz score $< 60.0\%$ regardless of confidence. |
| **Developing** | Quiz score between $60.0\%$ and $79.9\%$, or Quiz score $\ge 80.0\%$ with only 1 attempt and low initial confidence. |
| **Nearly Ready** | Quiz score $\ge 80.0\%$ with confirmed revision or consistent prior performance. |
| **Demonstrated Strong Mastery** | Quiz score $\ge 90.0\%$ on at least 2 attempts with low skip rate and fast response time. |

> **Critical Rule:** Self-reported confidence can **never** substitute for missing quiz results. A topic with $100\%$ confidence and zero quiz attempts is displayed as **"Provisional / Not Yet Assessed"**.
