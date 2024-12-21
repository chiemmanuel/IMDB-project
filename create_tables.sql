CREATE TABLE IF NOT EXISTS title_info (
    title_id VARCHAR(20) PRIMARY KEY,
    title_type VARCHAR(20) NOT NULL,
    primary_title VARCHAR(1000),
    original_title VARCHAR(1000) NOT NULL,
    is_adult BOOLEAN NOT NULL,
    start_year INTEGER,
    end_year INTEGER,
    runtime_minutes INTEGER,
    genres TEXT ARRAY
);

CREATE TABLE IF NOT EXISTS local_titles (
    title_id VARCHAR(20) PRIMARY KEY,
    ordering INTEGER NOT NULL,
    title VARCHAR(1000) NOT NULL,
    region VARCHAR(6),
    lang VARCHAR(6),
    types TEXT ARRAY,
    attributes TEXT ARRAY,
    is_original_title BOOLEAN,
    FOREIGN KEY (title_id) REFERENCES title_info(title_id)
);

CREATE TABLE IF NOT EXISTS title_ratings (
    title_id VARCHAR(20) PRIMARY KEY,
    average_rating FLOAT CHECK (average_rating >= 0),
    num_votes INTEGER CHECK (num_votes >= 0),
    FOREIGN KEY (title_id) REFERENCES title_info(title_id)
);

CREATE TABLE IF NOT EXISTS person_info (
    person_id VARCHAR(20) PRIMARY KEY,
    primary_name VARCHAR(100) NOT NULL,
    birth_year INTEGER NOT NULL,
    death_year INTEGER,
    primary_profession TEXT ARRAY,
    known_for_titles TEXT ARRAY
);

CREATE TABLE IF NOT EXISTS crew_actors (
    title_id VARCHAR(20),
    person_id VARCHAR(20),
    ordering INTEGER NOT NULL,
    role_played VARCHAR(100),
    is_actress BOOLEAN NOT NULL,
    FOREIGN KEY (title_id) REFERENCES title_info(title_id),
    FOREIGN KEY (person_id) REFERENCES person_info(person_id)
);

CREATE TABLE IF NOT EXISTS crew_members (
    title_id VARCHAR(20),
    person_id VARCHAR(20),
    job VARCHAR(100),
    FOREIGN KEY (title_id) REFERENCES title_info(title_id),
    FOREIGN KEY (person_id) REFERENCES person_info(person_id)
);

CREATE TABLE IF NOT EXISTS title_episodes (
    episode_id VARCHAR(20) PRIMARY KEY,
    parent_title_id VARCHAR(20),
    season_number INTEGER NOT NULL,
    episode_number INTEGER NOT NULL,
    FOREIGN KEY (parent_title_id) REFERENCES title_info(title_id)
);





