# Webpages Generation Queries

This document outlines the SQL queries used to generate the data for the different webpages of the IMDb website. The queries are categorized based on the webpage they are used to generate.

## [select_person_page.sql](../webpages_generation_queries/select_person_page.sql)

The data for this page is fetched in four main queries, the first to select the basic person info, second the titles the person is known for, third the person's acting roles, and finally the person's non-acting roles. The queries are as follows:

### Select basic information of a person
This query fetches the basic information of a person from the `person_info` table, such as their name, birth year, death year, primary profession, and known for titles. This information would be displayed on the person's profile page.

### Select info for most popular titles of a person
This query fetches the titles where the person is known for, based on the known_for_titles array in the person_info table. This would provide the info for a banner or carousel of the person's most popular titles.

### Select all titles where the person is an actor
This query fetches all the titles where the person is an actor, along with the average rating and number of votes for each title. It would be used to display a more exhaustive list of the person's acting credits.

### Select all titles where the person is a crew member
This query fetches all the titles where the person is a crew member, along with the category of their role (e.g., writer, director) and the average rating and number of votes for each title. It would be used to display a list of the person's non-acting credits.

## [select_episode_page.sql](../webpages_generation_queries/select_episode_page.sql)
The data for this page is fetched in four main queries, the first to fetch the overall information about the episode, second to fetch all localized titles for the episode, the third to fetch the writers & directors of the episode, and fourth to fetch the guest stars on that episode. The queries are as follows:

### Query to fetch episode-specific information for a given episode ID
This main query fetches all the basic information related to a given episode, such as the parent's title & id, title, release year, runtime, genres, season number, episode number, average rating, and number of votes.

### Query to fetch all localized titles for a given episode ID
This query fetches all the localized titles for a given episode by simply selecting from the local_titles table where the title_id matches the given episode ID with the results ordered by the region.

### Query to fetch the writers & directors for a given episode ID
This query fetches the writers & directors for a given episode by joining the crew_members table with the person_info table on the person_id field. It then filters the results based on the title_id and the category (writer or director) to get the desired information. The results are ordered by the category to separate the writers from the directors.

### Query to fetch guest stars for a given episode ID
As guest star is not a standard role in the IMDB dataset, I instead chose to determine guest stars as actors who only appear in a single episode of a given series. I find these actors by filtering out actors who appear in any title that shares the same parent title ID as the given episode, but are not the given episode itself.
