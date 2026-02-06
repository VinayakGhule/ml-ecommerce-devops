import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Get data from order service
response = requests.get("http://127.0.0.1:5000/daily-sales")
data = response.json()["daily_sales"]

df = pd.DataFrame(data)

# Convert date to number
df["date"] = pd.to_datetime(df["date"])
df["day_number"] = (df["date"] - df["date"].min()).dt.days

X = df[["day_number"]]
y = df["sales"]

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
joblib.dump(model, "model/forecast_model.pkl")

print("Model trained and saved!")
