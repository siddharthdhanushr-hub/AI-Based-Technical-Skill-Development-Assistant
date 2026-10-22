# Initial Model Evaluation & Baseline Benchmarks — Phase 1

**Author:** Member 2 (Shreyash Singh)  
**Role:** Feature Engineering, Baseline Modeling, Model Comparison, and Evaluation  
**Date:** October 2026  
**Status:** Completed & Verified  

---

## 1. Prediction Task & Formulation

### Problem Statement
In technical skill learning, providing students with timely, targeted recommendations requires anticipating their demonstrated grasp of a topic **before** they begin an assessment.

The prediction task is framed as a **pre-quiz multi-class classification problem**:
- **Goal**: Predict the student's demonstrated mastery band on an upcoming quiz attempt using strictly pre-quiz observations.
- **Target Variable**: `target_mastery_band`
  - Class `0` — **Needs Revision** (Demonstrated score $< 60.0\%$)
  - Class `1` — **Developing** (Demonstrated score between $60.0\%$ and $79.9\%$)
  - Class `2` — **Demonstrated Mastery** (Demonstrated score $\ge 80.0\%$)

---

## 2. Pre-Quiz Feature Set & Leakage Prevention

### A. Predictor Features
All features are computed chronologically using events that occurred **strictly before** the quiz attempt started:

| Feature Name | Type | Description |
|---|---|---|
| `confidence_score` | Float ($[0, 100]$) | Self-reported topic confidence score |
| `completed_revision` | Binary ($0 / 1$) | Indicates whether the student finished revision before the quiz |
| `revision_duration_seconds` | Float ($\ge 0$) | Total seconds spent in the revision & flashcard interface |
| `prior_topic_attempts` | Integer | Count of previous attempts taken on this specific topic |
| `prior_topic_avg_score` | Float ($[0, 100]$) | Historical mean score on this topic (default: $50.0$ if first attempt) |
| `prior_global_attempts` | Integer | Total attempts completed across other curriculum topics |
| `prior_global_avg_score` | Float ($[0, 100]$) | Historical average score across all other topics |
| `topic_id` | Categorical | Specific topic identifier (one-hot encoded) |

### B. Strict Target Leakage Precautions
- **Post-Quiz Isolation**: The current attempt's `quiz_score`, individual question response times, and answer correctness (`is_correct`) are **strictly prohibited** from the feature set.
- **Audit Verification**: Enforced programmatically via `verify_zero_leakage()` in `src/evaluation.py`.
- **Group-Based Partitioning**: Evaluated using `GroupShuffleSplit` on `student_id` (test size = $25\%$). This guarantees zero student overlap between train and test sets, preventing individual learner aptitude from leaking across partitions.

---

## 3. Baseline Comparison & Empirical Results

All models were evaluated on the held-out student test partition (63 attempts across 13 unseen students). Preprocessing transformations (`StandardScaler` and `OneHotEncoder`) were fitted strictly on the training partition.

| Model Algorithm | Accuracy | Balanced Accuracy | Precision (Macro) | Recall (Macro) | F1-Score (Macro) | F1-Score (Weighted) | Status |
|---|---|---|---|---|---|---|---|
| **Logistic Regression (L2, Balanced)** | **53.97%** | **53.38%** | **0.5248** | **0.5338** | **0.5268** | **0.5353** | **Selected Best Baseline** |
| **Random Forest ($N=100$, Depth=5)** | 49.21% | 50.36% | 0.5089 | 0.5036 | 0.4938 | 0.4943 | Competitive Ensemble |
| **Decision Tree (Depth=4)** | 47.62% | 45.72% | 0.4562 | 0.4572 | 0.4531 | 0.4728 | Interpretable Tree |
| **Dummy (Stratified)** | 34.92% | 35.89% | 0.3721 | 0.3589 | 0.3486 | 0.3500 | Trivial Random Baseline |
| **Dummy (Most Frequent)** | 26.98% | 33.33% | 0.0899 | 0.3333 | 0.1417 | 0.1147 | Majority Class Baseline |

---

## 4. Key Analytical Insights

1. **Superiority over Naïve Baselines**:
   - Logistic Regression achieved an F1-Score of **0.5268**, dramatically exceeding the majority class baseline (F1 = 0.1417) and stratified random guessing (F1 = 0.3486).
2. **Feature Importance (Weights for Mastery)**:
   - High self-reported confidence ($\beta = +0.72$) and completed revision ($\beta = +0.48$) were the strongest positive indicators of reaching the *Demonstrated Mastery* band.
   - Topics with higher intrinsic conceptual complexity (`topic_eval_metrics_03`) exhibited negative baseline weights, aligning with domain difficulty.
3. **Model Selection**:
   - **Logistic Regression** is recommended as the Phase 1 primary baseline due to its superior generalization on the grouped test partition, mathematical transparency, calibrated class probability outputs, and microsecond inference latency.
   - The serialized pipeline artifact is preserved at `models/mastery_classifier.joblib`.

---

## 5. Model Serving & Fallback Architecture

To protect student experience against service disruptions:
- The inference interface (`MasteryPredictor` in `src/models/predictor.py`) exposes a standardized Python contract.
- If the model binary is unavailable or corrupted, it automatically executes a **calibrated deterministic rule fallback**:
  $$\text{Score}_{\text{est}} = 0.70 \times C + 0.30 \times \bar{S}_{\text{prior}} + 10.0 \times \mathbb{I}(\text{revision})$$
- Inference outputs always indicate `is_fallback: False` (ML) or `is_fallback: True` (Rules) to maintain transparent accountability.

---

## 6. Academic & Scientific Caveats

> [!WARNING]
> **Synthetic Cold-Start Benchmark**
> All metrics reported above were obtained using the Phase 1 bootstrap synthetic dataset (`student_interactions_bootstrap.csv`). While the data reflects realistic cognitive patterns (including overconfidence and Dunning-Kruger gaps), these numerical metrics confirm **pipeline reproducibility and leak-free design**, NOT real-world educational efficacy.
>
> Live website usage will collect real learner telemetry, enabling re-training and verification on empirical classroom data in Phase 2.
