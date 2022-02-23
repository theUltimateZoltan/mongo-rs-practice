from pytest import fixture, mark
from compose.container import Container

pytest_plugins = ["docker_compose"]

@fixture
def mongo_master_pod(function_scoped_container_getter) -> Container:
    return function_scoped_container_getter.get("mongo-master")

@fixture
def mongo_interface_pod(function_scoped_container_getter) -> Container:
    return function_scoped_container_getter.get("mongo-interface")

@mark.skip(reason="Not implemented yet")
def test_basic_connectivity(mongo_master_pod: Container, mongo_interface_pod: Container):
    raise NotImplementedError