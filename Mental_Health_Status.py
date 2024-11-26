# Step 1: Import Libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Step 2: Load Data
data = pd.read_csv('cleaned_dataset.csv')  # Adjust path as necessary

# Step 3: Preprocessing
age_mapping = {'18-21': 0, '22-25': 1, 'Above 26': 2}
data['Age'] = data['Age'].map(age_mapping)
data.fillna(data.median(), inplace=True)

# Step 4: Select Features and Target
X = data[['Age', 'Sex', 'Scholorship Type', 'Weekly Study Hours', 'Sports Activity']]
y = data['Expected Grade in Graduation']

# Step 5: Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 6: Train Model
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Step 7: Evaluate Model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Step 8: Save Model
joblib.dump(model, 'mental_health_model.pkl')
print("Model saved as 'mental_health_model.pkl'")

