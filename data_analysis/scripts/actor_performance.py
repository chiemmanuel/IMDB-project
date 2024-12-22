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

def fetch_actor_data(engine, top_n, rating_threshold=7.5):
    """
    Fetch data for actors in the top cast (ordering 1-5) and movies with ratings above the threshold.
    Handles null values and inconsistencies in the data.
    """
    query = f"""
    SELECT p.primary_name, COUNT(DISTINCT t.title_id) AS high_rated_movies_count
    FROM crew_actors c
    JOIN title_info t ON c.title_id = t.title_id
    JOIN person_info p ON c.person_id = p.person_id
    JOIN title_ratings r ON t.title_id = r.title_id
    WHERE c.ordering BETWEEN 1 AND 5
      AND r.average_rating IS NOT NULL
      AND r.average_rating > {rating_threshold}
      AND t.title_type = 'movie'
    GROUP BY p.primary_name
    ORDER BY high_rated_movies_count DESC
    LIMIT {top_n};
    """
    return pd.read_sql_query(query, engine)

def plot_actor_data(actor_data, top_n, rating_threshold):
    """
    Create a histogram for actor performance.
    """
    plt.figure(figsize=(10, 8))
    plt.bar(actor_data["primary_name"], actor_data["high_rated_movies_count"], color='skyblue')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.title(f"Top {top_n} Actors with High-Rated Movies (Ordering 1-5)", fontsize=14)
    plt.xlabel("Actors", fontsize=12)
    plt.ylabel(f"Number of Movies with Rating > {rating_threshold}", fontsize=12)
    plt.tight_layout()
    plt.show()

def main():
    """
    Main function to execute the actor analysis.
    """
    # Default number of actors to analyze
    top_n = 10
    rating_threshold = 7.5  # Default rating threshold
    if len(sys.argv) > 1:
        try:
            top_n = int(sys.argv[1])
        except ValueError:
            print("Invalid argument for number of actors. Using default value of 10.")
    
    # Use environment variables to create the database connection URL
    db_uri = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Database connection using SQLAlchemy
    try:
        engine = create_engine(db_uri)
    except Exception as e:
        print("Error connecting to the database:", e)
        return

    # Fetch actor data
    print(f"Analyzing the top {top_n} actors...")
    actor_data = fetch_actor_data(engine, top_n, rating_threshold)

    if actor_data.empty:
        print("No data found for the analysis.")
    else:
        # Handle potential nulls or inconsistencies
        actor_data["high_rated_movies_count"] = actor_data["high_rated_movies_count"].fillna(0)

        # Print actor names and their movie counts
        print("\nTop Actors and Their High-Rated Movie Counts:")
        for idx, row in actor_data.iterrows():
            print(f"{idx + 1}. {row['primary_name']}: {int(row['high_rated_movies_count'])} movies")

        # Visualize actor performance
        plot_actor_data(actor_data, top_n, rating_threshold)

if __name__ == "__main__":
    main()
