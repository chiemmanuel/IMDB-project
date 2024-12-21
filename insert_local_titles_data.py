import psycopg2
import csv
import time
import sys  # Import sys to handle CSV field size limit

def parse_and_insert_tsv(file_path, db_params):
    """
    Parses a TSV file and inserts data into the local_titles table.
    All rows for `title_id`s in the title_ids.txt will be inserted, even if there are duplicates.

    Args:
        file_path (str): Path to the TSV file.
        db_params (dict): Database connection parameters.
    """
    # Set CSV field size limit
    csv.field_size_limit(sys.maxsize)

    # Database connection
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    TITLE_IDS_FILE = './tsv/title_ids.txt'

    # Step 1: Read all the title IDs from the title_ids.txt file
    title_ids = set()
    with open(TITLE_IDS_FILE, mode="r", encoding="utf-8") as file:
        for line in file:
            title_ids.add(line.strip())

    # Step 2: Prepare to insert data from the TSV file
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tsv_reader = csv.DictReader(file, delimiter='\t')

            # Initialize variables for batching and performance tracking
            rows_to_insert = []
            batch_size = 1000  # Number of rows per batch
            row_count = 0
            start_time = time.time()

            # Query for insertion
            query = """
            INSERT INTO local_titles (title_id, ordering, title, region, lang, types, attributes, is_original_title)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """

            # Step 3: Iterate over the rows in the TSV file
            for row in tsv_reader:
                title_id = row['titleId']

                # If the title_id is in title_ids.txt, prepare the row for insertion
                if title_id in title_ids:
                    ordering = int(row['ordering'])
                    title = row['title']
                    region = row['region'] if row['region'] != '\\N' else None
                    lang = row['language'] if row['language'] != '\\N' else None
                    types = row['types'].split(',') if row['types'] != '\\N' else []
                    attributes = row['attributes'].split(',') if row['attributes'] != '\\N' else []
                    is_original_title = bool(int(row['isOriginalTitle']))

                    # Append the row data as a tuple to the batch
                    rows_to_insert.append((title_id, ordering, title, region, lang, types, attributes, is_original_title))
                    row_count += 1

                # Execute the batch insert when batch size is reached
                if len(rows_to_insert) == batch_size:
                    cursor.executemany(query, rows_to_insert)
                    conn.commit()
                    rows_to_insert = []  # Clear the batch

            # Insert any remaining rows
            if rows_to_insert:
                cursor.executemany(query, rows_to_insert)
                conn.commit()

            # Measure the elapsed time
            end_time = time.time()
            elapsed_time = end_time - start_time

            # Output the results
            print(f"Data inserted successfully. Processed {row_count} rows.")
            print(f"Time taken for insertion: {elapsed_time:.2f} seconds.")

    except Exception as e:
        # If there's an error, roll back the transaction
        conn.rollback()
        print(f"Error: {e}")

    finally:
        # Clean up
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Path to the TSV file
    file_path = "./tsv/title.akas.tsv"

    # Database connection parameters
    db_params = {
        'dbname': 'IMDB',
        'user': 'admin',
        'password': 'adminpass',
        'host': 'localhost',
        'port': '5432'
    }

    # Call the function to parse and insert data
    parse_and_insert_tsv(file_path, db_params)
