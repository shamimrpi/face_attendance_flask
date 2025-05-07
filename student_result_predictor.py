import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Create DataFrame
df = pd.read_csv("dataset/students_result.csv")

# Categorical column encode করুন
df['Parent_Education'] = df['Parent_Education'].map({'HighSchool': 0, 'Graduate': 1})

# Features এবং Target আলাদা করুন
X = df[['Attendance', 'Study_Hours', 'Previous_Result', 'Parent_Education']]
y = df['Pass']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, y_pred))

# Save trained model
joblib.dump(model, 'trained_student_model.pkl')

# Predict new student result using the trained model
new_student = [[80, 2, 68, 1]]  # [Attendance, Study_Hours, Previous_Result, Parent_Education]
prediction = model.predict(new_student)
print("New Student Pass Prediction (1=Pass, 0=Fail):", prediction[0])

# If you want to load and make prediction using the saved model
loaded_model = joblib.load('trained_student_model.pkl')
loaded_prediction = loaded_model.predict(new_student)
print("Loaded Model Prediction:", loaded_prediction[0])
