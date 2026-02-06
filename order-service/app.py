from flask import Flask, jsonify
from config import get_db_connection
from faker import Faker
import random
from datetime import datetime, timedelta

app = Flask(__name__)
fake = Faker()

@app.route('/')
def home():
    return "Order Service + PostgreSQL Connected!"

@app.route('/generate-data')
def generate_data():
    conn = get_db_connection()
    cur = conn.cursor()

    # Insert Users
    for _ in range(50):
        name = fake.name()
        cur.execute("INSERT INTO users (name) VALUES (%s)", (name,))

    # Insert Products
    products = []
    for i in range(20):
        product_name = f"Product_{i+1}"
        price = round(random.uniform(100, 1000), 2)
        cur.execute(
            "INSERT INTO products (name, price) VALUES (%s, %s) RETURNING id",
            (product_name, price)
        )
        product_id = cur.fetchone()[0]
        products.append(product_id)

    # Get all user IDs
    cur.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cur.fetchall()]

    # Insert Orders
    for _ in range(500):
        user_id = random.choice(user_ids)
        product_id = random.choice(products)
        quantity = random.randint(1, 5)

        # Random date in last 60 days
        random_days = random.randint(0, 60)
        order_date = datetime.now() - timedelta(days=random_days)

        cur.execute(
            """
            INSERT INTO orders (user_id, product_id, quantity, order_date)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, product_id, quantity, order_date)
        )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Dummy data generated successfully!"})

@app.route('/sales-summary')
def sales_summary():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM orders")
    total_orders = cur.fetchone()[0]

    cur.execute("""
        SELECT SUM(o.quantity * p.price)
        FROM orders o
        JOIN products p ON o.product_id = p.id
    """)
    total_revenue = cur.fetchone()[0] or 0

    cur.execute("""
        SELECT p.name, SUM(o.quantity) AS total_sold
        FROM orders o
        JOIN products p ON o.product_id = p.id
        GROUP BY p.name
        ORDER BY total_sold DESC
        LIMIT 5
    """)
    top_products = cur.fetchall()

    cur.close()
    conn.close()

    return {
        "total_orders": total_orders,
        "total_revenue": float(total_revenue),
        "top_products": [
            {"name": row[0], "quantity_sold": row[1]}
            for row in top_products
        ]
    }


@app.route('/daily-sales')
def daily_sales():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT DATE(order_date) as day,
               SUM(o.quantity * p.price) as total_sales
        FROM orders o
        JOIN products p ON o.product_id = p.id
        GROUP BY day
        ORDER BY day
    """)

    results = cur.fetchall()

    cur.close()
    conn.close()

    data = []
    for row in results:
        data.append({
            "date": str(row[0]),
            "sales": float(row[1])
        })

    return {"daily_sales": data}



@app.route('/orders-data')
def orders_data():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id, product_id
        FROM orders
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    data = [
        {"user_id": r[0], "product_id": r[1]}
        for r in rows
    ]

    return {"orders": data}





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
