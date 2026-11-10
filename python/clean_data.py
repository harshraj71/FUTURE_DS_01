
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_FILE = BASE_DIR / "data" / "raw" / "Sample_Superstore.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load the raw dataset
df = pd.read_csv(RAW_FILE, encoding="latin1")

print("\n========== ORIGINAL DATASET ==========")
print("Rows and columns:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())

# 2. Check data quality
print("\n========== DATA QUALITY CHECK ==========")
print("Missing values:\n", df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())

# 3. Remove duplicate records
df = df.drop_duplicates()

# 4. Convert date columns
df["Order Date"] = pd.to_datetime(
    df["Order Date"], errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"], errors="coerce"
)

# 5. Convert numeric columns
numeric_columns = [
    "Sales", "Quantity", "Discount", "Profit"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column], errors="coerce"
    )

# 6. Remove rows with invalid essential values
essential_columns = [
    "Order Date", "Sales", "Profit",
    "Quantity", "Category", "Region"
]

df = df.dropna(subset=essential_columns)

# 7. Create additional analytical columns
df["Order Year"] = df["Order Date"].dt.year
df["Order Month"] = df["Order Date"].dt.month
df["Month Name"] = df["Order Date"].dt.strftime("%B")
df["Year-Month"] = df["Order Date"].dt.strftime("%Y-%m")

# 8. Save cleaned dataset
cleaned_file = OUTPUT_DIR / "superstore_cleaned.csv"
df.to_csv(cleaned_file, index=False)

# 9. Generate a cleaning summary
print("\n========== CLEANING SUMMARY ==========")
print("Final rows:", len(df))
print("Final columns:", len(df.columns))
print("Remaining missing values:", df.isnull().sum().sum())
print("Remaining duplicates:", df.duplicated().sum())
print("Total Sales:", round(df["Sales"].sum(), 2))
print("Total Profit:", round(df["Profit"].sum(), 2))
print("Total Quantity:", df["Quantity"].sum())

print("\nCleaned file saved at:")
print(cleaned_file)
print("\nData cleaning completed successfully!")
