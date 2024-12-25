# IMDB-project

## Project Summary
This is Travis Berthrong & Junior Chi Emmanuel's submission for the final project. The sql files for the database structure and the webpages generation queries are in the respective folders. The data analysis scripts are in the data_analysis folder. The documentation folder contains the markdown files for the database schema, webpages generation queries, and data analysis.

## Team Members
- Junior Chi Emmanuel Ngu
- Travis Berthrong

## Running the Project
1. Clone the repository.
2. Run docker-compose up to start the PostgreSQL database.
3. Create a databse called IMDB.
4. Run the [Full IMDB Database Creation Script](./schema/Full%20IMDB%20database%20backup.zip) to create the database schema and populate the tables.
5. Run the webpages generation queries located in the [webpages_generation_queries](./webpages_generation_queries) folder.
6. Run the data analysis scripts located in the [data_analysis/scripts](./data_analysis/scripts) folder or view the output directly either in the [markdown files](./documentation/data_analysis.md) or the [data_analysis/output](./data_analysis/output) folder. The data analysis scripts do require a .env file to be created following the [.env.template](./.env.template) file.
 
## Table of Contents

1. [Database Schema](documentation/database_schema.md)
2. [Webpages Generation Queries](documentation/webpages_generation_queries.md)
   - [select_person_page.sql](webpages_generation_queries/select_person_page.sql)
   - [select_episode_page.sql](webpages_generation_queries/select_episode_page.sql)
   - [movie_detail_page.sql](webpages_generation_queries/movie_detail_page.sql)
   - [movie_summary_page.sql](webpages_generation_queries/movie_summary_page.sql)
   - [tv_series_summary_page.sql](webpages_generation_queries/tv_series_summary_page.sql)
3. [Data Analysis](documentation/data_analysis.md)
   - [Episode Rating Performance Analysis](data_analysis/scripts/episode_rating_performance.py)
   - [Actor Rating Performance Analysis](data_analysis/scripts/actor_rating_performance.py)
   - [Genre Popularity Over Decades](data_analysis/scripts/most_popular_genre_overtime.py)
4. [Scripts used for initial dataset parsing](./data_insertion_scripts/)
   - These scripts were used to parse the original dataset and insert the data into the database.


