import json
import joblib
import numpy as np
import os
import xgboost as xgb

def model_fn(model_dir):
    """Load model and preprocessing artifacts"""
    # Load XGBoost booster (better cross-version compatibility)
    model = xgb.Booster()
    model.load_model(os.path.join(model_dir, 'xgboost_model.json'))
    
    scaler = joblib.load(os.path.join(model_dir, 'scaler.pkl'))
    label_encoders = joblib.load(os.path.join(model_dir, 'label_encoders.pkl'))
    
    return {
        'model': model,
        'scaler': scaler,
        'label_encoders': label_encoders
    }

def input_fn(request_body, content_type='application/json'):
    """Parse input data"""
    if content_type == 'application/json':
        data = json.loads(request_body)
        return data
    else:
        raise ValueError(f"Unsupported content type: {content_type}")

def predict_fn(input_data, model_artifacts):
    """Make predictions"""
    model = model_artifacts['model']
    scaler = model_artifacts['scaler']
    label_encoders = model_artifacts['label_encoders']
    
    # Expected feature order
    feature_columns = [
        'airline', 'origin', 'destination', 'distance', 
        'day_of_week', 'month', 'departure_hour',
        'temperature', 'wind_speed', 'precipitation', 'visibility', 'snow'
    ]
    
    # Handle single record or batch
    if isinstance(input_data, dict):
        input_data = [input_data]
    
    # Process each record
    processed_data = []
    for record in input_data:
        features = []
        for col in feature_columns:
            value = record[col]
            # Encode categorical features
            if col in label_encoders:
                try:
                    value = label_encoders[col].transform([value])[0]
                except:
                    value = 0  # Unknown category
            features.append(value)
        processed_data.append(features)
    
    # Convert to numpy array
    X = np.array(processed_data, dtype=np.float32)
    
    # Scale numeric features
    numeric_indices = [3, 7, 8, 9, 10]  # distance, temperature, wind_speed, precipitation, visibility
    X[:, numeric_indices] = scaler.transform(X[:, numeric_indices])
    
    # Make predictions using booster - set feature names to match training
    dmatrix = xgb.DMatrix(X, feature_names=feature_columns)
    probabilities = model.predict(dmatrix)
    
    # For binary classification, XGBoost booster returns probabilities for positive class
    # Convert to class predictions (threshold 0.5)
    predictions = (probabilities > 0.5).astype(int)
    
    # Format probabilities as [[prob_class_0, prob_class_1], ...]
    # Convert numpy types to Python types for JSON serialization
    formatted_probs = [[float(1-p), float(p)] for p in probabilities]
    
    return {
        'predictions': [int(p) for p in predictions],
        'probabilities': formatted_probs
    }

def output_fn(prediction, accept='application/json'):
    """Format output"""
    if accept == 'application/json':
        return json.dumps(prediction), accept
    raise ValueError(f"Unsupported accept type: {accept}")
