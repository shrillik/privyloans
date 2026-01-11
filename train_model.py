import warnings
warnings.filterwarnings('ignore')

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

print("Loading data from train.csv...")
data = pd.read_csv('train.csv')
print("Columns found in CSV:", data.columns.tolist())

# Drop missing values for simplicity
data = data.dropna()

# One-hot encode Employment_Status (creates Employment_Status_Unemployed)
data = pd.get_dummies(data, columns=['Employment_Status'], drop_first=True)

# Feature columns and target
features = [
    'Age',
    'Income',
    'Credit_Score',
    'Loan_Amount',
    'Loan_Term',
    'Employment_Status_Unemployed'
]
X = data[features]
y = data['Loan_Approved']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train / test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Logistic Regression with balanced classes
print("Training model...")
model = LogisticRegression(max_iter=1500, class_weight='balanced')
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {acc:.2f}")

# Save model and scaler
joblib.dump(model, 'loan_model.joblib')
joblib.dump(scaler, 'scaler.joblib')
print("Saved 'loan_model.joblib' and 'scaler.joblib'")
