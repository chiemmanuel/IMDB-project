import psycopg2
import csv

# Database connection parameters
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'IMDB'
DB_USER = 'admin'
DB_PASSWORD = 'adminpass'

# File path to your TSV file
TSV_FILE_PATH = './tsv/name.basics.tsv'

# Connect to the PostgreSQL database
def connect_to_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# Insert data into the person_info table
def insert_data_into_table(conn, data):
    try:
        with conn.cursor() as cursor:
            insert_query = """
                INSERT INTO person_info (
                    person_id,
                    primary_name,
                    birth_year,
                    death_year,
                    primary_profession,
                    known_for_titles
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (person_id) DO NOTHING;
            """
            cursor.executemany(insert_query, data)
        conn.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()

# Process TSV file and prepare data
def process_tsv_file(file_path):
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='\t')
            next(reader)  # Skip header row
            for row in reader:
                person_id = row[0]
                primary_name = row[1]
                birth_year = int(row[2]) if row[2] != '\\N' else None
                death_year = int(row[3]) if row[3] != '\\N' else None
                primary_profession = row[4].split(',') if row[4] != '\\N' else None
                known_for_titles = row[5].split(',') if row[5] != '\\N' else None
                data.append((
                    person_id,
                    primary_name,
                    birth_year,
                    death_year,
                    primary_profession,
                    known_for_titles
                ))
    except Exception as e:
        print(f"Error processing file: {e}")
    return data

def main():
    conn = connect_to_db()
    if conn:
        print("Connected to database.")
        data = process_tsv_file(TSV_FILE_PATH)
        if data:
            print("Data processed successfully.")
            insert_data_into_table(conn, data)
        conn.close()

if __name__ == '__main__':
    main()
