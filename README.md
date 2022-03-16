# nebula3_database
NEBULA arango and milvus api
Structure: 
1. database/arango.py - API for arango client
2. database/milvus.py - API for vector database client
3. database/s3_api.py - API for accessin s3 store
4. database/elastic.py - API for ElasticSearch
5. notebooks/ -  test and play notebooks 
6. movie_graph.py - Graph API
7. movie_db.py - API for movie metadata, stored in document db
8. config.py - database connection settings
9. Dockerfile - docker image definition
10. run.sh - image entry point
11. environment.yaml - python dependencies
