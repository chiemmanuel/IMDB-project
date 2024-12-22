#Top Episodes: Identify episodes with the highest ratings.
#Season Performance: Compare average ratings across seasons to find the most consistent series.
#Title Fragmentation: Analyze how titles with episodes compare in terms of ratings to standalone titles.

import argparse
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define database credentials
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "IMDB"
DB_USER = "admin"
DB_PASSWORD = "adminpass"

def connect_to_db_sqlalchemy():
    """Establishes connection to the PostgreSQL database using SQLAlchemy."""
    try:
        db_uri = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(db_uri)
        print("Database connection using SQLAlchemy successful.")
        return engine
    except Exception as e:
        print(f"Error connecting to the database using SQLAlchemy: {e}")
        return None

def retrieve_episode_data(engine):
    """Fetches episode and rating data from the database."""
    query = """
    SELECT 
        e.parent_title_id, 
        e.season_number, 
        e.episode_number, 
        r.average_rating, 
        r.num_votes,
        ti.primary_title AS series_name
    FROM 
        title_episodes e
    LEFT JOIN 
        title_ratings r ON e.episode_id = r.title_id
    LEFT JOIN 
        title_info ti ON e.parent_title_id = ti.title_id
    WHERE 
        e.season_number IS NOT NULL AND e.episode_number IS NOT NULL
    ORDER BY 
        e.parent_title_id, e.season_number, e.episode_number;
    """
    try:
        return pd.read_sql_query(query, engine)
    except Exception as e:
        print(f"Error retrieving data: {e}")
        return None

def handle_nulls(data):
    """Handles null values in the dataset."""
    print("Null values before handling:")
    print(data.isnull().sum())

    data['average_rating'] = data['average_rating'].fillna(data['average_rating'].mean())  # Replace null ratings with mean
    data['num_votes'] = data['num_votes'].fillna(0)  # Replace null votes with 0
    data = data.dropna(subset=['season_number', 'episode_number'])

    print("Null values after handling:")
    print(data.isnull().sum())
    return data

def get_top_series(data, top_n=10):
    """Identifies the top N best-rated series based on average episode ratings."""
    top_series = (
        data.groupby(['parent_title_id', 'series_name'])['average_rating']
        .mean()
        .reset_index()
        .sort_values(by='average_rating', ascending=False)
        .head(top_n)
    )
    return top_series

def visualize_combined_series(data, top_series):
    """Visualizes episode ratings for the top series in a combined plot."""
    # Filter data for the top series
    top_series_ids = top_series['parent_title_id'].tolist()
    filtered_data = data[data['parent_title_id'].isin(top_series_ids)]
    
    plt.figure(figsize=(14, 8))
    sns.lineplot(
        data=filtered_data,
        x='episode_number',
        y='average_rating',
        hue='series_name',
        style='season_number',
        markers=True,
        dashes=False,
        palette='tab10'
    )
    plt.title("Episode Ratings Comparison for Top Series First Season", fontsize=14)
    plt.xlabel("Episode Number", fontsize=12)
    plt.ylabel("Average Rating", fontsize=12)
    plt.legend(title="Series (Season)", fontsize=10, loc='upper left', bbox_to_anchor=(1, 1))
    plt.xticks(
        ticks=range(int(filtered_data['episode_number'].min()), int(filtered_data['episode_number'].max()) + 1),
        fontsize=10
    )
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    """Main function to execute the analysis."""
    parser = argparse.ArgumentParser(description="Analyze and visualize episode ratings for the best series.")
    parser.add_argument("--top_n", type=int, default=10, help="Number of top series to compare (default: 10).")
    args = parser.parse_args()

    engine = connect_to_db_sqlalchemy()
    if engine:
        data = retrieve_episode_data(engine)
        if data is not None and not data.empty:
            print(data.head())
            data = handle_nulls(data)
            top_series = get_top_series(data, top_n=args.top_n)
            print(f"Top {args.top_n} Series:")
            print(top_series)
            visualize_combined_series(data, top_series)

if __name__ == "__main__":
    main()
