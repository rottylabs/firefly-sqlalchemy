import pytest

from firefly_sqlalchemy import Relationship


def test_props(sut: Relationship):
    assert sut.type == Relationship.MANY_TO_ONE


def test_id_column(sut: Relationship):
    assert hasattr(sut.entity_a.entity, 'category_id') is True


@pytest.fixture()
def sut(widget, category):
    return Relationship(
        entity_a=widget,
        field_a=widget.get_field('category'),
        entity_b=category
    )
