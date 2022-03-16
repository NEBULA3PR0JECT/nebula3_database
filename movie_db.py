import os
import time
import urllib
from database.arangodb import DatabaseConnector
from config import NEBULA_CONF




class MOVIE_DB:
    def __init__(self):
        #self.connect_db("nebula_development")
        config = NEBULA_CONF()
        self.db_host = config.get_database_host()
        self.database = config.get_database_name()
        self.gdb = DatabaseConnector()
        self.db = self.gdb.connect_db(self.database)
    
    def change_db(self, dbname):
        self.database(dbname)
        self.db = self.gdb.connect_db(self.database)

    def get_all_movies(self):
        nebula_movies = []
        query = 'FOR doc IN Movies RETURN doc'
        cursor = self.db.aql.execute(query)
        for data in cursor:
            nebula_movies.append(data['_id'])
        return(nebula_movies)
    
    def get_movie(self, movie_id):
        query = 'FOR doc IN Movies FILTER doc._id == "{}" RETURN doc'.format(movie_id)
        cursor = self.db.aql.execute(query)
        for data in cursor:
            #print(data)
            metadata = data
        return(metadata)

    def get_movie_url(self, movie_id):
        url = ""
        query = 'FOR doc IN Movies FILTER doc._id == "{}" RETURN doc.url_path'.format(movie_id)
        cursor = self.db.aql.execute(query)
        for data in cursor:
            #print(data)
            url = data
        #print(url)
        return(url)

    def get_scene_from_collection(self, movie_id, scene_element, collection):
        results = {}
        query = 'FOR doc IN {} FILTER doc.movie_id == "{}" AND doc.scene_element == {} RETURN doc'.format(collection,movie_id, scene_element)
        #print(query)
        cursor = self.db.aql.execute(query)
        for doc in cursor:
            results.update(doc)
        return (results)

    def get_scene_elements(self, movie_id):
        query = 'FOR doc IN Movies FILTER doc._id == "{}" RETURN doc'.format(movie_id)
        cursor = self.db.aql.execute(query)
        stages = []
        for  movie in cursor:
            for scene_element in movie['scene_elements']:
                stages.append(scene_element)
        return(stages)
    
    def get_mdfs(self, movie_id):
        query = 'FOR doc IN Movies FILTER doc._id == "{}" RETURN doc'.format(movie_id)
        cursor = self.db.aql.execute(query)
        stages = []
        for  movie in cursor:
            for scene_element in movie['mdfs']:
                stages.append(scene_element)
        return(stages)
    
    def get_movie_metadata(self, movie_id):
        query = 'FOR doc IN Movies FILTER doc._id == "{}" RETURN doc'.format(movie_id)
        cursor = self.db.aql.execute(query)
        stages = []
        for  movie in cursor:
            stages.append(movie['meta'])
        return(stages)