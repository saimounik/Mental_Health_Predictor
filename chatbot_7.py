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

# Prediction messages and tips
grade_messages = {
    1: "Level 1: Normal. Keep maintaining your health and study habits! 😊",
    2: "Level 2: Slightly at risk. Consider improving your routine and stress management. 🧘",
    3: "Level 3: Moderate risk. Try to focus on improving your mental and physical health. 🏋️",
    4: "Level 4: High risk. It is highly recommended to seek guidance from a professional. 🩺"
}
grade_tips = {
    1: ["💡 Maintain a consistent daily routine.", "📚 Engage in positive activities like reading and exercising."],
    2: ["💡 Start daily mindfulness or meditation.", "📋 Plan your study schedule to reduce stress.", "🍎 Maintain a healthy diet."],
    3: ["💡 Join a peer support group.", "📅 Schedule regular breaks during study sessions.", "🏋️ Include physical activity to reduce stress."],
    4: ["💡 Seek support from a mental health counselor.", "📞 Contact your university's wellness services.", "🌟 Remember, seeking help is a strength."]
}

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

# Function to render chat bubbles
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
                <div style="background-color: #951C95; color: #FFFFFF; 
                            padding: 10px; border-radius: 10px; 
                            margin: 5px 0; max-width: 70%; 
                            margin-left: auto; text-align: right;">
                    <b>You:</b> {message['text']}
                </div>
            """, unsafe_allow_html=True)

# Display the chat log
st.title("Mental Health Prediction Chatbot")
render_chat()

# Sidebar for contact information
st.sidebar.title("Mental Health Chatbot Info")
st.sidebar.write("**Name:** Sai Mounik Kamisetty")
st.sidebar.write("**Email:** kamisettys@mail.sacredheart.edu")
st.sidebar.write("**Section:** BUAN-690")

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
    st.session_state.chat_log.append({"sender": "Bot", "text": f"Predicted Level: {prediction}. {grade_messages.get(prediction)}"})
    st.success(f"Predicted Mental Health Status Level: {prediction}")
    st.info(grade_messages.get(prediction, "No message available for this level."))

    # Display additional tips
    if prediction in grade_tips:
        st.markdown("### Additional Tips:")
        for tip in grade_tips[prediction]:
            st.write(tip)

    # Add wellness center contact information
    st.markdown(
        """
        ---
        **If you still feel bad or need additional support, please reach out to:**
        - **Maureen Hamilton Wellness Center, Sacred Heart University**
        - **Address:** Wellness Center, 4980 Park Avenue, Fairfield, CT
        - **Email:** [counselingcenter@sacredheart.edu](mailto:counselingcenter@sacredheart.edu)
        - **Phone:** 203-371-7955
        ---
        """
    )

    # Reset option
    if st.button("Restart"):
        st.session_state.responses = {}
        st.session_state.current_question = 0
        st.session_state.chat_log = []
