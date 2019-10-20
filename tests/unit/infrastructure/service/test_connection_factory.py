from unittest.mock import MagicMock

import pytest
from sqlalchemy.engine import Engine

from firefly_sqlalchemy import ConnectionFactory


def test_factory(sut: ConnectionFactory):
    sut()
    assert sut._engine.connect.call_count == 1


def test_caching(sut: ConnectionFactory):
    sut()
    sut()
    assert sut._engine.connect.call_count == 1


def test_clear(sut: ConnectionFactory):
    sut()
    sut.clear()
    sut()
    assert sut._engine.connect.call_count == 2


def test_set_connection(sut: ConnectionFactory):
    c = MagicMock()
    sut.set_connection(c)

    assert sut() is c


@pytest.fixture()
def sut():
    ret = ConnectionFactory()
    ret._engine = MagicMock(spec=Engine)

    return ret
