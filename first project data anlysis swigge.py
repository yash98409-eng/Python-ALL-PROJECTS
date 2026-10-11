
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# 1. Create project folders
Path("outputs/charts").mkdir(parents=True, exist_ok=True)

# 2. Load dataset
# Replace this with your actual Swiggy CSV filename
file_path = "swiggy_orders.csv"

try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print("CSV file not found! Put swiggy_orders.csv in the project folder.")
    raise SystemExit

# 3. Explore data
print("\n--- DATA OVERVIEW ---")
print(df.head())
print("\nShape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nData types:\n", df.dtypes)
print("\nMissing values:\n", df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())
print("\nStatistics:\n", df.describe(include="all"))

# 4. Clean data
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

df = df.drop_duplicates().copy()

# Standardize text values
for col in df.select_dtypes(include=["object"]).columns:
    df[col] = df[col].str.strip()

# Convert common numeric columns if present
for col in ["price", "order_value", "rating", "delivery_time",
            "delivery_time_min", "quantity"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Parse date if available
for col in ["order_date", "date"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

# Save cleaned dataset
df.to_csv("outputs/cleaned_swiggy_data.csv", index=False)

print("\n--- CLEANED DATA ---")
print("Shape:", df.shape)
print("Missing values:\n", df.isnull().sum())

# 5. Automatically identify common columns
def find_col(possible_names):
    for name in possible_names:
        if name in df.columns:
            return name
    return None

city_col = find_col(["city", "location", "area"])
restaurant_col = find_col(["restaurant_name", "restaurant"])
price_col = find_col(["order_value", "price", "amount", "total_amount"])
rating_col = find_col(["rating", "restaurant_rating"])
date_col = find_col(["order_date", "date"])
status_col = find_col(["order_status", "status"])
cuisine_col = find_col(["cuisine", "food_type"])
delivery_col = find_col(["delivery_time_min", "delivery_time"])

# 6. Overall KPIs
print("\n--- BUSINESS KPIs ---")
print("Total records:", len(df))

if price_col:
    print("Total recorded value:", df[price_col].sum())
    print("Average order value:", round(df[price_col].mean(), 2))

if restaurant_col:
    print("Unique restaurants:", df[restaurant_col].nunique())

if city_col:
    print("Unique cities/areas:", df[city_col].nunique())

if rating_col:
    print("Average rating:", round(df[rating_col].mean(), 2))

if status_col:
    print("\nOrder status counts:\n", df[status_col].value_counts())

# 7. City-wise analysis
if city_col:
    if price_col:
        city_analysis = df.groupby(city_col).agg(
            records=(city_col, "size"),
            total_value=(price_col, "sum"),
            average_value=(price_col, "mean")
        ).sort_values("total_value", ascending=False)
    else:
        city_analysis = df[city_col].value_counts().to_frame("records")

    print("\n--- CITY ANALYSIS ---\n", city_analysis)
    city_analysis.to_csv("outputs/city_analysis.csv")

    if price_col:
        city_analysis["total_value"].sort_values().plot(
            kind="barh", figsize=(10, 6), title="Value by City"
        )
        plt.tight_layout()
        plt.savefig("outputs/charts/city_analysis.png")
        plt.show()

# 8. Restaurant analysis
if restaurant_col:
    agg = {restaurant_col: "size"}
    if price_col:
        agg[price_col] = "sum"
    if rating_col:
        agg[rating_col] = "mean"

    restaurant_analysis = df.groupby(restaurant_col).agg(agg)
    restaurant_analysis = restaurant_analysis.rename(
        columns={restaurant_col: "records",
                 price_col: "total_value" if price_col else ""}
    )

    print("\n--- TOP RESTAURANTS ---")
    print(restaurant_analysis.sort_values(
        "records", ascending=False
    ).head(10))

    restaurant_analysis.to_csv("outputs/restaurant_analysis.csv")

# 9. Cuisine analysis
if cuisine_col:
    print("\n--- CUISINE ANALYSIS ---")
    print(df[cuisine_col].value_counts())

    df[cuisine_col].value_counts().plot(
        kind="bar", figsize=(10, 5), title="Popular Cuisines"
    )
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("outputs/charts/cuisine_analysis.png")
    plt.show()

# 10. Rating analysis
if rating_col:
    sns.histplot(df[rating_col].dropna(), bins=10, kde=True)
    plt.title("Rating Distribution")
    plt.tight_layout()
    plt.savefig("outputs/charts/rating_distribution.png")
    plt.show()

# 11. Monthly trend
if date_col and price_col:
    monthly = df.dropna(subset=[date_col]).copy()
    monthly["month"] = monthly[date_col].dt.to_period("M").astype(str)
    monthly_analysis = monthly.groupby("month")[price_col].sum()

    print("\n--- MONTHLY TREND ---\n", monthly_analysis)
    monthly_analysis.to_csv("outputs/monthly_analysis.csv")

    monthly_analysis.plot(
        kind="line", marker="o", figsize=(10, 5),
        title="Monthly Recorded Value"
    )
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("outputs/charts/monthly_trend.png")
    plt.show()

# 12. Delivery time analysis
if delivery_col:
    print("\nAverage delivery time:", df[delivery_col].mean())

    sns.histplot(df[delivery_col].dropna(), bins=15, kde=True)
    plt.title("Delivery Time Distribution")
    plt.tight_layout()
    plt.savefig("outputs/charts/delivery_time.png")
    plt.show()

# 13. Export final report
print("\nAnalysis completed successfully!")
print("Check the outputs folder for cleaned data, reports and charts.")

