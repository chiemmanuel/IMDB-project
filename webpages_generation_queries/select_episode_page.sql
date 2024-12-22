
-- Query to fetch episode-specific information for a given episode ID
-- This main query fetches all the basic information related to a given episode, such as the parent's title & id, title, release year, runtime, genres, season number, episode number, average rating, and number of votes.
SELECT parent_ti.title_id AS parent_id, parent_ti.primary_title AS parent_title,
    ep_ti.primary_title AS episode_title, ep_ti.original_title, ep_ti.is_adult,
    ep_ti.start_year AS release_year, ep_ti.runtime_minutes, ep_ti.genres,
    te.season_number, te.episode_number, ep_tr.average_rating, ep_tr.num_votes
FROM title_episodes te
JOIN title_info ep_ti ON ep_ti.title_id = te.episode_id
JOIN title_ratings ep_tr ON ep_tr.title_id = te.episode_id
JOIN title_info parent_ti ON parent_ti.title_id = te.parent_title_id
WHERE te.episode_id = 'tt0041951';

-- Query to fetch the writers & directors for a given episode ID
-- This query fetches the writers & directors for a given episode by joining the crew_members table with the person_info table on the person_id field.
-- It then filters the results based on the title_id and the category (writer or director) to get the desired information.
-- The results are ordered by the category to separate the writers from the directors.
SELECT cm.category, cm.person_id, pi.primary_name
FROM crew_members cm
JOIN person_info pi ON cm.person_id = pi.person_id
WHERE cm.title_id = 'tt0041951' AND (cm.category = 'writer' OR cm.category = 'director')
ORDER BY cm.category;

-- Query to fetch guest stars for a given episode ID
-- As guest star is not a standard role in the IMDB dataset, I instead chose to determine guest stars as actors who only appear in a single episode of a given series.
-- I find these actors by filtering out actors who appear in any title that shares the same parent title ID as the given episode, but are not the given episode itself.
SELECT DISTINCT
    ca.person_id,
    pi.primary_name AS actor_name,
    ca.role_played
FROM 
    crew_actors ca
JOIN 
    person_info pi ON pi.person_id = ca.person_id
JOIN 
    title_episodes te ON te.episode_id = ca.title_id
WHERE 
    ca.title_id = 'tt0041951'
    AND NOT EXISTS (
        SELECT 1
        FROM crew_actors other_ca
        JOIN title_episodes other_te ON other_te.episode_id = other_ca.title_id
        WHERE 
            other_ca.person_id = ca.person_id
            AND other_te.parent_title_id = te.parent_title_id
            AND other_ca.title_id <> te.episode_id
);