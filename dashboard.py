
import streamlit as st
import requests
import pandas as pd

# Dashboard configuration
st.set_page_config(
    page_title="Customer Churn AI",
    page_icon="📊",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

st.title("📊 Customer Churn Prediction Dashboard")
st.write("AI-powered customer churn analysis")

# Fetch data from FastAPI
try:
    customers_response = requests.get(
        f"{API_URL}/customers",
        timeout=5
    )
    predictions_response = requests.get(
        f"{API_URL}/predictions",
        timeout=5
    )

    customers_response.raise_for_status()
    predictions_response.raise_for_status()

    customers = customers_response.json()
    predictions = predictions_response.json()

    # Calculate dashboard statistics
    total_customers = len(customers)
    total_predictions = len(predictions)

    churn_count = sum(
        1 for p in predictions
        if p["prediction"] == "Churn"
    )

    no_churn_count = total_predictions - churn_count

    avg_probability = (
        sum(p["churn_probability"] for p in predictions)
        / total_predictions
        if total_predictions else 0
    )

    # Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", total_customers)
    col2.metric("Total Predictions", total_predictions)
    col3.metric("Churn Predictions", churn_count)
    col4.metric("Average Churn Probability", f"{avg_probability:.2%}")

    st.divider()

    # Prediction history
    st.subheader("Customer Prediction History")

    if predictions:
        df = pd.DataFrame(predictions)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No predictions available yet.")

    # Customer records
    st.subheader("Customer Records")

    if customers:
        customer_df = pd.DataFrame(customers)
        st.dataframe(customer_df, use_container_width=True)
    else:
        st.info("No customer records available.")

except requests.exceptions.RequestException as error:
    st.error("Cannot connect to FastAPI.")
    st.write("Please start your FastAPI server first.")
    st.code(str(error))


st.divider()

st.header("🔍 Predict Customer Churn")
st.write("Enter customer details to predict the likelihood of churn.")

with st.form("customer_prediction_form"):

    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        senior = st.selectbox("Senior Citizen", [0, 1])
        partner = st.selectbox("Partner", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["Yes", "No"])
        tenure = st.number_input("Tenure (months)", 0, 72, 5)
        phone = st.selectbox("Phone Service", ["Yes", "No"])
        multiple = st.selectbox(
            "Multiple Lines", ["Yes", "No", "No phone service"]
        )
        internet = st.selectbox(
            "Internet Service", ["DSL", "Fiber optic", "No"]
        )
        security = st.selectbox(
            "Online Security", ["Yes", "No", "No internet service"]
        )
        backup = st.selectbox(
            "Online Backup", ["Yes", "No", "No internet service"]
        )

    with col2:
        device = st.selectbox(
            "Device Protection", ["Yes", "No", "No internet service"]
        )
        support = st.selectbox(
            "Tech Support", ["Yes", "No", "No internet service"]
        )
        tv = st.selectbox(
            "Streaming TV", ["Yes", "No", "No internet service"]
        )
        movies = st.selectbox(
            "Streaming Movies", ["Yes", "No", "No internet service"]
        )
        contract = st.selectbox(
            "Contract",
            ["Month-to-month", "One year", "Two year"]
        )
        paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
            ]
        )
        monthly = st.number_input(
            "Monthly Charges", min_value=0.0, value=89.50
        )
        total = st.number_input(
            "Total Charges", min_value=0.0, value=450.0
        )

    submitted = st.form_submit_button(
        "Predict Churn",
        use_container_width=True
    )

    if submitted:
        customer_data = {
            "gender": gender,
            "SeniorCitizen": senior,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "PhoneService": phone,
            "MultipleLines": multiple,
            "InternetService": internet,
            "OnlineSecurity": security,
            "OnlineBackup": backup,
            "DeviceProtection": device,
            "TechSupport": support,
            "StreamingTV": tv,
            "StreamingMovies": movies,
            "Contract": contract,
            "PaperlessBilling": paperless,
            "PaymentMethod": payment,
            "MonthlyCharges": monthly,
            "TotalCharges": total
        }

        try:
            response = requests.post(
                f"{API_URL}/predict",
                json=customer_data,
                timeout=15
            )

            response.raise_for_status()
            result = response.json()

            st.subheader("Prediction Result")

            if result["prediction"] == "Churn":
                st.error("Customer is likely to CHURN")
            else:
                st.success("Customer is likely to STAY")

            st.metric(
                "Churn Probability",
                f"{result['churn_probability']:.2%}"
            )

            st.write("Customer ID:", result["customer_id"])
            st.success(result["database_status"])

        except requests.exceptions.RequestException as error:
            st.error(f"Prediction failed: {error}")
