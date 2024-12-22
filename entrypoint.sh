#!/bin/bash

# Run all scripts sequentially

python ./data_insertion_scripts/insert_titleinfo_data.py

python ./data_insertion_scripts/insert_title_rating_data.py

python ./data_insertion_scripts/insert_local_titles_data.py

python ./data_insertion_scripts/insert_person_data.py

python ./data_insertion_scripts/insert_crew_data.py

python ./data_insertion_scripts/insert_episode_data.py