import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load dataset
df = pd.read_csv("./data/dataset.csv")

# Rename columns for consistency
df.columns = [
    "patient_id", "age", "family_history", "smoking", "alcohol",
    "diet_score", "physical_activity", "symptom_score", "mri_abnormality", "risk_level"
]

# Drop 'patient_id' since it's not useful for prediction
df = df.drop(columns=["patient_id"])

# Encode categorical variables using Label Encoding
label_encoders = {}
categorical_columns = ["family_history", "smoking", "alcohol", "mri_abnormality", "risk_level"]

for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])  # Convert categories to numbers
    label_encoders[col] = le  # Store the encoder for future decoding

# Split dataset into features and target variable
X = df.drop(columns=["risk_level"])
y = df["risk_level"]

# Split dataset into training (80%) and testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest Model (without optimization)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model and encoders
joblib.dump(model, "random_forest_categorical.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")

# Model Accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print(f"Model Accuracy: {accuracy:.2f}")
print("Classification Report:\n", classification_rep)
