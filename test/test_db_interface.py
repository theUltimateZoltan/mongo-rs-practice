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
    result=fake_client[DB_NAME]["test"].find_one({"_id": id})
    assert result
    assert result["name"] == "bob"

def test_delete_by_id(fake_client):
    mongo = MongoCollectionInterface("test", fake_client)
    id = fake_client[DB_NAME]["test"].insert_one({"name": "bob"}).inserted_id
    mongo.delete_by_id(id)
    result = fake_client[DB_NAME]["test"].find_one(id)
    assert result is None

def test_update_by_id(fake_client):
    mongo = MongoCollectionInterface("test", fake_client)
    id = fake_client[DB_NAME]["test"].insert_one({"name": "bob"}).inserted_id
    mongo.update_by_id(id, {"name": "alice", "age": 23})
    result = fake_client[DB_NAME]["test"].find_one(id)
    assert result["name"] == "alice" and result["age"] == 23

def test_get_id_for_properties(fake_client):
    mongo = MongoCollectionInterface("test", fake_client)
    id = fake_client[DB_NAME]["test"].insert_one({"name": "bob"}).inserted_id
    retrieved_id = mongo.get_first_id_for_properties({"name": "bob"})
    assert retrieved_id == id