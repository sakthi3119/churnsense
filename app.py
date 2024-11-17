from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load the retrained model
model = pickle.load(open("mlmodel.sav", "rb"))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=["POST"])
def predict():
    try:
        # Extract form data
        contract = float(request.form['contract'])
        totalcharges = float(request.form['totalcharges'])
        onlinesecurity = float(request.form['onlinesecurity'])
        techsupport = float(request.form['techsupport'])
        internetservice = float(request.form['internetservice'])

        # Prepare input vector
        features = np.array([[contract, totalcharges, onlinesecurity, techsupport, internetservice]])

        # Make prediction
        prediction = model.predict(features)[0]
        confidence = max(model.predict_proba(features)[0]) * 100

        # Map prediction to readable output
        prediction_text = "Yes" if prediction == 1 else "No"

        return render_template("index.html", prediction=prediction_text, confidence=confidence)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
