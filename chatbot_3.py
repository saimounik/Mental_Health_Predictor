import gradio as gr
import joblib
import pandas as pd

# Load the trained model
model = joblib.load("mental_health_model.pkl")

# Define chatbot logic
def chatbot_response(inputs):
    # Extract user inputs
    age, sex, scholarship, study_hours, sports = inputs

    # Map inputs to the correct format
    sex = 1 if sex == "Male" else 0
    scholarship = 1 if scholarship == "Yes" else 0
    sports = 1 if sports == "Yes" else 0

    # Prepare data and predict
    input_data = pd.DataFrame([[
        age, sex, scholarship, study_hours, sports
    ]], columns=["Age", "Sex", "Scholorship Type", "Weekly Study Hours", "Sports Activity"])

    prediction = model.predict(input_data)[0]
    messages = {
        1: "Grade 1: Normal. Keep maintaining your health and study habits! 😊",
        2: "Grade 2: Slightly at risk. Consider improving your routine. 🧘",
        3: "Grade 3: Moderate risk. Focus on improving mental and physical health. 🏋️",
        4: "Grade 4: High risk. Seek guidance from a professional. 🩺"
    }

    # Return the result message
    return f"✅ Predicted Grade: {prediction}. {messages.get(prediction)}"

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# 🧠 Mental Health Prediction Chatbot")
    gr.Markdown("Welcome! Please provide the following details to predict your mental health grade.")

    # Input fields
    with gr.Row():
        age = gr.Slider(18, 100, step=1, label="Age", value=20)
        study_hours = gr.Slider(0, 100, step=1, label="Weekly Study Hours", value=10)

    with gr.Row():
        sex = gr.Radio(["Male", "Female"], label="Gender", value="Male")
        scholarship = gr.Radio(["Yes", "No"], label="Do you have a scholarship?", value="No")
        sports = gr.Radio(["Yes", "No"], label="Do you participate in sports?", value="Yes")

    # Output field
    output = gr.Textbox(label="Prediction Result", interactive=False)

    # Predict button
    predict_btn = gr.Button("Predict")
    predict_btn.click(
        chatbot_response,
        inputs=[age, sex, scholarship, study_hours, sports],
        outputs=output
    )

demo.launch()
