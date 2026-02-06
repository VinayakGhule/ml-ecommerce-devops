from flask import Flask, jsonify
import joblib
import requests
import pandas as pd

app = Flask(__name__)

# Load trained model
model = joblib.load("model/forecast_model.pkl")

@app.route('/')
def home():
    return "Forecast Service Running"

@app.route('/predict')
def predict():
    # Get latest daily sales data
    response = requests.get("http://host.docker.internal:5000/daily-sales")
    data = response.json()["daily_sales"]

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df["day_number"] = (df["date"] - df["date"].min()).dt.days

    last_day = df["day_number"].max()

    predictions = []

    # Predict next 7 days
    for i in range(1, 8):
        future_day = last_day + i
        predicted_sales = model.predict([[future_day]])[0]

        predictions.append({
            "day_offset": i,
            "predicted_sales": float(predicted_sales)
        })

    return jsonify({"forecast": predictions})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)

