from pytest import fixture

pytest_plugins = ["docker_compose"]

@fixture
def mongo_master_pod(function_scoped_container_getter):
    return function_scoped_container_getter.get("mongo-master")


def test_basic_connectivity(mongo_master_pod):
    assert mongo_master_pod
    print(mongo_master_pod)