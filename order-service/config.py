import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        host="host.docker.internal",
        database="ml_ecommerce",
        user="postgres",
        password="0790"
    )
    return conn
