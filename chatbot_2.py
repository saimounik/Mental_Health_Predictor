import streamlit as st
import joblib
import pandas as pd

# Load the trained model
model = joblib.load('mental_health_model.pkl')

# Define the input schema
input_schema = ['Age', 'Sex', 'Scholorship Type', 'Weekly Study Hours', 'Sports Activity']

# Mapping predictions to messages
grade_messages = {
    1: "Grade 1: Normal. Keep maintaining your health and study habits!",
    2: "Grade 2: Slightly at risk. Consider improving your routine and stress management.",
    3: "Grade 3: Moderate risk. Try to focus on improving your mental and physical health.",
    4: "Grade 4: High risk. It is highly recommended to seek guidance from a professional."
}

# Streamlit UI
st.title("Mental Health Prediction Chatbot")
st.write("This chatbot predicts mental health grades based on your inputs. Simply provide the required details below.")

# Sidebar for contact information
st.sidebar.title("Mental Health Status Predictor by")
st.sidebar.write("Sai Mounik Kamisetty")
st.sidebar.write("kamsiettys@mail.sacredheart.edu")
st.sidebar.write("BUAN-690")

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
    predicted_grade = prediction[0]

    # Display the grade and message
    st.success(f"Predicted Grade: {predicted_grade}")
    st.info(grade_messages.get(predicted_grade, "No message available for this grade."))