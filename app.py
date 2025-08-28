from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), 'mlmodel.sav')
try:
    model = pickle.load(open(model_path, 'rb'))
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Feature names for reference
FEATURE_NAMES = ['contract', 'totalcharges', 'onlinesecurity', 'techsupport', 'internetservice']

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=["POST"])
def predict():
    # Check if model is loaded
    if model is None:
        return jsonify({"error": "Model not loaded. Please try again later."}), 500
    
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

        # Make prediction
        prediction = model.predict(features)[0]
        prediction_proba = model.predict_proba(features)[0]
        confidence = max(prediction_proba) * 100
        
        # Get the probability of churn (class 1)
        churn_probability = prediction_proba[1] * 100
        
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
            "timestamp": datetime.now().isoformat()
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

# This is required for Vercel
app = app

# This is for local development
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
