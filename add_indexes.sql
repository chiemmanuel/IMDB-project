-- Creating indexes for faster querying, run after inserting data

-- For title_info table
CREATE INDEX IF NOT EXISTS idx_title_info_title_type ON title_info(title_type);
CREATE INDEX IF NOT EXISTS idx_title_info_start_year ON title_info(start_year);
CREATE INDEX IF NOT EXISTS idx_title_info_original_title ON title_info(original_title);

-- For local_titles table
CREATE INDEX IF NOT EXISTS idx_local_titles_title_id ON local_titles(title_id);
CREATE INDEX IF NOT EXISTS idx_local_titles_region_lang ON local_titles(region, lang);

-- For title_ratings table
CREATE INDEX IF NOT EXISTS idx_title_ratings_average_rating ON title_ratings(average_rating);
CREATE INDEX IF NOT EXISTS idx_title_ratings_num_votes ON title_ratings(num_votes);

-- For person_info table
CREATE INDEX IF NOT EXISTS idx_person_info_primary_name ON person_info(primary_name);

-- For crew_actors table
CREATE INDEX IF NOT EXISTS idx_crew_actors_title_id ON crew_actors(title_id);
CREATE INDEX IF NOT EXISTS idx_crew_actors_person_id ON crew_actors(person_id);
CREATE INDEX IF NOT EXISTS idx_crew_actors_title_id_ordering ON crew_actors(title_id, ordering);

-- For crew_members table
CREATE INDEX IF NOT EXISTS idx_crew_members_title_id ON crew_members(title_id);
CREATE INDEX IF NOT EXISTS idx_crew_members_person_id ON crew_members(person_id);
CREATE INDEX IF NOT EXISTS idx_crew_members_title_id_job ON crew_members(title_id, job);

-- For title_episodes table
CREATE INDEX IF NOT EXISTS idx_title_episodes_parent_title_id ON title_episodes(parent_title_id);
CREATE INDEX IF NOT EXISTS idx_title_episodes_season_number ON title_episodes(season_number);

