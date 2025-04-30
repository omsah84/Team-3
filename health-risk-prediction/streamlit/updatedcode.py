import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Load the trained model and encoders
model = joblib.load("../model/random_forest_categorical.pkl")
label_encoders = joblib.load("../model/label_encoders.pkl")

# Streamlit UI
st.title("🏥 Health Risk Prediction")
st.markdown("### Enter patient details below:")

# Input fields
age = st.number_input("Age", min_value=1, max_value=100, step=1)
family_history = st.selectbox("Family History", ["No", "Yes"])
smoking = st.selectbox("Smoking", ["Non-Smoker", "Smoker"])
alcohol = st.selectbox("Alcohol Consumption", ["Non-Drinker", "Drinker"])
diet_score = st.slider("Diet Score (1-10)", min_value=1, max_value=10, step=1)
physical_activity = st.slider("Physical Activity (1-10)", min_value=1, max_value=10, step=1)
symptom_score = st.slider("Symptom Score (1-10)", min_value=1, max_value=10, step=1)
mri_abnormality = st.selectbox("MRI Abnormality", ["Normal", "Abnormal"])

# Encode categorical inputs
def encode_input(value, column_name):
    return label_encoders[column_name].transform([value])[0]

# Prepare input data
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

# Prediction
if st.button("Predict Health Risk"):
    prediction = model.predict(input_data)[0]
    risk_level = label_encoders["risk_level"].inverse_transform([prediction])[0]
    st.success(f"🔍 Predicted Risk Level: **{risk_level}**")

    # Risk probability bar chart
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(input_data)[0]
        classes = label_encoders["risk_level"].inverse_transform(np.arange(len(probabilities)))

        fig1, ax1 = plt.subplots()
        ax1.bar(classes, probabilities, color='skyblue')
        ax1.set_ylabel("Probability")
        ax1.set_title("Risk Level Probabilities")
        st.pyplot(fig1)

# Health profile radar chart
if st.checkbox("Show Health Profile Radar"):
    categories = ['Diet', 'Physical Activity', 'Symptoms']
    values = [diet_score, physical_activity, symptom_score]

    fig2 = go.Figure()
    fig2.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Your Scores'
    ))

    fig2.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=False,
        title="Patient Health Profile"
    )
    st.plotly_chart(fig2)

# Run using: streamlit run app.py
