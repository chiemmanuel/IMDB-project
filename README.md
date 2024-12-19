# IMDB-project

for title_ids.txt:
```bash
head -n 100000 title.basics.tsv | cut -f 1 > title_ids.txt
```

for persons_id.txt:
```bash
head -n 100000 name.basics.tsv | cut -f 1 > person_ids.txt
```