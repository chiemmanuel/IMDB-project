import psycopg2
import csv
import time
import os

DB_HOST = os.getenv('DB_HOST', 'localhost')  # Default to localhost for local testing
DB_PORT = os.getenv('DB_PORT', '5432')  # Default PostgreSQL port
DB_NAME = os.getenv('DB_NAME', 'IMDB')  # Your database name
DB_USER = os.getenv('DB_USER', 'admin')  # Database username
DB_PASSWORD = os.getenv('DB_PASSWORD', 'adminpass') # Database password

# File paths to your TSV file and IDs
TSV_FILE_PATH = '../tsv/title.principals.tsv'
TITLE_IDS_FILE = '../tsv/title_ids.txt'
PERSON_IDS_FILE = '../tsv/person_ids.txt'

title_ids = set()
person_ids = set()

# Load title_ids
with open(TITLE_IDS_FILE, mode="r", encoding="utf-8") as file:
    for line in file:
        title_ids.add(line.strip())

# Load person_ids
with open(PERSON_IDS_FILE, mode="r", encoding="utf-8") as file:
    for line in file:
        person_ids.add(line.strip())

# Function to transform '\N' to None and handle specific column transformations
def transform_row(row):
    return {
        "title_id": row[0],
        "ordering": int(row[1]) if row[1] != "\\N" else None,
        "person_id": row[2],
        "category": row[3],
        "job": row[4] if row[4] != "\\N" else None,
        "characters": row[5] if row[5] != "\\N" else None
    }

# Insert data into the crew_actors and crew_members tables
def insert_data():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        print("Connected to the database.")
        cursor = conn.cursor()

        # Measure the start time
        start_time = time.time()

        # Open the TSV file
        with open(TSV_FILE_PATH, mode="rt", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter="\t")
            next(reader)  # Skip the header row

            count_actors = 0  # Track the number of rows inserted into crew_actors
            count_members = 0  # Track the number of rows inserted into crew_members

            for row in reader:
                if count_actors and count_members >= 100000:  # Stop after 100,000 entries for testing
                    break
                transformed = transform_row(row)

                # Skip rows with invalid title_id or person_id
                if transformed["title_id"] not in title_ids or transformed["person_id"] not in person_ids:
                    continue

                if transformed["category"] in ["actor", "actress"]:
                    query = """
                        INSERT INTO crew_actors (
                            title_id, person_id, ordering, role_played, is_actress
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING;
                    """
                    is_actress = transformed["category"] == "actress"
                    cursor.execute(query, (
                        transformed["title_id"],
                        transformed["person_id"],
                        transformed["ordering"],
                        transformed["characters"],
                        is_actress
                    ))
                    count_actors += 1

                else:
                    query = """
                        INSERT INTO crew_members (
                            title_id, person_id, job, category
                        )
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT DO NOTHING;
                    """
                    cursor.execute(query, (
                        transformed["title_id"],
                        transformed["person_id"],
                        transformed["job"],
                        transformed["category"] 
                    ))
                    count_members += 1

        # Commit the transaction
        conn.commit()

        # Measure the end time and calculate elapsed time
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Entries successfully inserted into the tables.")
        print(f"Actors: {count_actors}, Crew Members: {count_members}")
        print(f"Time taken for insertion: {elapsed_time:.2f} seconds.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the database connection
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    insert_data()
