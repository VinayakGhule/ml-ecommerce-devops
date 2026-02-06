from flask import Flask, jsonify
import joblib

app = Flask(__name__)

# Load saved matrix
matrix = joblib.load("model/user_product_matrix.pkl")

@app.route('/')
def home():
    return "Recommendation Service Running"

@app.route('/recommend/<int:user_id>')
def recommend(user_id):
    if user_id not in matrix.index:
        return jsonify({"error": "User not found"})

    # Products user already bought
    user_products = matrix.loc[user_id]
    bought_products = user_products[user_products > 0].index.tolist()

    # Find similar users
    similarity_scores = matrix.corrwith(user_products, axis=1).dropna()
    similar_users = similarity_scores.sort_values(ascending=False).index[1:6]

    # Collect products from similar users
    recommended_products = set()
    for sim_user in similar_users:
        sim_user_products = matrix.loc[sim_user]
        recommended_products.update(
            sim_user_products[sim_user_products > 0].index.tolist()
        )

    # Remove already bought products
    recommended_products = list(set(recommended_products) - set(bought_products))

    return jsonify({
        "user_id": user_id,
        "recommended_products": recommended_products[:5]
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002)

