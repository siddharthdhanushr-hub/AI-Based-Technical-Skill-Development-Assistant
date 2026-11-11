# Data Dictionary: Student Interaction Telemetry

## 1. Column Specifications

| Column Name | Data Type | Nullable | Valid Values / Constraints | Description | Role in ML Pipeline |
|---|---|---|---|---|---|
| `event_id` | String | No | Unique String (`ev_...`) | Primary key for the interaction event | Metadata / Join key |
| `timestamp` | Datetime (ISO 8601) | No | UTC Datetime string | Timestamp when the action was recorded | Temporal feature / Session ordering |
| `student_id` | String | No | `std_...` | Pseudonymous identifier for learner | Grouping identifier (GroupKFold split) |
| `topic_id` | String | No | Registered topic slug | Technical skill topic identifier | Categorical input feature |
| `event_type` | String | No | Enum (10 allowed actions) | Type of user interaction event | Event filter / State transition |
| `attempt_id` | String | Yes | `att_...` or `null` | Associated quiz attempt identifier | Attempt aggregator |
| `question_id` | String | Yes | `q_...` or `null` | Item identifier for assessment question | Item Response Analysis |
| `confidence_score` | Float | Yes | `0.0` – `100.0` | Self-reported rating of topic confidence | **Pre-Quiz Predictor Feature** |
| `selected_option` | String | Yes | `A`, `B`, `C`, `D`, or `null` | Selected MCQ option | Answer telemetry |
| `is_correct` | Boolean | Yes | `True`, `False`, or `null` | Question correctness | Outcome intermediate |
| `response_time_seconds` | Float | Yes | `>= 0.0` or `null` | Duration spent on question or revision | Behavioral feature |
| `quiz_score` | Float | Yes | `0.0` – `100.0` or `null` | Final percentage scored on quiz attempt | **Post-Quiz Target / Label** |
| `revision_status` | String | Yes | `opened`, `completed`, `null` | Revision phase status | **Pre-Quiz Feature** (`revision_completed`) |
| `readiness_status` | String | Yes | `Needs Revision`, `Developing`, `Demonstrated Mastery` | Computed grip category | **Post-Quiz Categorical Target** |
| `is_synthetic` | Boolean | No | `True`, `False` | Flag indicating synthetic vs real origin | Data hygiene audit filter |

---

## 2. Event Types & Associated Fields Matrix

| Event Type | Typical Non-Null Fields | Notes |
|---|---|---|
| `topic_selected` | `event_id`, `timestamp`, `student_id`, `topic_id` | Learner views curriculum topic |
| `confidence_assessment_submitted` | `event_id`, `timestamp`, `student_id`, `topic_id`, `confidence_score` | Slider rating submitted |
| `revision_opened` | `event_id`, `timestamp`, `student_id`, `topic_id`, `revision_status='opened'` | Flashcard / revision loaded |
| `revision_completed` | `event_id`, `timestamp`, `student_id`, `topic_id`, `response_time_seconds`, `revision_status='completed'` | Student marks revision complete |
| `quiz_started` | `event_id`, `timestamp`, `student_id`, `topic_id`, `attempt_id` | Quiz initialized |
| `question_answered` | `event_id`, `timestamp`, `student_id`, `topic_id`, `attempt_id`, `question_id`, `selected_option`, `is_correct`, `response_time_seconds` | Individual MCQ response logged |
| `quiz_submitted` | `event_id`, `timestamp`, `student_id`, `topic_id`, `attempt_id`, `quiz_score` | Quiz finished |
| `quiz_result_calculated` | `event_id`, `timestamp`, `student_id`, `topic_id`, `attempt_id`, `quiz_score`, `readiness_status` | Score and grip evaluated |
| `recommendation_displayed` | `event_id`, `timestamp`, `student_id`, `topic_id`, `readiness_status` | Rule-based recommendation shown |

---

## 3. Data Leakage Precautions
- **Strict Separation**: In predictive modeling (Member 2), features must **never** include `quiz_score`, `is_correct`, or `readiness_status` from the current attempt to predict that same attempt's outcome.
- **Pre-Quiz Features Only**: Predictors must be limited to prior attempt history, self-reported confidence, revision completion prior to the quiz, and topic identifier.
