import pytest
from sqlalchemy import Text

from firefly_sqlalchemy import Entity
from .entities import Widget, Address, Category, Part


def test_props(sut: Entity):
    assert sut.fields[0].metadata == {'pk': True}
    assert sut.fields[0].fk_column_string == 'widgets.id'


def test_is_list(sut: Entity):
    assert sut.fields[0].is_list() is False
    assert sut.fields[2].is_list() is True


def test_type(sut: Entity):
    assert sut.fields[0].type() == str
    assert sut.fields[2].type() == Address
    assert sut.fields[3].type() == Category
    assert sut.fields[4].type() == Part


def test_sqlalchemy_type(sut: Entity):
    assert sut.fields[0].sqlalchemy_type == Text
    assert sut.fields[1].sqlalchemy_type == Text
    assert sut.fields[2].sqlalchemy_type is None
    assert sut.fields[3].sqlalchemy_type is None


@pytest.fixture()
def sut():
    return Entity(Widget)
