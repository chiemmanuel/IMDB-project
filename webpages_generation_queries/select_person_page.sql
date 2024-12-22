-- Select basic information of a person
SELECT pi.*
FROM person_info pi
WHERE pi.person_id = 'nm0103842';

-- Select info for most popular titles of a person
-- This query fetches the titles where the person is known for, based on the known_for_titles array in the person_info table.
-- This would provide the info for a banner or carousel of the person's most popular titles.
SELECT ti.*, tr.average_rating, tr.num_votes
FROM title_info ti
JOIN title_ratings tr 
ON tr.title_id = ti.title_id
WHERE ti.title_id IN (
    SELECT unnest(known_for_titles) -- unnest() function is used to unpack the array into individual rows for the IN clause
    FROM person_info 
    WHERE person_id = 'nm0103842'
);

-- Select all titles where the person is an actor
-- This query fetches all the titles where the person is an actor, along with the average rating and number of votes for each title.
-- It would be used to display a more exhasutive list of the person's acting credits.
SELECT ti.*, tr.average_rating, tr.num_votes
FROM crew_actors ca
JOIN title_info ti ON ca.title_id = ti.title_id
JOIN title_ratings tr ON tr.title_id = ti.title_id
WHERE ca.person_id = 'nm0103842';

-- Select all titles where the person is a crew member
-- This query fetches all the titles where the person is a crew member, along with the category of their role (e.g., writer, director) and the average rating and number of votes for each title.
-- It would be used to display a list of the person's non-acting credits.
SELECT cm.category, ti.*, tr.average_rating, tr.num_votes
FROM crew_members cm
JOIN title_info ti ON cm.title_id = ti.title_id
JOIN title_ratings tr ON tr.title_id = ti.title_id
WHERE cm.person_id = 'nm0103842'
ORDER BY cm.category;