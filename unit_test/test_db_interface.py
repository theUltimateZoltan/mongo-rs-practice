from dataclasses import dataclass
from pytest import fixture
from db_interface import MongoCollectionInterface, DB_NAME
import mongomock

@fixture
def fake_client() -> mongomock.MongoClient:
    return mongomock.MongoClient()

@fixture
def interface(fake_client) -> MongoCollectionInterface:
    return MongoCollectionInterface("test", fake_client)

@fixture
def fake_client_collection(fake_client) -> mongomock.Collection:
    return fake_client[DB_NAME]["test"]

@fixture
def foobar_object() -> object:
    @dataclass
    class Foo:
        property: str
    return Foo("bar")

def insert_fake_entry(collection: mongomock.Collection) -> mongomock.ObjectId:
    return collection.insert_one({"name": "bob"}).inserted_id

def test_insert(fake_client_collection, interface):
    id = interface.insert({"name": "bob"})
    result=fake_client_collection.find_one({"_id": id})
    assert result
    assert result["name"] == "bob"

def test_delete_by_id(fake_client_collection, interface):
    id = insert_fake_entry(fake_client_collection)
    interface.delete_by_id(id)
    result = fake_client_collection.find_one(id)
    assert result is None

def test_update_by_id(fake_client_collection, interface):
    id = insert_fake_entry(fake_client_collection)
    interface.update_by_id(id, {"name": "alice", "age": 23})
    result = fake_client_collection.find_one(id)
    assert result["name"] == "alice" and result["age"] == 23

def test_get_id_for_properties(fake_client_collection, interface):
    id = insert_fake_entry(fake_client_collection)
    retrieved_id = interface.get_first_id_for_properties({"name": "bob"})
    assert retrieved_id == id

def test_object_saving(fake_client_collection, interface, foobar_object):
    id = interface.save_object(foobar_object)
    result = fake_client_collection.find_one(id)
    assert result["property"] == foobar_object.property

def test_saved_object_dict_recovery(fake_client_collection, interface, foobar_object):
    id = insert_fake_entry(fake_client_collection)
    retrieved_dict = interface.recover_object_dict(id)
    assert retrieved_dict["name"] == "bob"

# TODO: abstract dataclass that can be stored and retrieved automatically