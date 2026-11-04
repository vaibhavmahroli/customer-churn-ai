from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from src.database import Base


class CustomerRecord(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    gender = Column(String)
    tenure = Column(Integer)
    Contract = Column(String)
    MonthlyCharges = Column(Float)
    TotalCharges = Column(Float)


class PredictionRecord(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer)
    prediction = Column(String)
    churn_probability = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())