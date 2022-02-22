from pytest import fixture
from db_interface import MongoCollectionInterface, DB_NAME
import mongomock

@fixture
def fake_client():
    return mongomock.MongoClient()

def test_connection(fake_client):
    MongoCollectionInterface("test", client=fake_client)

def test_insert(fake_client):
    mongo = MongoCollectionInterface("test", fake_client)
    id = mongo.insert({"name": "bob"})
    result=fake_client[DB_NAME]["test"].find_one(id)
    assert result
    assert result["name"] == "bob"