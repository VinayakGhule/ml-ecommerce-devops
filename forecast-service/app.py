from flask import Flask, jsonify
import joblib
import requests
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = joblib.load("model/forecast_model.pkl")

@app.route('/')
def home():
    return "Forecast Service Running"

# Keep existing route
@app.route('/predict')
def predict():
    response = requests.get("http://host.docker.internal:5000/daily-sales")
    data = response.json()["daily_sales"]

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df["day_number"] = (df["date"] - df["date"].min()).dt.days

    last_day = df["day_number"].max()

    predictions = []

    for i in range(1, 8):
        future_day = last_day + i
        predicted_sales = model.predict([[future_day]])[0]

        predictions.append({
            "day_offset": i,
            "predicted_sales": float(predicted_sales)
        })

    return jsonify({"forecast": predictions})

# 👇 ADD THIS (alias route for UI)
@app.route('/forecast')
def forecast():
    return predict()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
