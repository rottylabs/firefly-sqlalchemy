import pytest

from firefly_sqlalchemy import Entity
from .entities import Widget, Address


def test_props(sut: Entity):
    assert sut.fk_column_string == 'widgets.id'
    assert sut.table_name == 'widgets'
    assert sut.foreign_id_column_name == 'widget_id'
    assert sut.primary_key_column.name == 'id'
    assert sut.type == Widget


def test_relationships(sut: Entity):
    relationships = sut.get_relationship_fields()
    assert len(relationships) == 3
    assert relationships[0].name == 'addresses'
    assert relationships[1].name == 'category'
    assert relationships[2].name == 'part'


def test_equality(sut: Entity):
    assert sut == Widget
    assert sut == sut
    assert sut == Entity(Widget)
    assert sut != Address
    assert sut != Entity(Address)


@pytest.fixture()
def sut():
    return Entity(entity=Widget)
