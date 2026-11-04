import pandas as pd

# Load customer dataset
df = pd.read_csv("data/raw/Telco-Customer-Churn.csv")

print("CUSTOMER CHURN PROJECT")
print("----------------------")

# Dataset information
print("\nDataset Shape:")
print(df.shape)

# First five customers
print("\nFirst 5 Customers:")
print(df.head())

# Column information
print("\nDataset Columns:")
print(df.columns.tolist())

# Missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Churn distribution
print("\nChurn Distribution:")
print(df["Churn"].value_counts())

print("\nDay 1 setup completed!")