from pymongo import MongoClient

DB_NAME = "app_data"
DB_PORT = 27017
DB_HOST = "localhost"
DB_REPLICA_SET = "dbrs"

class MongoCollectionInterface:
    def __init__(self, collection: str ,client=None) -> None:
        self.__client = client or MongoCollectionInterface.__default_client()
        self.__collection = self.__client[DB_NAME][collection]

    @staticmethod
    def __default_client():
        return MongoClient(DB_HOST, DB_PORT, replicaset=DB_REPLICA_SET)

    def insert(self, record) -> None:
        return self.__collection.insert_one(record).inserted_id