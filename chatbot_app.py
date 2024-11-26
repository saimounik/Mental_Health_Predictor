import streamlit as st
import joblib
import pandas as pd

# Load the trained model
model = joblib.load('mental_health_model.pkl')

# Define the input schema
input_schema = ['Age', 'Sex', 'Scholorship Type', 'Weekly Study Hours', 'Sports Activity']

# Streamlit UI
st.title("Mental Health Prediction Chatbot")
st.write("Answer the following questions to predict the grade:")

# Collect user inputs
age = st.number_input("Enter your age:", min_value=18, max_value=100, step=1)
sex = st.selectbox("Select your gender:", ["Male", "Female"])
scholarship = st.selectbox("Do you have a scholarship?", ["Yes", "No"])
study_hours = st.number_input("Enter weekly study hours:", min_value=0, max_value=100, step=1)
sports = st.selectbox("Do you participate in sports?", ["Yes", "No"])

# Map inputs to numeric values
sex = 1 if sex == "Male" else 0
scholarship = 1 if scholarship == "Yes" else 0
sports = 1 if sports == "Yes" else 0

# Predict button
if st.button("Predict"):
    # Prepare the input data
    input_data = pd.DataFrame([[age, sex, scholarship, study_hours, sports]], columns=input_schema)

    # Make a prediction
    prediction = model.predict(input_data)
    st.success(f"Predicted Grade: {prediction[0]}")
