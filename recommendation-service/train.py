import requests
import pandas as pd
import joblib
import os

# Get order data
order_service_url = os.getenv("ORDER_SERVICE_URL", "http://127.0.0.1:5000")
response = requests.get(f"{order_service_url}/orders-data")
orders = response.json()["orders"]

df = pd.DataFrame(orders)

# Create user-product matrix
user_product_matrix = pd.crosstab(df["user_id"], df["product_id"])

# Save matrix
joblib.dump(user_product_matrix, "model/user_product_matrix.pkl")

print("Recommendation model trained and saved!")
