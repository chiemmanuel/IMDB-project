import psycopg2
import csv

def parse_and_insert_tsv(file_path, db_params):
    """
    Parses a TSV file and inserts data into the local_titles table.

    Args:
        file_path (str): Path to the TSV file.
        db_params (dict): Database connection parameters.
    """
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tsv_reader = csv.DictReader(file, delimiter='\t')

            for i, row in enumerate(tsv_reader):
                if i >= 100000:
                    break
                title_id = row['titleId']
                ordering = int(row['ordering'])
                title = row['title']
                region = row['region'] if row['region'] != '\\N' else None
                lang = row['language'] if row['language'] != '\\N' else None
                types = row['types'].split(',') if row['types'] != '\\N' else []
                attributes = row['attributes'].split(',') if row['attributes'] != '\\N' else []
                is_original_title = bool(int(row['isOriginalTitle']))

                # Insert query
                query = """
                INSERT INTO local_titles (title_id, ordering, title, region, lang, types, attributes, is_original_title)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (title_id, ordering) DO NOTHING;
                """
                cursor.execute(query, (title_id, ordering, title, region, lang, types, attributes, is_original_title))

        conn.commit()
        print("Data inserted successfully.")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    file_path = "./tsv/title.akas.tsv"

    db_params = {
        'dbname': 'IMDB',
        'user': 'admin',
        'password': 'adminpass',
        'host': 'localhost',
        'port': '5432'
    }

    parse_and_insert_tsv(file_path, db_params)
