# Dataset Card: Technical Skill Learning Interaction Telemetry

## 1. Dataset Summary
- **Dataset Name**: Student Interaction Telemetry (Bootstrap v1.0)
- **Primary Owner**: Member 1 (Shreyas — Data Acquisition, Data Quality & EDA)
- **Version**: `1.0.0-synthetic-bootstrap`
- **Location**: `data/raw/student_interactions_bootstrap.csv`
- **Date Created**: October 2026
- **License**: Academic Use Only — Open Data Attribution
- **Dataset Type**: Synthetic Bootstrap Interaction Telemetry for Cold-Start Machine Learning Pipelines

---

## 2. Dataset Motivation & Intended Use
### Problem Addressed:
Before students actively engage with the new web platform, a cold-start data challenge exists: no empirical student interaction logs are available for training baseline predictive models or testing MLOps pipelines.

### Intended Use:
- Benchmarking Phase 1 data validation scripts, feature engineering pipelines, and baseline models (Member 2).
- Validating the end-to-end MLOps pipeline with DVC dataset tracking and MLflow experiment logging (Member 4).
- Ensuring schema compliance across backend and frontend contracts.

### Out-of-Scope / Prohibited Uses:
- Claiming that model evaluation metrics on this synthetic data prove pedagogical effectiveness or real-world student generalization.
- Representing these records as genuine human student observations.

---

## 3. Dataset Composition & Provenance
- **Total Records**: 2,721 event rows.
- **Unique Students**: 50 simulated pseudonymous learners (`std_sim_001` to `std_sim_050`).
- **Topics Covered**: 6 technical skill topics across Machine Learning & MLOps domains:
  1. `topic_superv_01`: Supervised Learning & Loss Functions
  2. `topic_bias_var_02`: Bias-Variance Tradeoff
  3. `topic_eval_metrics_03`: Classification Metrics & Imbalance
  4. `topic_tree_ensembles_04`: Decision Trees & Ensembles
  5. `topic_dvc_version_01`: Data & Pipeline Versioning (DVC)
  6. `topic_mlflow_track_02`: Experiment Tracking (MLflow)
- **Generation Method**: Generative simulation via `src/data/generate_bootstrap_dataset.py` with fixed random seed (`seed=42`).
- **Latent Parameters**:
  - Underlying aptitude modeled as $\mathcal{N}(0.55, 0.18)$ bounded in $[0.15, 0.95]$.
  - Calibration bias (overconfidence vs modesty) modeled as $\mathcal{N}(0.0, 0.12)$.
  - Question correctness modeled via Item Response Theory (logistic probability curve based on aptitude, difficulty, and revision status).

---

## 4. Privacy, Safety & Ethical Considerations
- **PII Protection**: No personally identifiable information (names, emails, IP addresses, institutional IDs) is included.
- **Identifier Strategy**: Fully pseudonymous student keys (`std_sim_...`).
- **Consent Notice**: In production, genuine student event collection displays an explicit in-app privacy notice before logging interaction events.
- **Leakage Prevention**: Every event is explicitly labeled with `is_synthetic = True`.

---

## 5. Known Limitations
1. **Synthetic Dynamics**: Cognitive processes (fatigue, distraction, outside learning) are idealized through statistical distributions.
2. **Deterministic Fallbacks**: Revision boosts and practice effects follow fixed distributional shifts.
3. **Transition to Production**: Once the website collects sufficient approved live interactions, this bootstrap dataset will be superseded by validated real telemetry logs under DVC versioning.
