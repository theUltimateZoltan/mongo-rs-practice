import enum
from pymongo import MongoClient


class MongoWrapper:
    class Collection(enum.Enum):
        Test = "test_collection"

    def __init__(self, collection: Collection):
        self.__db_name = "test_app_db"
        self.__client = MongoClient("mongo_master", replicaset="dbrs")
        self.__collection = self.__client[self.__db_name][collection.value]

    def __repr__(self):
        return f"{self.__collection}"

    def insert(self, json_object):
        self.__collection.insert_one(json_object)

    def contains(self, json_object) -> bool:
        return bool(self.__collection.find_one(json_object))

    def delete_everything(self):
        pass

    def close(self):
        self.__client.close()


if __name__ == '__main__':
    test_collection = MongoWrapper(collection=MongoWrapper.Collection.Test)
    test_collection.insert({"a": 1, "b": 2})
    test_collection.close()
