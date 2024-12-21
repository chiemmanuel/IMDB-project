---Movie page: title, year, length, director, writer, main cast, rating, votes, basic info
SELECT ti.original_title, 
       ti.start_year, 
       ti.runtime_minutes AS length, 
       tr.average_rating, 
       tr.num_votes,
       array_agg(CASE WHEN cm.job = 'director' THEN p.primary_name END) AS directors,
       array_agg(CASE WHEN cm.job = 'writer' THEN p.primary_name END) AS writers
FROM title_info ti
JOIN title_ratings tr ON ti.title_id = tr.title_id
JOIN crew_members cm ON ti.title_id = cm.title_id
JOIN person_info p ON cm.person_id = p.person_id
WHERE cm.job IN ('director', 'writer')
GROUP BY ti.original_title, ti.start_year, ti.runtime_minutes, tr.average_rating, tr.num_votes
ORDER BY ti.original_title;


SELECT ti.original_title, 
       ARRAY_AGG(p.primary_name) AS actors
FROM title_info ti
JOIN crew_actors ca ON ti.title_id = ca.title_id
JOIN person_info p ON ca.person_id = p.person_id
GROUP BY ti.original_title
ORDER BY ti.original_title
LIMIT 5;




