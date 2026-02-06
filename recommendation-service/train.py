import requests
import pandas as pd
import joblib

# Get order data
response = requests.get("http://host.docker.internal:5000/orders-data")
orders = response.json()["orders"]

df = pd.DataFrame(orders)

# Create user-product matrix
user_product_matrix = pd.crosstab(df["user_id"], df["product_id"])

# Save matrix
joblib.dump(user_product_matrix, "model/user_product_matrix.pkl")

print("Recommendation model trained and saved!")
