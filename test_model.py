import joblib
import pandas as pd

# Load the saved model
model = joblib.load('mental_health_model.pkl')

# Define the input with feature names
test_input = pd.DataFrame([[20, 1, 1, 15, 1]], columns=['Age', 'Sex', 'Scholorship Type', 'Weekly Study Hours', 'Sports Activity'])

# Make a prediction
prediction = model.predict(test_input)
print("Predicted Grade:", prediction[0])


# Multiple test inputs
test_inputs = pd.DataFrame([
    [20, 1, 1, 15, 1],  # Input 1
    [22, 0, 0, 10, 0],  # Input 2
    [18, 1, 0, 20, 1]   # Input 3
], columns=['Age', 'Sex', 'Scholorship Type', 'Weekly Study Hours', 'Sports Activity'])

# Predict grades for multiple inputs
predictions = model.predict(test_inputs)
print("Predicted Grades:", predictions)



