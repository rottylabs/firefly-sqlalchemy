import pytest

from firefly_sqlalchemy import Relationship


def test_props(sut: Relationship):
    assert sut.type == Relationship.ONE_TO_ONE


@pytest.fixture()
def sut(widget, part):
    return Relationship(
        entity_a=widget,
        field_a=widget.get_field('part'),
        entity_b=part,
        field_b=part.get_field('widget')
    )
