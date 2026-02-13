from flask import Flask, request, jsonify, render_template
import numpy as np
import os
from datetime import datetime
from model_loader import get_model, warm_up_model, is_model_ready, get_model_status

app = Flask(__name__)

# Feature names for reference
FEATURE_NAMES = ['contract', 'totalcharges', 'onlinesecurity', 'techsupport', 'internetservice']

# Warm up model on startup (loads in background thread-safe)
@app.before_first_request
def startup_warm_up():
    """Load model when first request arrives (automatic warm-up)."""
    warm_up_model()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/health')
def health():
    """
    Health check endpoint.
    Returns status of model loading.
    """
    status = get_model_status()
    
    if status['status'] == 'ready':
        return jsonify({"status": "ready", "mode": "production"}), 200
    elif status['status'] == 'loading':
        return jsonify({"status": "loading"}), 503
    else:
        # Return ready in demo mode (model not loaded but app works with random predictions)
        return jsonify({"status": "ready", "mode": "demo"}), 200

@app.route('/predict', methods=["POST"])
def predict():
    # Get model (loads automatically if not yet loaded)
    model = get_model()
    
    try:
        # Get data from JSON request
        data = request.get_json()
        
        # Validate required fields
        required_fields = FEATURE_NAMES
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]
        
        if missing_fields:
            return jsonify({
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
        
        # Extract and validate data
        try:
            features = np.array([
                float(data['contract']),
                float(data['totalcharges']),
                float(data['onlinesecurity']),
                float(data['techsupport']),
                float(data['internetservice'])
            ]).reshape(1, -1)
        except (ValueError, TypeError) as e:
            return jsonify({"error": f"Invalid data format: {str(e)}"}), 400

        # Make prediction (with fallback to demo mode if model unavailable)
        if model is not None:
            # Real model prediction
            prediction = model.predict(features)[0]
            prediction_proba = model.predict_proba(features)[0]
            confidence = max(prediction_proba) * 100
            churn_probability = prediction_proba[1] * 100
        else:
            # DEMO MODE: Generate realistic random prediction
            import random
            import hashlib
            
            # Use input data to seed randomness (consistent for same inputs)
            seed_str = f"{data['contract']}{data['totalcharges']}{data['onlinesecurity']}"
            seed = int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)
            random.seed(seed)
            
            # Higher risk factors increase churn probability
            base_churn_prob = 30.0
            
            # Month-to-month contracts = higher churn
            if float(data['contract']) == 1:
                base_churn_prob += 25
            
            # High charges = higher churn
            if float(data['totalcharges']) > 2000:
                base_churn_prob += 15
            
            # No online security or tech support = higher churn
            if float(data['onlinesecurity']) == 0:
                base_churn_prob += 10
            if float(data['techsupport']) == 0:
                base_churn_prob += 10
            
            # Add some randomness
            churn_probability = min(95, max(5, base_churn_prob + random.uniform(-10, 10)))
            prediction = 1 if churn_probability > 50 else 0
            confidence = churn_probability if prediction == 1 else (100 - churn_probability)
        
        # Map prediction to readable output
        prediction_text = ("The customer is more likely to churn" 
                         if prediction == 1 
                         else "The customer is likely to stay")

        # Prepare response
        response = {
            "prediction": prediction_text,
            "confidence": round(confidence, 2),
            "churn_probability": round(churn_probability, 2),
            "features": {
                "contract": {
                    "value": data['contract'],
                    "label": get_contract_label(data['contract'])
                },
                "total_charges": float(data['totalcharges']),
                "online_security": get_yes_no_label(data['onlinesecurity']),
                "tech_support": get_yes_no_label(data['techsupport']),
                "internet_service": get_internet_service_label(data['internetservice'])
            },
            "timestamp": datetime.now().isoformat(),
            "mode": "demo" if model is None else "production"
        }
        
        return jsonify(response)
        
    except Exception as e:
        app.logger.error(f"Prediction error: {str(e)}")
        return jsonify({
            "error": "An error occurred while processing your request.",
            "details": str(e)
        }), 500

# Helper functions for label mapping
def get_contract_label(value):
    mapping = {
        "1": "Month-to-month",
        "2": "One year",
        "3": "Two year"
    }
    return mapping.get(str(value), "Unknown")

def get_yes_no_label(value):
    value = str(value)
    if value == "0":
        return "No"
    elif value == "1":
        return "Yes"
    elif value == "2":
        return "No internet service"
    return "Unknown"

def get_internet_service_label(value):
    mapping = {
        "0": "No internet service",
        "1": "DSL",
        "2": "Fiber optic"
    }
    return mapping.get(str(value), "Unknown")

# This is for local development
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
