import os
import psycopg2

DB_HOST = os.getenv('DB_HOST', 'localhost') 
DB_PORT = os.getenv('DB_PORT', '5432')  # Default PostgreSQL port
DB_NAME = os.getenv('DB_NAME', 'IMDB')  # Your database name
DB_USER = os.getenv('DB_USER', 'admin')  # Database username
DB_PASSWORD = os.getenv('DB_PASSWORD', 'adminpass') # Database password

try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        print("Connected to the database.")
        cursor = conn.cursor()
except Exception as e:
        print("Error connecting to the database: ", e)