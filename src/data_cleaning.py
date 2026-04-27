import pandas as pd
import numpy as np

# Load data
df = pd.read_csv("Data/raw/houses_with_pool.csv")

print("=" * 60)
print("START DATA CLEANING")
print("=" * 60)

# ---------------------------
# 1. Remove duplicates
# ---------------------------
df = df.drop_duplicates()

# ---------------------------
# 2. Fix Missing Values
# ---------------------------

# PoolQuality (categorical → use mode NOT median)
df["PoolQuality"] = df["PoolQuality"].fillna(df["PoolQuality"].mode()[0])

# PoolType
df["PoolType"] = df["PoolType"].fillna("None")

# ---------------------------
# 3. Fix Logical Consistency
# ---------------------------

# If no pool → force values
df.loc[df["HasPool"] == "No", ["PoolArea",
                               "PoolType", "PoolQuality"]] = [0, "None", "None"]

# If has pool but area = 0 → fix
df.loc[(df["HasPool"] == "Yes") & (df["PoolArea"] == 0),
       "PoolArea"] = df["PoolArea"].median()

# ---------------------------
# 4. Convert Data Types
# ---------------------------
numeric_cols = [
    "Area",
    "Bedrooms",
    "Bathrooms",
    "Floors",
    "YearBuilt",
    "Price",
    "PoolArea"]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ---------------------------
# 5. Remove Invalid Values
# ---------------------------
df = df[(df["Area"] > 0) & (df["Price"] > 0)]

# ---------------------------
# 6. Handle Outliers (IQR)
# ---------------------------


def remove_outliers(data, col):
    Q1 = data[col].quantile(0.25)
    Q3 = data[col].quantile(0.75)
    IQR = Q3 - Q1
    return data[(data[col] >= Q1 - 1.5 * IQR) & (data[col] <= Q3 + 1.5 * IQR)]


df = remove_outliers(df, "Price")
df = remove_outliers(df, "Area")

# ---------------------------
# 7. Clean Categorical Values
# ---------------------------
cat_cols = [
    "Location",
    "Condition",
    "Garage",
    "HasPool",
    "PoolQuality",
    "PoolType"]

for col in cat_cols:
    df[col] = df[col].astype(str).str.strip().str.capitalize()

# ---------------------------
# 8. Final Checks
# ---------------------------
print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

print("\nInconsistencies Check:")
print(df[(df["HasPool"] == "No") & (df["PoolArea"] > 0)])

# ---------------------------
# 9. Reset Index
# ---------------------------
df = df.reset_index(drop=True)

# ---------------------------
# 10. Save Clean Data
# ---------------------------
df.to_csv("Data/processed/clean_data_final.csv", index=False)

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETED SUCCESSFULLY ✅")
print(f"Final Shape: {df.shape}")
print("=" * 60)
