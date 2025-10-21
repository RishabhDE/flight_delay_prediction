import pandas as pd
import numpy as np
import argparse
import os
import joblib
import xgboost as xgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    # Hyperparameters
    parser.add_argument("--max-depth", type=int, default=6)
    parser.add_argument("--eta", type=float, default=0.1)
    parser.add_argument("--num-round", type=int, default=100)
    parser.add_argument("--subsample", type=float, default=0.8)
    parser.add_argument("--colsample-bytree", type=float, default=0.8)
    
    # SageMaker specific arguments
    parser.add_argument("--model-dir", type=str, default=os.environ.get("SM_MODEL_DIR"))
    parser.add_argument("--train", type=str, default=os.environ.get("SM_CHANNEL_TRAIN"))
    parser.add_argument("--validation", type=str, default=os.environ.get("SM_CHANNEL_VALIDATION"))
    
    args, _ = parser.parse_known_args()
    
    # Load data
    print("Loading training data...")
    train_data = pd.read_csv(os.path.join(args.train, "train.csv"), header=None)
    
    # Split features and target
    y_train = train_data.iloc[:, 0].values
    X_train = train_data.iloc[:, 1:].values
    
    print(f"Training samples: {len(X_train)}")
    print(f"Features: {X_train.shape[1]}")
    
    # Calculate scale_pos_weight for imbalanced data
    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
    print(f"Scale pos weight: {scale_pos_weight:.2f}")
    
    # Create DMatrix
    dtrain = xgb.DMatrix(X_train, label=y_train)
    
    # Set parameters
    params = {
        'max_depth': args.max_depth,
        'eta': args.eta,
        'objective': 'binary:logistic',
        'eval_metric': 'logloss',
        'subsample': args.subsample,
        'colsample_bytree': args.colsample_bytree,
        'scale_pos_weight': scale_pos_weight
    }
    
    # Train model
    print("Training XGBoost model...")
    model = xgb.train(
        params=params,
        dtrain=dtrain,
        num_boost_round=args.num_round
    )
    
    # Save model
    model_path = os.path.join(args.model_dir, "xgboost-model")
    model.save_model(model_path)
    print(f"Model saved to {model_path}")
    
    print("Training complete!")
