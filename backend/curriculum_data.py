"""
Curated Curriculum & Assessment Data
Contains vetted questions, concept summaries, and flashcards.
"""

SUBJECTS = [
    {
        "subject_id": "sub_ml_core",
        "subject_name": "Machine Learning Core",
        "description": "Foundations of learning algorithms, loss functions, generalization, and tree ensembles.",
        "topics_count": 4
    },
    {
        "subject_id": "sub_mlops_eng",
        "subject_name": "MLOps & Reproducibility",
        "description": "Pipeline reproducibility, DVC dataset tracking, MLflow experimentation, and data hygiene.",
        "topics_count": 2
    }
]

TOPICS = [
    {
        "topic_id": "topic_superv_01",
        "topic_name": "Supervised Learning & Loss Functions",
        "subject_id": "sub_ml_core",
        "description": "Empirical risk minimization, MSE vs Cross-Entropy, and L1/L2 regularization.",
        "difficulty": "Medium",
        "estimated_minutes": 20
    },
    {
        "topic_id": "topic_bias_var_02",
        "topic_name": "Bias-Variance Tradeoff",
        "subject_id": "sub_ml_core",
        "description": "Underfitting vs overfitting, decomposition of generalization error, and regularization.",
        "difficulty": "Medium",
        "estimated_minutes": 15
    },
    {
        "topic_id": "topic_eval_metrics_03",
        "topic_name": "Classification Metrics & Imbalance",
        "subject_id": "sub_ml_core",
        "description": "Precision, Recall, F1-Score, PR-AUC, and ROC curves under skewed class priors.",
        "difficulty": "Hard",
        "estimated_minutes": 25
    },
    {
        "topic_id": "topic_tree_ensembles_04",
        "topic_name": "Decision Trees & Ensembles",
        "subject_id": "sub_ml_core",
        "description": "Gini impurity, tree pruning, Bagging, Random Forests, and variance reduction.",
        "difficulty": "Hard",
        "estimated_minutes": 30
    },
    {
        "topic_id": "topic_dvc_version_01",
        "topic_name": "Data & Pipeline Versioning (DVC)",
        "subject_id": "sub_mlops_eng",
        "description": "Tracking non-code data assets, DAG pipeline reproducibility, and remote caching.",
        "difficulty": "Medium",
        "estimated_minutes": 20
    },
    {
        "topic_id": "topic_mlflow_track_02",
        "topic_name": "Experiment Tracking (MLflow)",
        "subject_id": "sub_mlops_eng",
        "description": "Structured logging of hyperparameters, evaluation metrics, and model binaries.",
        "difficulty": "Medium",
        "estimated_minutes": 25
    }
]

