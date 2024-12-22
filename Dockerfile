# Use the official Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all necessary files to the container
COPY ./data_insertion_scripts app/data_insertion_scripts
COPY ./webpages_generation_queries app/webpages_generation_queries
COPY ./tsv /app/tsv
COPY ./create_tables.sql /app/create_tables.sql
COPY ./add_indexes.sql /app/add_indexes.sql
COPY ./requirements.txt /app/requirements.txt
COPY ./entrypoint.sh /app/entrypoint.sh

# Install required Python packages
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set the environment variable for the DB credentials
ENV DB_HOST=localhost
ENV DB_PORT=5432
ENV DB_NAME=IMDB
ENV DB_USER=admin
ENV DB_PASSWORD=adminpass

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
