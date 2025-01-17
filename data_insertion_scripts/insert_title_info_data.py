import psycopg2
import csv
import time
import os

# Database connection parameters
DB_HOST = os.getenv('DB_HOST', 'localhost')  # Default to localhost for local testing
DB_PORT = os.getenv('DB_PORT', '5432')  # Default PostgreSQL port
DB_NAME = os.getenv('DB_NAME', 'IMDB')  # Your database name
DB_USER = os.getenv('DB_USER', 'admin')  # Database username
DB_PASSWORD = os.getenv('DB_PASSWORD', 'adminpass') # Database password

# File path to your TSV file
TSV_FILE_PATH = '../tsv/title.basics.tsv'



# Function to transform '\N' to None and handle specific column transformations
def transform_row(row):
    return {
        "title_id": row[0],
        "title_type": row[1],
        "primary_title": row[2] if row[2] != "\\N" else None,
        "original_title": row[3] if row[3] != "\\N" else None,
        "is_adult": bool(int(row[4])),
        "start_year": row[5] if row[5] != "\\N" else None,
        "end_year": row[6] if row[6] != "\\N" else None,
        "runtime_minutes": row[7] if row[7] != "\\N" else None,
        "genres": row[8].split(",") if row[8] != "\\N" else None
    }

# Insert data into the title_info table
def insert_data():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Open the TSV file
        with open(TSV_FILE_PATH, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter="\t")
            next(reader)  # Skip the header row

            for i, row in enumerate(reader):
                if i >= 100000:
                    break
                transformed = transform_row(row)
                query = """
                    INSERT INTO title_info (
                        title_id, title_type, primary_title, original_title, 
                        is_adult, start_year, end_year, runtime_minutes, genres
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (title_id) DO NOTHING;
                """
                cursor.execute(query, (
                    transformed["title_id"],
                    transformed["title_type"],
                    transformed["primary_title"] if transformed["primary_title"] is not None else None,
                    transformed["original_title"] if transformed["original_title"] is not None else None,
                    transformed["is_adult"],
                    transformed["start_year"] if transformed["start_year"] is not None else None,
                    transformed["end_year"] if transformed["end_year"] is not None else None,
                    transformed["runtime_minutes"] if transformed["runtime_minutes"] is not None else None,
                    transformed["genres"],
                ))

        # Commit the transaction
        conn.commit()
        print("Data successfully inserted into the title_info table.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the database connection
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    start_time = time.time()
    insert_data()
    print(f"Execution time: {time.time() - start_time} seconds.")