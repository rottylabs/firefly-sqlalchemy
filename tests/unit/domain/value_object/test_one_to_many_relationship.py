import pytest

from firefly_sqlalchemy import Relationship


def test_props(sut: Relationship):
    assert sut.type == Relationship.ONE_TO_MANY


@pytest.fixture()
def sut(widget, category):
    return Relationship(
        entity_a=category,
        field_a=category.get_field('widgets'),
        entity_b=widget
    )
