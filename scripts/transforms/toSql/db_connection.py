# db_connection.py
import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        dbname="ch1vo",
        user="myuser",
        password="mypassword",
        host="localhost"
    )
    return conn
