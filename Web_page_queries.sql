---Movie page: title, year, length, director, writer, main cast, rating, votes, basic info
SELECT ti.original_title, ti.start_year, ti.runtime_minutes AS length, 
       p.primary_name, tr.average_rating, tr.num_votes
FROM title_info ti
JOIN title_ratings tr ON ti.title_id = tr.title_id
JOIN crew_members cm ON ti.title_id = cm.title_id
JOIN person_info p ON cm.person_id = p.person_id
WHERE (cm.job = 'director' OR cm.job = 'writer') 



SELECT ti.original_title, 
       (p.birth_year - COALESCE(p.death_year, EXTRACT(YEAR FROM CURRENT_DATE))) AS age
FROM title_info ti
JOIN crew_actors ca ON ti.title_id = ca.title_id
JOIN person_info p ON ca.person_id = p.person_id
GROUP BY ti.original_title
ORDER BY ca.ordering
LIMIT 5


