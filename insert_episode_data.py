import psycopg2
import csv
import time  # Import time module to measure execution time

# Database connection parameters
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'IMDB'
DB_USER = 'admin'
DB_PASSWORD = 'adminpass'

# File path to your TSV file
TSV_FILE_PATH = './tsv/title.episode.tsv'

TITLE_IDS_FILE = './tsv/title_ids.txt'

# Read each line from the TITLE_IDS_FILE and append it to title_ids
title_ids = set()

with open(TITLE_IDS_FILE, mode="r", encoding="utf-8") as file:
    for line in file:
        title_ids.add(line.strip())

# Function to transform '\N' to None and handle specific column transformations
def transform_row(row):
    return {
        "episode_id": row[0],
        "parent_title_id": row[1] if row[1] != "\\N" else None,
        "season_number": int(row[2]) if row[2] != "\\N" else None,
        "episode_number": int(row[3]) if row[3] != "\\N" else None
    }

# Insert data into the title_episodes table
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

            count = 0  # Track the number of rows inserted
            for row in reader:
                transformed = transform_row(row)

                # Check if the parent_title_id is in the title_ids set
                if transformed["parent_title_id"] in title_ids:
                    query = """
                        INSERT INTO title_episodes (
                            episode_id, parent_title_id, season_number, episode_number
                        )
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (episode_id) DO NOTHING;
                    """
                    cursor.execute(query, (
                        transformed["episode_id"],
                        transformed["parent_title_id"],
                        transformed["season_number"],
                        transformed["episode_number"]
                    ))

                    count += 1

        # Commit the transaction
        conn.commit()

        # Measure the end time and calculate elapsed time
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"First {count} entries successfully inserted into the title_episodes table.")
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
