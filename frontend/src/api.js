import axios from 'axios';

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: apiBaseUrl,
  timeout: 5000,
});

// Curated Fallback Data for offline / initial development
export const FALLBACK_CURRICULUM = {
  subjects: [
    {
      subject_id: 'sub_ml_core',
      subject_name: 'Machine Learning Core',
      description: 'Foundations of learning algorithms, statistical modeling, and generalization.',
      topics_count: 4
    },
    {
      subject_id: 'sub_mlops_eng',
      subject_name: 'MLOps & Reproducibility',
      description: 'Pipelines, data versioning, experiment tracking, and artifact management.',
      topics_count: 3
    }
  ],
  topics: {
    sub_ml_core: [
      {
        topic_id: 'topic_superv_01',
        topic_name: 'Supervised Learning & Loss Functions',
        description: 'Empirical risk minimization, MSE, Cross-Entropy, and regularization.',
        difficulty: 'Medium',
        estimated_minutes: 20
      },
      {
        topic_id: 'topic_bias_var_02',
        topic_name: 'Bias-Variance Tradeoff',
        description: 'Underfitting vs overfitting, model complexity, and validation curves.',
        difficulty: 'Medium',
        estimated_minutes: 15
      },
      {
        topic_id: 'topic_eval_metrics_03',
        topic_name: 'Classification Metrics & Imbalance',
        description: 'Precision, Recall, F1-Score, ROC-AUC, and PR curves.',
        difficulty: 'Hard',
        estimated_minutes: 25
      },
      {
        topic_id: 'topic_tree_ensembles_04',
        topic_name: 'Decision Trees & Ensembles',
        description: 'Gini impurity, bagging, random forests, and gradient boosting.',
        difficulty: 'Hard',
        estimated_minutes: 30
      }
    ],
    sub_mlops_eng: [
      {
        topic_id: 'topic_dvc_version_01',
        topic_name: 'Data & Pipeline Versioning (DVC)',
        description: 'Tracking large datasets, remote storage, and DAG pipeline reproducibility.',
        difficulty: 'Medium',
        estimated_minutes: 20
      },
      {
        topic_id: 'topic_mlflow_track_02',
        topic_name: 'Experiment Tracking (MLflow)',
        description: 'Logging parameters, metrics, run artifacts, and model registry lifecycle.',
        difficulty: 'Medium',
        estimated_minutes: 25
      },
      {
        topic_id: 'topic_leakage_prep_03',
        topic_name: 'Feature Leakage & Data Hygiene',
        description: 'Pre-quiz feature separation, train/test split hygiene, and leakage prevention.',
        difficulty: 'Hard',
        estimated_minutes: 25
      }
    ]
  },
  revisions: {
    topic_superv_01: {
      topic_id: 'topic_superv_01',
      topic_name: 'Supervised Learning & Loss Functions',
      summary: 'Supervised learning fits a mapping function f(X) -> Y using ground truth labels. The objective is minimized via an optimization algorithm guided by a loss function.',
      key_definitions: [
        { term: 'Empirical Risk', definition: 'The average loss calculated over the observed training sample.' },
        { term: 'Cross-Entropy Loss', definition: 'Measures the difference between two probability distributions for classification.' },
        { term: 'L2 Regularization (Ridge)', definition: 'Penalizes large weights by adding the squared L2 norm to the loss function.' }
      ],
      flashcards: [
        {
          card_id: 'fc_01',
          front: 'What does Mean Squared Error (MSE) penalize more heavily than Mean Absolute Error (MAE)?',
          back: 'MSE squares errors, heavily penalizing large outliers and deviations compared to linear MAE.'
        },
        {
          card_id: 'fc_02',
          front: 'When is binary cross-entropy preferred over MSE?',
          back: 'When modeling probabilistic outputs between 0 and 1, avoiding vanishing gradients on extreme misclassifications.'
        }
      ]
    },
    topic_eval_metrics_03: {
      topic_id: 'topic_eval_metrics_03',
      topic_name: 'Classification Metrics & Imbalance',
      summary: 'Raw accuracy is misleading when classes are imbalanced. Robust evaluation requires precision, recall, F1, and PR-AUC.',
      key_definitions: [
        { term: 'Precision', definition: 'True Positives / (True Positives + False Positives) — measures exactness.' },
        { term: 'Recall (Sensitivity)', definition: 'True Positives / (True Positives + False Negatives) — measures completeness.' },
        { term: 'Macro F1-Score', definition: 'Unweighted mean of F1-scores across all individual classes.' }
      ],
      flashcards: [
        {
          card_id: 'fc_03',
          front: 'If fraud occurs in 0.1% of transactions, what is the accuracy of a model that predicts "No Fraud" always?',
          back: '99.9% accuracy — proving that accuracy is completely uninformative under extreme class imbalance.'
        },
        {
          card_id: 'fc_04',
          front: 'What metric should you optimize when false negatives are catastrophic (e.g. disease diagnosis)?',
          back: 'Recall (Sensitivity), to minimize missed positive cases.'
        }
      ]
    }
  },
  quizzes: {
    topic_superv_01: [
      {
        question_id: 'q_sup_1',
        text: 'Which loss function is standard for multi-class classification with softmax outputs?',
        options: ['A. Categorical Cross-Entropy', 'B. Mean Squared Error', 'C. Hinge Loss', 'D. Cosine Similarity'],
        correct_option: 'A',
        explanation: 'Categorical cross-entropy directly measures the divergence between one-hot labels and predicted probability distributions.'
      },
      {
        question_id: 'q_sup_2',
        text: 'What is the primary effect of adding an L1 regularization term (Lasso) to a linear model?',
        options: ['A. Induces sparsity by driving non-essential coefficients to zero', 'B. Guarantees zero training error', 'C. Increases model variance', 'D. Accelerates gradient descent computation'],
        correct_option: 'A',
        explanation: 'L1 regularization produces sparse feature representations due to diamond-shaped geometric constraint boundaries.'
      }
    ],
    topic_eval_metrics_03: [
      {
        question_id: 'q_eval_1',
        text: 'When evaluating a rare defect detection model (1 in 10,000 items), which metric provides the most reliable comparison?',
        options: ['A. PR-AUC (Precision-Recall AUC) or F1-score', 'B. Accuracy', 'C. Explained Variance', 'D. Mean Absolute Percentage Error'],
        correct_option: 'A',
        explanation: 'Under heavy class imbalance, Precision-Recall curves focus strictly on the minority positive class without distortion from true negatives.'
      },
      {
        question_id: 'q_eval_2',
        text: 'What is the relationship between Precision and Recall when moving the classification decision threshold higher?',
        options: ['A. Precision generally increases, while Recall decreases', 'B. Both Precision and Recall always increase', 'C. Recall increases, while Precision decreases', 'D. Neither metric changes'],
        correct_option: 'A',
        explanation: 'A stricter threshold demands higher model confidence for positive predictions, reducing false positives (higher precision) but increasing false negatives (lower recall).'
      }
    ]
  }
};

// Telemetry Event Dispatcher
export const logLearningEvent = async (eventData) => {
  const payload = {
    event_id: `ev_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`,
    timestamp: new Date().toISOString(),
    student_id: localStorage.getItem('student_id') || 'std_anon_learner',
    ...eventData,
  };

  try {
    await api.post('/telemetry/event', payload);
  } catch (err) {
    // If backend is unreachable, buffer event in localStorage
    const existing = JSON.parse(localStorage.getItem('buffered_events') || '[]');
    existing.push(payload);
    localStorage.setItem('buffered_events', JSON.stringify(existing.slice(-200)));
  }
  return payload;
};

export default api;
