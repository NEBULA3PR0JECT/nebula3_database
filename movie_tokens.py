from dataclasses import dataclass
from typing import List
from .database.arangodb import DatabaseConnector
from .config import NEBULA_CONF

@dataclass
class TokenEntry:
    movie_id: str
    scene_element: int = 0
    scene: int = 0
    expert: str = None
    bbox: list = None
    label: str = None
    meta_label: dict = None
    re_id: int = 0




class MovieTokens:
    def __init__(self, db = None):
        if db:
            self.db = db
        else:
            config = NEBULA_CONF()
            self.db_host = config.get_database_host()
            self.database = config.get_database_name()
            self.gdb = DatabaseConnector()
            self.db = self.gdb.connect_db(self.database)
            self.batch_size = config.get_db_save_batch_size()

    def get_movie_tokens(self, movie_id) -> list:
        tokens = list()
        query = 'FOR doc IN Token FILTER doc._id == "{}" RETURN doc'.format(movie_id)
        cursor = self.db.aql.execute(query)
        for data in cursor:
            tokens.append(data)
        return tokens

    def save_bulk_movie_tokens(self, movie_id, tokens: List[TokenEntry]):
        docs = []
        error = None
        result = None
        collection = self.db.collection(name = "Tokens")
        for token in tokens:
            movie_id_key = movie_id.split('/')[1]
            doc = { '_key':  f'{movie_id_key}:{token.scene_element}:{token.scene}:{token.label.replace(" ","_")}', **token.__dict__ }
            docs.append(doc)
        if len(docs):
            result = collection.import_bulk(docs)
        else:
            error = 'no documents to save'
        return (result, error)

    def save_movie_token(self, movie_id, token: TokenEntry):
        result = None
        collection = self.db.collection(name = "Tokens")
        movie_id_key = movie_id.split('/')[1]
        doc = { '_key':  f'{movie_id_key}:{token.scene_element}:{token.scene}:{token.label.replace(" ","_")}', **token.__dict__ }
        result = collection.insert(doc, overwrite_mode='update')
        return (result['_id'])

