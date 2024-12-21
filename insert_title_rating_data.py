import psycopg2
import csv
import time

def parse_and_insert_ratings_tsv(file_path, db_params):
    """
    Parses a TSV file and inserts data into the title_ratings table.

    Args:
        file_path (str): Path to the TSV file.
        db_params (dict): Database connection parameters.
    """
    # Database connection
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    TITLE_IDS_FILE = './tsv/title_ids.txt'

    title_ids = set()

    # Read each line from the TITLE_IDS_FILE and append it to title_ids
    with open(TITLE_IDS_FILE, mode="r", encoding="utf-8") as file:
        for line in file:
            title_ids.add(line.strip())

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tsv_reader = csv.DictReader(file, delimiter='\t')

            row_count = 0  # Initialize a counter for the number of rows inserted
            start_time = time.time()  # Start the timer

            for i, row in enumerate(tsv_reader):
                if i >= 100000:
                    break
                title_id = row['tconst']
                if title_id not in title_ids:
                    continue
                average_rating = float(row['averageRating'])
                num_votes = int(row['numVotes'])

                # Insert query
                query = """
                INSERT INTO title_ratings (title_id, average_rating, num_votes)
                VALUES (%s, %s, %s)
                ON CONFLICT (title_id) DO UPDATE 
                SET average_rating = EXCLUDED.average_rating, 
                    num_votes = EXCLUDED.num_votes;
                """
                cursor.execute(query, (title_id, average_rating, num_votes))
                row_count += 1  # Increment row counter

        conn.commit()

        # Stop the timer and calculate elapsed time
        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"Data inserted successfully. {row_count} rows inserted.")
        print(f"Time taken for insertion: {elapsed_time:.2f} seconds.")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Path to the TSV file
    file_path = "tsv/title.ratings.tsv"

    # Database connection parameters
    db_params = {
        'dbname': 'IMDB',
        'user': 'admin',
        'password': 'adminpass',
        'host': 'localhost',
        'port': '5432'
    }

    parse_and_insert_ratings_tsv(file_path, db_params)
