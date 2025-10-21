import pandas as pd
import numpy as np
import argparse
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-test-split-ratio", type=float, default=0.2)
    args, _ = parser.parse_known_args()
    
    print("Loading data...")
    input_data_path = "/opt/ml/processing/input/flight_data_complete.csv"
    df = pd.read_csv(input_data_path)
    print(f"Loaded {len(df)} records")
    
    # Select features
    feature_columns = [
        'airline', 'origin', 'destination', 'distance', 
        'day_of_week', 'month', 'departure_hour',
        'temperature', 'wind_speed', 'precipitation', 'visibility', 'snow'
    ]
    target_column = 'is_delayed'
    
    X = df[feature_columns].copy()
    y = df[target_column].copy()
    
    # Encode categorical variables
    categorical_features = ['airline', 'origin', 'destination']
    label_encoders = {}
    
    for col in categorical_features:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.train_test_split_ratio, random_state=42, stratify=y
    )
    
    # Scale numerical features
    scaler = StandardScaler()
    numeric_features = ['distance', 'temperature', 'wind_speed', 'precipitation', 'visibility']
    
    X_train[numeric_features] = scaler.fit_transform(X_train[numeric_features])
    X_test[numeric_features] = scaler.transform(X_test[numeric_features])
    
    # Combine features and target
    train_data = pd.concat([y_train.reset_index(drop=True), X_train.reset_index(drop=True)], axis=1)
    test_data = pd.concat([y_test.reset_index(drop=True), X_test.reset_index(drop=True)], axis=1)
    
    # Save datasets
    print("Saving processed data...")
    train_data.to_csv("/opt/ml/processing/train/train.csv", index=False, header=False)
    test_data.to_csv("/opt/ml/processing/test/test.csv", index=False, header=False)
    
    # Save test features and labels separately for evaluation
    X_test.to_csv("/opt/ml/processing/test/test_features.csv", index=False, header=False)
    y_test.to_csv("/opt/ml/processing/test/test_labels.csv", index=False, header=False)
    
    # Save preprocessing artifacts
    joblib.dump(scaler, "/opt/ml/processing/model/scaler.pkl")
    joblib.dump(label_encoders, "/opt/ml/processing/model/label_encoders.pkl")
    
    print(f"Training data: {train_data.shape}")
    print(f"Test data: {test_data.shape}")
    print("Preprocessing complete!")
