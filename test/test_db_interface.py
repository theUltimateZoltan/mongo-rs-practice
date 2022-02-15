from pytest import fixture
from db_interface import MongoWrapper


@fixture(scope="module",  autouse=True)
def faker_seed():
    return 512


@fixture
def sample_size():
    return 12


@fixture
def sample_data(faker, sample_size):
    return [{
        "name": faker.name(),
        "long_text": faker.paragraph(),
        "age": faker.pyint(12, 99),
        "some_date": faker.date(),
        "some_time": faker.time(),
        "some_boolean": faker.pybool()
    } for _ in range(sample_size)]


@fixture
def collection():
    test_collection = MongoWrapper(collection=MongoWrapper.Collection.Test)
    return test_collection


@fixture(autouse=True)


def setup_teardown(collection):
    yield
    collection.delete_everything()
    collection.close()


def test_insert_then_found(sample_data, collection):
    collection.insert(sample_data[0])
    assert collection.contains(sample_data[0])


def test_find_not_inserted(sample_data, collection):
    collection.insert(sample_data[0])
    assert not collection.contains(sample_data[1])


def test_data_persistent(sample_data, collection):
    collection.insert(sample_data[0])
    another_conn = MongoWrapper(MongoWrapper.Collection.Test)
    assert another_conn.contains(sample_data[0])
