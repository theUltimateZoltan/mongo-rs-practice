from unittest.mock import MagicMock
from pytest import fixture
from db_interface import MongoInterface

@fixture
def fake_client() -> MagicMock:
    return MagicMock(MongoClient)

def test_insert(fake_client: MagicMock):
    mongo = MongoInterface(fake_client)
    mongo.insert({"bob", 1})