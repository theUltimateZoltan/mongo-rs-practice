from pymongo import MongoClient
from bson.objectid import ObjectId


DB_NAME = "app_data"
DB_PORT = 27017
DB_HOST = "localhost"
DB_REPLICA_SET = "dbrs"

class MongoCollectionInterface:
    def __init__(self, collection: str ,client=None) -> None:
        self.__client = client or MongoCollectionInterface.__default_client()
        self.__collection = self.__client[DB_NAME][collection]

    @staticmethod
    def __default_client() -> MongoClient:
        return MongoClient(DB_HOST, DB_PORT, replicaset=DB_REPLICA_SET)

    def insert(self, record) -> ObjectId:
        return self.__collection.insert_one(record).inserted_id
    
    def delete_by_id(self, record_id: ObjectId) -> None:
        self.__collection.delete_one({'_id': record_id})

    def update_by_id(self, record_id: ObjectId, updated_fields: dict) -> None:
        self.__collection.update_one({'_id': record_id}, {"$set": updated_fields})

    def get_first_id_for_properties(self, properties_to_search: dict) -> ObjectId:
        return self.__collection.find_one(properties_to_search)["_id"]