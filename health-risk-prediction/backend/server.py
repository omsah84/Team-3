import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

# Load the trained model and label encoders
model = joblib.load("../model/random_forest_categorical.pkl")
label_encoders = joblib.load("../model/label_encoders.pkl")

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Health Risk Prediction API!"})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data from request
        data = request.json
        
        # Expected input features
        expected_features = ["age", "family_history", "smoking", "alcohol", 
                             "diet_score", "physical_activity", "symptom_score", "mri_abnormality"]
        
        # Ensure all features are provided
        for feature in expected_features:
            if feature not in data:
                return jsonify({"error": f"Missing feature: {feature}"}), 400

        # Convert categorical values to numerical using label encoders
        for col in ["family_history", "smoking", "alcohol", "mri_abnormality"]:
            if data[col] in label_encoders[col].classes_:
                data[col] = label_encoders[col].transform([data[col]])[0]
            else:
                return jsonify({"error": f"Invalid value for {col}: {data[col]}"}), 400

        # Convert data to NumPy array for prediction
        input_data = np.array([[data[feature] for feature in expected_features]])

        # Make prediction
        prediction = model.predict(input_data)[0]
        risk_level = "High" if prediction == 1 else "Low"

        return jsonify({"risk_level": risk_level})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask API
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
