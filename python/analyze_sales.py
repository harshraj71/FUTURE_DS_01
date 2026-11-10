
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "superstore_cleaned.csv"
REPORT_DIR = BASE_DIR / "reports"
CHART_DIR = REPORT_DIR / "charts"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)

# Load cleaned dataset
df = pd.read_csv(INPUT_FILE)

print("\n========== SALES PERFORMANCE ANALYSIS ==========")

# 1. Overall Business Performance
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()
total_quantity = df["Quantity"].sum()
profit_margin = (total_profit / total_sales) * 100

print("\n--- Overall KPIs ---")
print(f"Total Revenue: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Total Quantity Sold: {total_quantity:,}")
print(f"Profit Margin: {profit_margin:.2f}%")

# 2. Category Analysis
category_analysis = (
    df.groupby("Category")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Quantity=("Quantity", "sum")
    )
    .sort_values("Total_Sales", ascending=False)
)

print("\n--- Category Performance ---")
print(category_analysis.round(2))

category_analysis.to_csv(
    REPORT_DIR / "category_analysis.csv"
)

# 3. Regional Analysis
region_analysis = (
    df.groupby("Region")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Quantity=("Quantity", "sum")
    )
    .sort_values("Total_Sales", ascending=False)
)

print("\n--- Regional Performance ---")
print(region_analysis.round(2))

region_analysis.to_csv(
    REPORT_DIR / "region_analysis.csv"
)

# 4. Monthly Sales Analysis
df["Order Date"] = pd.to_datetime(df["Order Date"])

monthly_analysis = (
    df.set_index("Order Date")
    .resample("MS")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum")
    )
)

print("\n--- Monthly Sales Performance ---")
print(monthly_analysis.head(12).round(2))

monthly_analysis.to_csv(
    REPORT_DIR / "monthly_sales_analysis.csv"
)

# 5. Top 10 Products by Revenue
product_analysis = (
    df.groupby("Product Name")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Quantity=("Quantity", "sum")
    )
    .sort_values("Total_Sales", ascending=False)
    .head(10)
)

print("\n--- Top 10 Products by Sales ---")
print(product_analysis.round(2))

product_analysis.to_csv(
    REPORT_DIR / "top_10_products.csv"
)

# 6. Sub-Category Analysis
subcategory_analysis = (
    df.groupby("Sub-Category")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum")
    )
    .sort_values("Total_Profit", ascending=True)
)

print("\n--- Sub-Category Profitability ---")
print(subcategory_analysis.round(2))

subcategory_analysis.to_csv(
    REPORT_DIR / "subcategory_analysis.csv"
)

# 7. Loss-making transactions
loss_transactions = df[df["Profit"] < 0]

print("\n--- Loss Analysis ---")
print("Loss-making transactions:", len(loss_transactions))
print(
    "Total loss from negative-profit records: $",
    round(abs(loss_transactions["Profit"].sum()), 2)
)

# 8. Chart: Monthly Revenue Trend
plt.figure(figsize=(12, 6))
plt.plot(
    monthly_analysis.index,
    monthly_analysis["Total_Sales"],
    marker="o"
)
plt.title("Monthly Sales Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue ($)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig(CHART_DIR / "monthly_sales_trend.png", dpi=300)
plt.close()

# 9. Chart: Sales by Category
plt.figure(figsize=(9, 5))
category_analysis["Total_Sales"].plot(
    kind="bar",
    title="Sales by Product Category"
)
plt.xlabel("Category")
plt.ylabel("Revenue ($)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(CHART_DIR / "category_sales.png", dpi=300)
plt.close()

# 10. Chart: Profit by Region
plt.figure(figsize=(9, 5))
region_analysis["Total_Profit"].plot(
    kind="bar",
    title="Profit by Region"
)
plt.xlabel("Region")
plt.ylabel("Profit ($)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(CHART_DIR / "regional_profit.png", dpi=300)
plt.close()

# 11. Chart: Top 10 Products
plt.figure(figsize=(12, 7))
product_analysis["Total_Sales"].sort_values().plot(
    kind="barh",
    title="Top 10 Products by Revenue"
)
plt.xlabel("Revenue ($)")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig(CHART_DIR / "top_10_products.png", dpi=300)
plt.close()

print("\n========== EDA COMPLETED ==========")
print("Analysis reports saved in:", REPORT_DIR)
print("Charts saved in:", CHART_DIR)
