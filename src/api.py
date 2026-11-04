from sqlalchemy.orm import Session
from fastapi import Depends

from src.database import SessionLocal, Base, engine
from src.models import CustomerRecord, PredictionRecord

from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create FastAPI application
app = FastAPI(
    title="Customer Churn Prediction API",
    description="AI-powered customer churn prediction",
    version="1.0"
)
@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables checked/created successfully")
    
# Load trained ML model
model = joblib.load("models/churn_model.pkl")


# Define customer data structure
class Customer(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Customer Churn Prediction API is running!"
    }


# Prediction endpoint

@app.post("/predict")
def predict_churn(
    customer: Customer,
    db: Session = Depends(get_db)
):
    customer_data = pd.DataFrame([customer.model_dump()])

    prediction = model.predict(customer_data)[0]
    probability = model.predict_proba(customer_data)[0][1]

    # Save customer
    new_customer = CustomerRecord(
        gender=customer.gender,
        tenure=customer.tenure,
        Contract=customer.Contract,
        MonthlyCharges=customer.MonthlyCharges,
        TotalCharges=customer.TotalCharges
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    # Save prediction
    new_prediction = PredictionRecord(
        customer_id=new_customer.id,
        prediction="Churn" if prediction == 1 else "No Churn",
        churn_probability=float(probability)
    )

    db.add(new_prediction)
    db.commit()

    return {
        "customer_id": new_customer.id,
        "prediction": "Churn" if prediction == 1 else "No Churn",
        "churn_probability": round(float(probability), 4),
        "database_status": "Saved successfully"
    }

@app.get("/customers")
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(CustomerRecord).order_by(
        CustomerRecord.id.desc()
    ).all()

    return [
        {
            "id": customer.id,
            "gender": customer.gender,
            "tenure": customer.tenure,
            "contract": customer.Contract,
            "monthly_charges": customer.MonthlyCharges,
            "total_charges": customer.TotalCharges
        }
        for customer in customers
    ]


@app.get("/predictions")
def get_predictions(db: Session = Depends(get_db)):
    predictions = db.query(PredictionRecord).order_by(
        PredictionRecord.id.desc()
    ).all()

    return [
        {
            "id": prediction.id,
            "customer_id": prediction.customer_id,
            "prediction": prediction.prediction,
            "churn_probability": prediction.churn_probability,
            "created_at": (
                prediction.created_at.isoformat()
                if prediction.created_at else None
            )
        }
        for prediction in predictions
    ]
