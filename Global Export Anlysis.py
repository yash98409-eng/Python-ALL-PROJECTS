import numpy as np
import pandas as pd


#DATA CLEAN----



customers = pd.read_csv(
    r"D:\movie\ai_data_analyzer\ai_data_analyzer\Global Export\olist_customers_dataset.csv"
)

geolocation = pd.read_csv(
    r"D:\movie\ai_data_analyzer\ai_data_analyzer\Global Export\olist_geolocation_dataset.csv"
)
order_item= pd.read_csv(
    r"D:\movie\ai_data_analyzer\ai_data_analyzer\Global Export\olist_order_items_dataset.csv"
)
order_payment= pd.read_csv(
    r"D:\movie\ai_data_analyzer\ai_data_analyzer\Global Export\olist_order_payments_dataset.csv"
)
order_review=pd.read_csv(
    r"D:\movie\ai_data_analyzer\ai_data_analyzer\Global Export\olist_order_reviews_dataset.csv"
)
order= pd.read_csv(
    r"D:\movie\ai_data_analyzer\ai_data_analyzer\Global Export\olist_orders_dataset.csv"
)
product=pd.read_csv(
    r"D:\movie\ai_data_analyzer\ai_data_analyzer\Global Export\olist_products_dataset.csv"
)
seller=pd.read_csv(
    r"D:\movie\ai_data_analyzer\ai_data_analyzer\Global Export\olist_sellers_dataset.csv"
)
translatoin=pd.read_csv(
    r"D:\movie\ai_data_analyzer\ai_data_analyzer\Global Export\product_category_name_translation.csv"
)
print(customers.head())     #1
print(geolocation.head())   #2
print(order_item.head())    #3
print(order_payment.head()) #4
print(order_review.head())  #5
print(order.head())         #6
print(product.head())       #7
print(seller.head())        #8
print(translatoin.head())   #9


tables = {
    "customers": customers,
    "geolocation": geolocation,
    "orders": order,
    "order_items": order_item,
    "payments": order_payment,
    "products": product,
    "order_review":order_review,
    "seller": seller,
    "translatoin":translatoin,
}

for name, df in tables.items():
    print("\n====================")
    print(name)
    print("====================")
    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    print("Missing:", df.isnull().sum())
    print("Duplicates:", df.duplicated().sum())
    print(df.describe())


print("ORDERS")
print(order.isnull().sum())

print("\nPRODUCTS")
print(product.isnull().sum())

print("\nREVIEWS")
print(order_review.isnull().sum())

# show duplactae and missing value

print("\n order deleted")
print(order.duplicated())


print("\n missing and duplicat evalue ")

print("\n products deleted")
print(product.duplicated())

print("\n REVIEWS deleted")
print(order_review.duplicated())

# dupcate remove
print("\nOrders duplicates:")
print(order.duplicated().sum())

print("\nProducts duplicates:")
print(product.duplicated().sum())

print("\nReviews duplicates:")
print(order_review.duplicated().sum())


# 1. Remove duplicate geolocation rows
geolocation = geolocation.drop_duplicates()


# 2. Convert order dates
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_columns:
    order[col] = pd.to_datetime(order[col], errors="coerce")


# 3. Product category
product["product_category_name"] = product[
    "product_category_name"
].fillna("unknown")


# 4. Product numerical columns
numeric_cols = [
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]

for col in numeric_cols:
    product[col] = product[col].fillna(product[col].median())


# 5. Reviews
order_review["review_comment_title"] = (
    order_review["review_comment_title"]
    .fillna("No Title")
)

order_review["review_comment_message"] = (
    order_review["review_comment_message"]
    .fillna("No Comment")
)


print("===== FINAL CHECK =====")

print("\nOrders:")
print(order.isnull().sum())

print("\nProducts:")
print(product.isnull().sum())

print("\nReviews:")
print(order_review.isnull().sum())

print("\nGeolocation duplicates:")
print(geolocation.duplicated().sum())

customers.to_csv("clean_customers.csv", index=False)
geolocation.to_csv("clean_geolocation.csv", index=False)
order.to_csv("clean_orders.csv", index=False)
order_item.to_csv("clean_order_items.csv", index=False)
order_payment.to_csv("clean_payments.csv", index=False)
order_review.to_csv("clean_reviews.csv", index=False)
product.to_csv("clean_products.csv", index=False)
seller.to_csv("clean_sellers.csv", index=False)
translatoin.to_csv("clean_translation.csv", index=False)
print("All cleaned files saved successfully!")



#misssing value & duplicates

# ====================
# customers
# ====================
# Shape: (99441, 5)
# Columns: ['customer_id', 'customer_unique_id', 'customer_zip_code_prefix', 'customer_city', 'customer_state']
# Missing: 0
# Duplicates: 0

# ====================
# geolocation
# ====================
# Shape: (1000163, 5)
# Columns: ['geolocation_zip_code_prefix', 'geolocation_lat', 'geolocation_lng', 'geolocation_city', 'geolocation_state']
# Missing: 0
# Duplicates: 261831

# ====================
# orders
# ====================
# Shape: (99441, 8)
# Columns: ['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']
# Missing: 4908
# Duplicates: 0

# ====================
# order_items
# ====================
# Shape: (112650, 7)
# Columns: ['order_id', 'order_item_id', 'product_id', 'seller_id', 'shipping_limit_date', 'price', 'freight_value']
# Missing: 0
# Duplicates: 0

# ====================
# payments
# ====================
# Shape: (103886, 5)
# Columns: ['order_id', 'payment_sequential', 'payment_type', 'payment_installments', 'payment_value']
# Missing: 0
# Duplicates: 0

# ====================
# products
# ====================
# Shape: (32951, 9)
# Columns: ['product_id', 'product_category_name', 'product_name_lenght', 'product_description_lenght', 'product_photos_qty', 'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']
# Missing: 2448
# Duplicates: 0

# ====================
# order_review
# ====================
# Shape: (99224, 7)
# Columns: ['review_id', 'order_id', 'review_score', 'review_comment_title', 'review_comment_message', 'review_creation_date', 'review_answer_timestamp']
# Missing: 145903
# Duplicates: 0

# ====================
# seller
# ====================
# Shape: (3095, 4)
# Columns: ['seller_id', 'seller_zip_code_prefix', 'seller_city', 'seller_state']
# Missing: 0
# Duplicates: 0

# ====================
# translatoin
# ====================
# Shape: (71, 2)
# Columns: ['product_category_name', 'product_category_name_english']
# Missing: 0
# Duplicates: 0




