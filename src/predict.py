
import pandas as pd
import joblib

# Load the trained model
model = joblib.load("models/churn_model.pkl")

# Sample customer details
customer = {
    "gender": "Male",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 5,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "Yes",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 89.50,
    "TotalCharges": 450.00
}

# Convert customer data into a DataFrame
customer_df = pd.DataFrame([customer])

# Make prediction
prediction = model.predict(customer_df)[0]

# Calculate churn probability
probability = model.predict_proba(customer_df)[0][1]

# Display result
print("\n--- Customer Churn Prediction ---")

if prediction == 1:
    print("Prediction: Customer is likely to CHURN")
else:
    print("Prediction: Customer is likely to STAY")

print(f"Churn Probability: {probability:.2%}")
