"""
Model Evaluation & Benchmarking Module
Author: Member 2 (Shreyash Singh)
Role: Feature Engineering, Baseline Modeling, Model Comparison, and Evaluation
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


def evaluate_classification_model(
    model: Any,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    target_names: List[str] = None
) -> Dict[str, Any]:
    """
    Evaluates a trained classifier on test data and returns a standardized metrics dictionary.
    """
    y_pred = model.predict(X_test)

    acc = float(accuracy_score(y_test, y_pred))
    bal_acc = float(balanced_accuracy_score(y_test, y_pred))
    prec_macro = float(precision_score(y_test, y_pred, average="macro", zero_division=0))
    rec_macro = float(recall_score(y_test, y_pred, average="macro", zero_division=0))
    f1_macro = float(f1_score(y_test, y_pred, average="macro", zero_division=0))
    f1_weighted = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))

    cm = confusion_matrix(y_test, y_pred).tolist()
    report_dict = classification_report(y_test, y_pred, target_names=target_names, output_dict=True, zero_division=0)

    return {
        "accuracy": round(acc, 4),
        "balanced_accuracy": round(bal_acc, 4),
        "precision_macro": round(prec_macro, 4),
        "recall_macro": round(rec_macro, 4),
        "f1_macro": round(f1_macro, 4),
        "f1_weighted": round(f1_weighted, 4),
        "confusion_matrix": cm,
        "classification_report": report_dict,
        "predictions_sample": y_pred[:10].tolist()
    }


def compare_models(results: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
    """
    Constructs a comparative summary DataFrame across all evaluated baseline models.
    """
    rows = []
    for model_name, metrics in results.items():
        rows.append({
            "Model": model_name,
            "Accuracy": metrics["accuracy"],
            "Balanced Accuracy": metrics["balanced_accuracy"],
            "Precision (Macro)": metrics["precision_macro"],
            "Recall (Macro)": metrics["recall_macro"],
            "F1-Score (Macro)": metrics["f1_macro"],
            "F1-Score (Weighted)": metrics["f1_weighted"],
        })

    df_comp = pd.DataFrame(rows).sort_values(by="F1-Score (Macro)", ascending=False).reset_index(drop=True)
    return df_comp


def verify_zero_leakage(feature_columns: List[str], forbidden_columns: set) -> bool:
    """
    Verifies that no post-quiz outcome fields have leaked into the predictor column set.
    Raises ValueError if target leakage is detected.
    """
    leaked = set(feature_columns).intersection(forbidden_columns)
    if leaked:
        raise ValueError(f"CRITICAL TARGET LEAKAGE: Forbidden columns found in feature set: {leaked}")
    return True
