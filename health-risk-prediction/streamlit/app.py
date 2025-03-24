import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load the trained model and encoders
model = joblib.load("../model/random_forest_categorical.pkl")
label_encoders = joblib.load("../model/label_encoders.pkl")

# Streamlit UI
st.title("🏥 Health Risk Prediction")

st.markdown("### Enter patient details below:")

# Input fields for the user
age = st.number_input("Age", min_value=1, max_value=100, step=1)
family_history = st.selectbox("Family History", ["No", "Yes"])
smoking = st.selectbox("Smoking", ["Non-Smoker", "Smoker"])
alcohol = st.selectbox("Alcohol Consumption", ["Non-Drinker", "Drinker"])
diet_score = st.slider("Diet Score (1-10)", min_value=1, max_value=10, step=1)
physical_activity = st.slider("Physical Activity (1-10)", min_value=1, max_value=10, step=1)
symptom_score = st.slider("Symptom Score (1-10)", min_value=1, max_value=10, step=1)
mri_abnormality = st.selectbox("MRI Abnormality", ["Normal", "Abnormal"])

# Encode categorical inputs using the saved encoders
def encode_input(value, column_name):
    return label_encoders[column_name].transform([value])[0]

# Prepare the input for prediction
input_data = pd.DataFrame({
    "age": [age],
    "family_history": [encode_input(family_history, "family_history")],
    "smoking": [encode_input(smoking, "smoking")],
    "alcohol": [encode_input(alcohol, "alcohol")],
    "diet_score": [diet_score],
    "physical_activity": [physical_activity],
    "symptom_score": [symptom_score],
    "mri_abnormality": [encode_input(mri_abnormality, "mri_abnormality")]
})

# Predict Button
if st.button("Predict Health Risk"):
    prediction = model.predict(input_data)[0]
    
    # Decode the predicted risk level
    risk_level = label_encoders["risk_level"].inverse_transform([prediction])[0]

    st.success(f"🔍 Predicted Risk Level: **{risk_level}**")

# Run using: streamlit run app.py
