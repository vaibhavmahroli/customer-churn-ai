import pandas as pd

# Load original dataset
df = pd.read_csv("data/raw/Telco-Customer-Churn.csv")

print("DATA CLEANING")
print("-------------")

# Check data types
print("\nColumn Data Types:")
print(df.dtypes)

# Convert TotalCharges into numeric values
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"], errors="coerce"
)

# Check missing values again
print("\nMissing Values After Conversion:")
print(df.isnull().sum())

# Count missing TotalCharges
print("\nMissing TotalCharges:")
print(df["TotalCharges"].isnull().sum())

# Display affected customers
print("\nCustomers With Missing TotalCharges:")
print(df[df["TotalCharges"].isnull()][["tenure", "TotalCharges"]])
# Fill missing TotalCharges with 0
df["TotalCharges"] = df["TotalCharges"].fillna(0)

# Verify missing values
print("\nMissing Values After Cleaning:")
print(df.isnull().sum().sum())

# Save cleaned dataset
import os

os.makedirs("data/processed", exist_ok=True)

df.to_csv("data/processed/cleaned_churn.csv", index=False)

print("\nCleaned dataset saved successfully!")
print("Final Dataset Shape:", df.shape)