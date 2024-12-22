WITH series_base AS (
    SELECT 
        ti.title_id,
        ti.primary_title AS "Title",
        ti.original_title,
        ti.start_year AS "Release Year",
        ti.end_year AS "End Year",
        COALESCE(ti.end_year, EXTRACT(YEAR FROM CURRENT_DATE)) - ti.start_year AS "Series Length (Years)",
        ti.runtime_minutes AS "Runtime (minutes) per episode"
    FROM title_info ti
    WHERE ti.title_type = 'tvSeries'
),
series_ratings AS (
    SELECT 
        tr.title_id,
        tr.average_rating AS "Average Rating",
        tr.num_votes AS "Number of Votes"
    FROM title_ratings tr
),
series_seasons AS (
    SELECT 
        parent_title_id,
        COUNT(DISTINCT season_number) AS "Number of Seasons"
    FROM title_episodes
    GROUP BY parent_title_id
),
main_cast AS (
    SELECT 
        ca.title_id,
        array_agg(p.primary_name ORDER BY ca.ordering ASC) AS cast_members
    FROM crew_actors ca
    JOIN person_info p ON ca.person_id = p.person_id
    GROUP BY ca.title_id
)

SELECT 
    sb.*,
    sr."Average Rating",
    sr."Number of Votes",
    ss."Number of Seasons",
    (SELECT mc.cast_members[1:5] FROM main_cast mc WHERE mc.title_id = sb.title_id) AS "main cast"
FROM series_base sb
LEFT JOIN series_ratings sr ON sb.title_id = sr.title_id
LEFT JOIN series_seasons ss ON sb.title_id = ss.parent_title_id
ORDER BY sb."Title";