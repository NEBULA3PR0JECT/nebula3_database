from .database.arangodb import DatabaseConnector
from .config import NEBULA_CONF


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
