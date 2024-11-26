import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load("mental_health_model.pkl")

# Define questions and their options
questions = [
    {"key": "age", "text": "Hello! Let's predict your mental health status. How old are you?"},
    {"key": "sex", "text": "What's your gender? (Male/Female)", "options": ["Male", "Female"]},
    {"key": "scholarship", "text": "Do you have a scholarship? (Yes/No)", "options": ["Yes", "No"]},
    {"key": "study_hours", "text": "How many hours do you study weekly?"},
    {"key": "sports", "text": "Do you participate in sports? (Yes/No)", "options": ["Yes", "No"]}
]

# Initialize session state
if "responses" not in st.session_state:
    st.session_state.responses = {}
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# Helper function to move to the next question
def next_question():
    st.session_state.current_question += 1

# Function to render chat bubbles with AI-themed colors
def render_chat():
    for message in st.session_state.chat_log:
        if message["sender"] == "Bot":
            st.markdown(f"""
                <div style="background-color: #226b6a; color: #FFFFFF; 
                            padding: 10px; border-radius: 10px; 
                            margin: 5px 0; max-width: 70%;">
                    <b>Bot:</b> {message['text']}
                </div>
            """, unsafe_allow_html=True)
        elif message["sender"] == "User":
            st.markdown(f"""
                <div style="background-color: #FD3DB5; color: #FFFFFF; 
                            padding: 10px; border-radius: 10px; 
                            margin: 5px 0; max-width: 70%; 
                            margin-left: auto; text-align: right;">
                    <b>You:</b> {message['text']}
                </div>
            """, unsafe_allow_html=True)

# Display the chat log
st.title("Mental Health Prediction Chatbot")
render_chat()

# Display the current question
if st.session_state.current_question < len(questions):
    question = questions[st.session_state.current_question]
    st.markdown(f"**Bot:** {question['text']}")

    # Input based on question type
    if "options" in question:
        response = st.radio("Your response:", question["options"], key=question["key"])
    else:
        response = st.text_input("Your response:", key=question["key"])

    # Submit button
    if st.button("Submit"):
        if response:
            st.session_state.responses[question["key"]] = response
            st.session_state.chat_log.append({"sender": "User", "text": response})
            st.session_state.chat_log.append({"sender": "Bot", "text": question["text"]})
            next_question()
        else:
            st.warning("Please provide a response.")
else:
    # All questions answered, make prediction
    st.markdown("**Bot:** Thank you for answering all the questions. Let me predict your mental health status.")

    # Prepare input data for the model
    age = int(st.session_state.responses["age"])
    sex = 1 if st.session_state.responses["sex"] == "Male" else 0
    scholarship = 1 if st.session_state.responses["scholarship"] == "Yes" else 0
    study_hours = int(st.session_state.responses["study_hours"])
    sports = 1 if st.session_state.responses["sports"] == "Yes" else 0

    input_data = pd.DataFrame([[age, sex, scholarship, study_hours, sports]],
                               columns=["Age", "Sex", "Scholorship Type", "Weekly Study Hours", "Sports Activity"])

    # Make prediction
    prediction = model.predict(input_data)[0]
    grade_messages = {
        1: "Level 1: Normal. Keep maintaining your health and study habits! 😊",
        2: "Level 2: Slightly at risk. Consider improving your routine and stress management. 🧘",
        3: "Level 3: Moderate risk. Try to focus on improving your mental and physical health. 🏋️",
        4: "Level 4: High risk. It is highly recommended to seek guidance from a professional. 🩺"
    }
    st.session_state.chat_log.append({"sender": "Bot", "text": f"Predicted Level: {prediction}. {grade_messages.get(prediction)}"})
    st.success(f"Predicted Mental Health Status Level: {prediction}")
    st.info(grade_messages.get(prediction, "No message available for this level."))

    # Reset option
    if st.button("Restart"):
        st.session_state.responses = {}
        st.session_state.current_question = 0
        st.session_state.chat_log = []
