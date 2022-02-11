import pytest
from db_interface import DoesNothing

def test_nothing():
    n = DoesNothing()
    n.do_nothing()