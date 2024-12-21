
-- Query to fetch all episode-specific information for a given episode ID
SELECT parent_ti.title_id AS parent_id, parent_ti.primary_title AS parent_title, ep_ti.primary_title AS episode_title, ep_ti.original_title, ep_ti.is_adult, ep_ti.start_year AS release_year, ep_ti.runtime_minutes, ep_ti.genres,
te.season_number, te.episode_number, ep_tr.average_rating, ep_tr.num_votes
FROM title_episodes te
JOIN title_info ep_ti ON ep_ti.title_id = 'tt0041951'
JOIN title_ratings ep_tr ON ep_tr.title_id = 'tt0041951'
JOIN title_info parent_ti ON parent_ti.title_id = te.parent_title_id
WHERE te.episode_id = 'tt0041951';

-- Query to fetch all actors who appeared in the given episode but not in any other episode of the same series
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