REVISIONS = {
    "topic_superv_01": {
        "topic_id": "topic_superv_01",
        "topic_name": "Supervised Learning & Loss Functions",
        "summary": "Supervised learning models the functional relationship f(X) -> Y from labeled inputs. Optimization updates model weights to minimize an empirical loss function subject to regularization constraints.",
        "key_definitions": [
            {"term": "Empirical Risk", "definition": "The average loss calculated over the finite observed training sample."},
            {"term": "Cross-Entropy Loss", "definition": "Measures divergence between predicted probability distributions and true categorical targets."},
            {"term": "L2 Regularization (Ridge)", "definition": "Adds the squared Euclidean norm of coefficients to the objective, shrinking weights toward zero."}
        ],
        "flashcards": [
            {"card_id": "fc_sup_01", "front": "What differentiates MSE from MAE regarding outlier sensitivity?", "back": "MSE squares error residuals, penalizing large outliers quadratically, whereas MAE scales linearly."},
            {"card_id": "fc_sup_02", "front": "Why is Cross-Entropy preferred over MSE for multi-class classification?", "back": "Cross-entropy paired with softmax provides monotonic steep gradients for confident misclassifications, avoiding gradient saturation."},
            {"card_id": "fc_sup_03", "front": "What geometric property of L1 regularization promotes sparse feature weights?", "back": "L1 ball contours have sharp corners on the coordinate axes, causing level-loss ellipses to intersect at zero."}
        ]
    },
    "topic_bias_var_02": {
        "topic_id": "topic_bias_var_02",
        "topic_name": "Bias-Variance Tradeoff",
        "summary": "Expected test error decomposes into Bias^2 + Variance + Irreducible Error. Over-parameterized models risk high variance (overfitting), while under-parameterized models suffer from high bias (underfitting).",
        "key_definitions": [
            {"term": "Bias", "definition": "Error introduced by approximating a complex real-world phenomenon with a simpler model."},
            {"term": "Variance", "definition": "Variability of model predictions when trained on different random training subsets."},
            {"term": "Irreducible Error", "definition": "Noise inherent in the measurement or unobserved data generating process."}
        ],
        "flashcards": [
            {"card_id": "fc_bv_01", "front": "If training error is near 0% but test error is 35%, what regime is the model in?", "back": "High Variance (Overfitting) — the model memorized training idiosyncrasies and fails to generalize."},
            {"card_id": "fc_bv_02", "front": "How does increasing training sample size typically influence model variance?", "back": "Increasing sample size constrains parameter estimates and reduces model variance."}
        ]
    },
    "topic_eval_metrics_03": {
        "topic_id": "topic_eval_metrics_03",
        "topic_name": "Classification Metrics & Imbalance",
        "summary": "When class priors are heavily skewed, standard classification accuracy produces deceptive results. Practitioners must evaluate Precision, Recall, and PR-AUC.",
        "key_definitions": [
            {"term": "Precision", "definition": "TP / (TP + FP) — fraction of positive predictions that are truly positive."},
            {"term": "Recall (Sensitivity)", "definition": "TP / (TP + FN) — fraction of all actual positive cases successfully caught."},
            {"term": "Macro F1-Score", "definition": "Unweighted arithmetic average of F1 scores across individual classes."}
        ],
        "flashcards": [
            {"card_id": "fc_eval_01", "front": "If positive class prevalence is 0.5%, why is ROC-AUC often overly optimistic?", "back": "ROC-AUC incorporates the True Negative rate, which dominates the denominator under severe imbalance."},
            {"card_id": "fc_eval_02", "front": "When is high Recall prioritized over high Precision?", "back": "When false negatives carry severe consequences (e.g. fatal disease diagnosis or security breach detection)."}
        ]
    },
    "topic_tree_ensembles_04": {
        "topic_id": "topic_tree_ensembles_04",
        "topic_name": "Decision Trees & Ensembles",
        "summary": "Decision trees recursively partition feature space using impurity criteria. Ensemble methods combine multiple trees via Bagging (Random Forest) or Boosting to optimize generalization.",
        "key_definitions": [
            {"term": "Gini Impurity", "definition": "1 - sum(p_i^2): measures the probability of misclassifying a randomly chosen element."},
            {"term": "Bagging (Bootstrap Aggregation)", "definition": "Trains trees independently on bootstrap samples, reducing variance via averaging."},
            {"term": "Feature Subsampling", "definition": "Randomly considers a subset of features at each split, decorrelating individual trees."}
        ],
        "flashcards": [
            {"card_id": "fc_tree_01", "front": "Why do single deep decision trees exhibit high variance?", "back": "Small perturbations in training data can cause cascading changes across all downstream split thresholds."},
            {"card_id": "fc_tree_02", "front": "Does Random Forest bagging primarily reduce bias or variance?", "back": "Primarily variance, by averaging predictions of de-correlated low-bias trees."}
        ]
    },
    "topic_dvc_version_01": {
        "topic_id": "topic_dvc_version_01",
        "topic_name": "Data & Pipeline Versioning (DVC)",
        "summary": "Data Version Control (DVC) bridges Git code tracking and large data files via lightweight content-addressable hash pointers, enabling reproducible ML DAG workflows.",
        "key_definitions": [
            {"term": "Pointer File (.dvc)", "definition": "Tiny metadata file tracking the md5 hash and size of a large data artifact in Git."},
            {"term": "DAG Pipeline (dvc.yaml)", "definition": "Declarative specification of dependencies, parameters, and outputs across pipeline stages."},
            {"term": "Remote Storage", "definition": "Central storage location (S3, GCS, local folder) housing versioned binary data."}
        ],
        "flashcards": [
            {"card_id": "fc_dvc_01", "front": "Why should large CSV datasets not be committed directly into Git?", "back": "Git stores entire file copies upon edits, causing repository bloat and severe performance degradation."},
            {"card_id": "fc_dvc_02", "front": "How does DVC determine if a pipeline stage needs to be recomputed upon 'dvc repro'?", "back": "By verifying whether the hash of any listed dependency or parameter changed since the last run."}
        ]
    },
    "topic_mlflow_track_02": {
        "topic_id": "topic_mlflow_track_02",
        "topic_name": "Experiment Tracking (MLflow)",
        "summary": "MLflow standardizes experiment tracking, model packaging, and registry management across the machine learning lifecycle.",
        "key_definitions": [
            {"term": "Experiment Run", "definition": "A discrete execution logging parameters, metrics, tags, and output artifacts."},
            {"term": "Artifact Store", "definition": "Directory or cloud bucket saving models, evaluation plots, and metadata."},
            {"term": "Model Registry", "definition": "Central hub for staging, versioning, and deploying validated ML model binaries."}
        ],
        "flashcards": [
            {"card_id": "fc_mlflow_01", "front": "What is the crucial difference between an MLflow parameter and an MLflow metric?", "back": "Parameters are static input hyperparameters; metrics are numeric values evaluated across training or testing."},
            {"card_id": "fc_mlflow_02", "front": "Why is automated experiment tracking critical for MLOps reproducibility?", "back": "It links exact code versions, dataset hashes, hyperparameters, and evaluation metrics to specific model binaries."}
        ]
    }
}

