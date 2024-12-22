WITH movie_base AS (
    SELECT *
    FROM title_info
    WHERE title_type = 'movie'
    ORDER BY original_title
    LIMIT 10 OFFSET 0 -- Limiting to 10 movies for testing, can change to a  where id = 'tt1234567' to get a specific movie
),
alternative_titles AS (
    SELECT DISTINCT ON (lt.title_id, lt.title, lt.region, lt.lang)
        lt.title_id,
        jsonb_build_object(
            'title', lt.title,
            'region', lt.region,
            'language', lt.lang,
            'is_original_title', lt.is_original_title
        )::jsonb AS alt_title
    FROM local_titles lt
    WHERE lt.title_id IN (SELECT title_id FROM movie_base)
),
production_details AS (
    SELECT DISTINCT ON (cm.title_id, cm.job, p.primary_name)
        cm.title_id,
        CASE 
            WHEN cm.job = 'director' THEN jsonb_build_object('role', 'Director', 'name', p.primary_name)
            WHEN cm.job = 'writer' THEN jsonb_build_object('role', 'Writer', 'name', p.primary_name)
            ELSE jsonb_build_object('role', cm.job, 'name', p.primary_name)
        END AS prod_detail
    FROM crew_members cm
    JOIN person_info p ON cm.person_id = p.person_id
    WHERE cm.title_id IN (SELECT title_id FROM movie_base)
),
cast_details AS (
    SELECT DISTINCT ON (ca.title_id, ca.role_played, p2.primary_name)
        ca.title_id,
        jsonb_build_object(
            'role_played', ca.role_played,
            'actor_name', p2.primary_name,
            'is_actress', ca.is_actress
        )::jsonb AS cast_detail
    FROM crew_actors ca
    JOIN person_info p2 ON ca.person_id = p2.person_id
    WHERE ca.title_id IN (SELECT title_id FROM movie_base)
)

SELECT 
    mb.original_title AS "Original Title",
    mb.primary_title AS "Primary Title",
    mb.start_year AS "Release Year",
    mb.is_adult AS "Adult Content",
    mb.genres AS "Genres",
    mb.runtime_minutes AS "Runtime (minutes)",
    COALESCE(array_agg(DISTINCT at.alt_title) FILTER (WHERE at.alt_title IS NOT NULL), '{}') AS "Alternative Titles",
    COALESCE(array_agg(DISTINCT pd.prod_detail) FILTER (WHERE pd.prod_detail IS NOT NULL), '{}') AS "Production Details",
    COALESCE(array_agg(DISTINCT cd.cast_detail) FILTER (WHERE cd.cast_detail IS NOT NULL), '{}') AS "Cast Details"
FROM movie_base mb
LEFT JOIN alternative_titles at ON mb.title_id = at.title_id
LEFT JOIN production_details pd ON mb.title_id = pd.title_id
LEFT JOIN cast_details cd ON mb.title_id = cd.title_id
GROUP BY mb.title_id, mb.original_title, mb.primary_title, mb.start_year, mb.is_adult, mb.genres, mb.runtime_minutes
ORDER BY mb.original_title;