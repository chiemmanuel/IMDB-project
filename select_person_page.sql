-- Select basic information of a person
SELECT pi.*
FROM person_info pi
WHERE pi.person_id = 'nm0103842';

-- Select info for most popular titles of a person
SELECT ti.*, tr.average_rating, tr.num_votes
FROM title_info ti
JOIN title_ratings tr 
ON tr.title_id = ti.title_id
WHERE ti.title_id IN (
    SELECT unnest(known_for_titles) 
    FROM person_info 
    WHERE person_id = 'nm0103842'
);

-- Select all titles where the person is an actor
SELECT ti.*, tr.average_rating, tr.num_votes
FROM crew_actors ca
JOIN title_info ti ON ca.title_id = ti.title_id
JOIN title_ratings tr ON tr.title_id = ti.title_id
WHERE ca.person_id = 'nm0103842';

-- Select all titles where the person is a crew member
SELECT cm.category, ti.*, tr.average_rating, tr.num_votes
FROM crew_members cm
JOIN title_info ti ON cm.title_id = ti.title_id
JOIN title_ratings tr ON tr.title_id = ti.title_id
WHERE cm.person_id = 'nm0103842'
ORDER BY cm.category;