import streamlit as st
import pandas as pd
import joblib
import scipy.stats as s

# Load the saved Gaussian parameters
(mu_0, sigma_0, mu_1, sigma_1, strong_features) = joblib.load("gaussian_parameters.pkl")

# Streamlit UI
st.title("🩺 Breast Cancer Diagnosis Predictor")
st.write("Upload a CSV file with tumor data to predict whether it's benign (0) or malignant (1).")

# File uploader widget
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    data = pd.read_csv(uploaded_file)
    st.write("📊 Uploaded Data Preview:", data.head())

    # Preprocess the data: Remove unnecessary columns
    if "Unnamed: 32" in data.columns:
        data = data.drop(columns=["Unnamed: 32"])
    if "id" in data.columns:
        data = data.drop(columns=["id"])

    # (Optional) Select only the relevant features (same as used in training)
    # If required, replace the below list with your actual selected features.
    
    
    data = data[strong_features]

    # Compute Gaussian probabilities for each class
    p_class1 = s.multivariate_normal.pdf(data, mu_1, sigma_1)
    p_class0 = s.multivariate_normal.pdf(data, mu_0, sigma_0)

    # Make predictions: If probability for class 1 is higher, predict 1; else predict 0
    predictions = (p_class1 > p_class0).astype(int)

    st.subheader("🔍 Prediction Results")
    st.write("**0 = Benign, 1 = Malignant**")
    st.write(predictions)
