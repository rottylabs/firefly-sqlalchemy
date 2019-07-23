import pytest

from firefly_sqlalchemy import Relationship


def test_props(sut: Relationship):
    assert sut.type == Relationship.MANY_TO_MANY


@pytest.fixture()
def sut(widget, address):
    return Relationship(
        entity_a=widget,
        field_a=widget.get_field('addresses'),
        entity_b=address,
        field_b=address.get_field('widgets')
    )
