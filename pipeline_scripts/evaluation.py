import json
import pathlib
import pickle
import tarfile
import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

if __name__ == "__main__":
    # Load model
    model_path = "/opt/ml/processing/model/model.tar.gz"
    with tarfile.open(model_path) as tar:
        tar.extractall(path=".")
    
    model = xgb.Booster()
    model.load_model("xgboost-model")
    
    # Load test data
    print("Loading test data...")
    test_features = pd.read_csv(
        "/opt/ml/processing/test/test_features.csv",
        header=None
    )
    test_labels = pd.read_csv(
        "/opt/ml/processing/test/test_labels.csv",
        header=None
    )
    
    X_test = test_features.values
    y_test = test_labels.values.ravel()
    
    print(f"Test samples: {len(X_test)}")
    
    # Make predictions
    dtest = xgb.DMatrix(X_test)
    predictions_proba = model.predict(dtest)
    predictions = (predictions_proba > 0.5).astype(int)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, zero_division=0)
    recall = recall_score(y_test, predictions, zero_division=0)
    f1 = f1_score(y_test, predictions, zero_division=0)
    
    try:
        roc_auc = roc_auc_score(y_test, predictions_proba)
    except:
        roc_auc = 0.0
    
    cm = confusion_matrix(y_test, predictions)
    
    # Create report
    report_dict = {
        "binary_classification_metrics": {
            "accuracy": {"value": float(accuracy), "standard_deviation": "NaN"},
            "precision": {"value": float(precision), "standard_deviation": "NaN"},
            "recall": {"value": float(recall), "standard_deviation": "NaN"},
            "f1": {"value": float(f1), "standard_deviation": "NaN"},
            "roc_auc": {"value": float(roc_auc), "standard_deviation": "NaN"},
        },
        "confusion_matrix": cm.tolist()
    }
    
    print("\nEvaluation Results:")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print(f"ROC AUC:   {roc_auc:.4f}")
    
    # Save evaluation report
    output_dir = "/opt/ml/processing/evaluation"
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    evaluation_path = f"{output_dir}/evaluation.json"
    with open(evaluation_path, "w") as f:
        f.write(json.dumps(report_dict))
    
    print(f"\nEvaluation report saved to {evaluation_path}")
