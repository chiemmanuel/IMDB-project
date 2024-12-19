SELECT ti.primary_title, ti.start_year AS release_year, ti.runtime_minutes, tr.average_rating, tr.num_votes 
FROM title_info ti
JOIN title_ratings tr ON ti.title_id = tr.title_id AND ti.title_id = ?
WHERE ti.title_id = '?'