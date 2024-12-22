import sys
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch database credentials from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_NAME = os.getenv("DB_NAME", "IMDB")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "adminpass")

def fetch_genre_popularity(engine):
    """
    Fetch the number of movies per genre per decade, with genre extraction.
    Filters to select only movies based on title_type.
    """
    query = """
    SELECT (ti.start_year / 10) * 10 AS decade,
           unnest(string_to_array(regexp_replace(array_to_string(ti.genres, ','), '[{}]', '', 'g'), ',')) AS genre,
           COUNT(*) AS movie_count
    FROM title_info ti
    WHERE ti.start_year IS NOT NULL 
      AND ti.genres IS NOT NULL 
      AND ti.title_type = 'movie'
    GROUP BY decade, genre
    ORDER BY decade, movie_count DESC;
    """
    return pd.read_sql_query(query, engine)

def plot_genre_popularity(genre_data):
    """
    Create a stacked bar chart for genre popularity over decades.
    """
    genre_data_pivot = genre_data.pivot(index='decade', columns='genre', values='movie_count').fillna(0)

    # Print genre counts in the console before plotting
    print("\nGenre Popularity Over Decades (Exact Counts):\n")
    for decade in genre_data_pivot.index:
        print(f"Decade: {decade}s")
        for genre in genre_data_pivot.columns:
            count = genre_data_pivot.loc[decade, genre]
            if count > 0:
                print(f"  {genre}: {int(count)} movies")

    # Plot the stacked bar chart
    genre_data_pivot.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='tab20')
    plt.title('Most Popular Genres Over Decades')
    plt.xlabel('Decade')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    """
    Main function to execute the genre popularity analysis.
    """
    # Use environment variables to create the database connection URL
    db_uri = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    try:
        engine = create_engine(db_uri)
    except Exception as e:
        print("Error connecting to the database:", e)
        return

    # Fetch genre popularity over decades
    genre_data = fetch_genre_popularity(engine)

    if genre_data.empty:
        print("No data found for the analysis.")
    else:
        # Plot the results and print counts to the console
        plot_genre_popularity(genre_data)

if __name__ == "__main__":
    main()