QUESTIONS = {
    "topic_superv_01": [
        {
            "question_id": "q_sup_01",
            "text": "Which loss function is the standard empirical formulation for multi-class classification with softmax outputs?",
            "options": ["A. Categorical Cross-Entropy", "B. Mean Squared Error", "C. Hinge Loss", "D. Cosine Distance"],
            "correct_option": "A",
            "explanation": "Categorical cross-entropy directly measures the divergence between target one-hot vectors and softmax predicted probabilities."
        },
        {
            "question_id": "q_sup_02",
            "text": "What is the characteristic mathematical effect of applying L1 regularization (Lasso) to model parameters?",
            "options": ["A. Induces sparsity by driving uninformative coefficients exactly to zero", "B. Eliminates all empirical training loss", "C. Exclusively scales model variance upward", "D. Guarantees convex optimization without gradient descent"],
            "correct_option": "A",
            "explanation": "The geometric corners of the L1 diamond constraint boundary frequently intersect loss contours on the axes, inducing exact zero coefficients."
        },
        {
            "question_id": "q_sup_03",
            "text": "Why does Mean Squared Error (MSE) fail to provide reliable gradients when used with sigmoid output activations for classification?",
            "options": ["A. Extreme misclassifications saturate the sigmoid derivative near zero, causing vanishing gradients", "B. MSE is non-differentiable", "C. MSE requires integer inputs", "D. Gradient descent cannot optimize quadratic functions"],
            "correct_option": "A",
            "explanation": "When predictions approach 0 or 1, the sigmoid derivative shrinks toward zero, causing MSE gradients to vanish even when prediction error is maximum."
        }
    ],
    "topic_bias_var_02": [
        {
            "question_id": "q_bv_01",
            "text": "A polynomial regression model achieves 100% accuracy on training observations but 52% on test data. What is the diagnosis?",
            "options": ["A. High Variance (Overfitting)", "B. High Bias (Underfitting)", "C. Irreducible Error Dominance", "D. Data Leakage across partitions"],
            "correct_option": "A",
            "explanation": "A severe discrepancy between training accuracy and held-out validation accuracy is the textbook manifestation of high variance."
        },
        {
            "question_id": "q_bv_02",
            "text": "Which of the following interventions will generally REDUCE model variance?",
            "options": ["A. Increasing L2 regularization strength or gathering more training data", "B. Increasing polynomial degree", "C. Removing pruning constraints on decision trees", "D. Expanding the feature count arbitrarily"],
            "correct_option": "A",
            "explanation": "Regularization and additional training samples constrain the model hypothesis space, suppressing variance."
        }
    ],
    "topic_eval_metrics_03": [
        {
            "question_id": "q_eval_01",
            "text": "Under heavy class imbalance (e.g. 0.1% positive class prevalence), which metric provides the most reliable comparison of model precision-recall trade-offs?",
            "options": ["A. Precision-Recall AUC (PR-AUC) or F1-Score", "B. Raw Classification Accuracy", "C. Mean Squared Error", "D. Explained Variance Score"],
            "correct_option": "A",
            "explanation": "Accuracy is skewed by the overwhelmingly prevalent negative class. PR-AUC isolates performance on the minority target of interest."
        },
        {
            "question_id": "q_eval_02",
            "text": "What happens to Precision and Recall when the classification decision threshold is increased from 0.5 to 0.85?",
            "options": ["A. Precision typically increases while Recall decreases", "B. Recall increases while Precision decreases", "C. Both Precision and Recall strictly increase", "D. Neither metric changes"],
            "correct_option": "A",
            "explanation": "A higher threshold demands stronger model confidence to declare a positive, reducing false positives while increasing false negatives."
        }
    ],
    "topic_tree_ensembles_04": [
        {
            "question_id": "q_tree_01",
            "text": "In a Random Forest classifier, why are individual trees trained on bootstrap samples and random subsets of features?",
            "options": ["A. To decorrelate the trees, maximizing the variance reduction achieved by ensemble averaging", "B. To force trees to be identical", "C. To increase model bias", "D. To make the trees fully interpretable linear models"],
            "correct_option": "A",
            "explanation": "Bagging and feature subsampling prevent a single dominant feature from dictating all tree roots, producing de-correlated trees that average out idiosyncratic variance."
        }
    ],
    "topic_dvc_version_01": [
        {
            "question_id": "q_dvc_01",
            "text": "What does a `.dvc` file committed to Git actually contain?",
            "options": ["A. Content-addressable hash (md5), file path, and artifact size metadata", "B. The entire raw binary dataset compressed in base64", "C. Python code for training machine learning models", "D. Docker container image configuration"],
            "correct_option": "A",
            "explanation": "DVC replaces large binary data in Git with tiny pointer files recording the artifact hash and size, while binary files reside in the DVC cache or remote storage."
        }
    ],
    "topic_mlflow_track_02": [
        {
            "question_id": "q_mlflow_01",
            "text": "Which MLflow method is used to record numeric evaluation scores evaluated at the conclusion of an experiment run?",
            "options": ["A. mlflow.log_metric()", "B. mlflow.log_param()", "C. mlflow.log_artifact()", "D. mlflow.register_model()"],
            "correct_option": "A",
            "explanation": "`mlflow.log_metric()` logs scalar numerical values (accuracy, loss, F1), while `log_param()` logs static configurations."
        }
    ]
}
