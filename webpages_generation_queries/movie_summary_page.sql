WITH movie_base AS (
    SELECT 
        ti.title_id,
        ti.original_title, 
        ti.start_year AS "release year", 
        ti.runtime_minutes AS "length (minutes)", 
        tr.average_rating, 
        tr.num_votes
    FROM title_info ti
    LEFT JOIN title_ratings tr ON ti.title_id = tr.title_id
    WHERE ti.title_type = 'movie'
),
directors AS (
    SELECT 
        cm.title_id,
        array_agg(p.primary_name ORDER BY p.primary_name) AS directors
    FROM crew_members cm
    JOIN person_info p ON cm.person_id = p.person_id
    WHERE cm.job = 'director'
    GROUP BY cm.title_id
),
writers AS (
    SELECT 
        cm.title_id,
        array_agg(p.primary_name ORDER BY p.primary_name) AS writers
    FROM crew_members cm
    JOIN person_info p ON cm.person_id = p.person_id
    WHERE cm.job = 'writer'
    GROUP BY cm.title_id
),
main_cast AS (
    SELECT 
        ca.title_id,
        array_agg(p.primary_name ORDER BY ca.ordering ASC) AS main_cast
    FROM crew_actors ca
    JOIN person_info p ON ca.person_id = p.person_id
    GROUP BY ca.title_id
)

SELECT 
    mb.original_title, 
    mb."release year", 
    mb."length (minutes)", 
    mb.average_rating, 
    mb.num_votes, 
    d.directors, 
    w.writers,
    (SELECT mc.main_cast[1:5] FROM main_cast mc WHERE mc.title_id = mb.title_id) AS "main cast"
FROM movie_base mb
LEFT JOIN directors d ON mb.title_id = d.title_id
LEFT JOIN writers w ON mb.title_id = w.title_id
ORDER BY mb.original_title
LIMIT 100 OFFSET 0; -- limiting to 100 movies for testing