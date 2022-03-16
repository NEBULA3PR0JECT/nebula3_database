from arango import ArangoClient
from config import NEBULA_CONF

class DatabaseConnector():
    def __init__(self):
        config = NEBULA_CONF()
        self.arango_host = config.get_database_host()

    def connect_db(self, dbname):
        client = ArangoClient(hosts=self.arango_host)
        db = client.db(dbname, username='nebula', password='nebula')
        return (db)
    
    def init_new_db(self, dbname):
        client = ArangoClient(hosts=self.arango_host)
        sys_db = client.db('_system', username='root', password='nebula')

        if not sys_db.has_database(dbname):
            sys_db.create_database(
                dbname, users=[{'username': 'nebula', 'password': 'nebula', 'active': True}])

        db = client.db(dbname, username='nebula', password='nebula')

    def delete_db(self, dbname):
        client = ArangoClient(hosts='http://localhost:8529')
        # Connect to "_system" database as root user.
        # This returns an API wrapper for "_system" database.
        sys_db = client.db('_system', username='root', password='nebula')
        if not sys_db.has_database(dbname):
            print("NEBULADB not exist")
        else:
            sys_db.delete_database(dbname)

#For testing
def main():
    print()
    #
    vtdb = DatabaseConnector()
    #vtdb.delete_db()
    #vtdb.init_nebula_db('nebula_development')
    db = vtdb.connect_db('nebula_development')
    

if __name__ == '__main__':
    main()
