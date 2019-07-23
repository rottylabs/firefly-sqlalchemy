import pytest

from firefly_sqlalchemy import Table, Relationship


def test_props(sut: Table):
    assert sut.name == 'widgets'
    assert len(sut.columns) == 4


@pytest.fixture()
def sut(widget, address, category, part):
    return Table(entity=widget, relationships=[
        Relationship(entity_a=widget, field_a=widget.get_field('addresses'), entity_b=address,
                     field_b=address.get_field('widgets')),
        Relationship(entity_a=widget, field_a=widget.get_field('category'), entity_b=category,
                     field_b=part.get_field('widget')),
        Relationship(entity_a=widget, field_a=widget.get_field('part'), entity_b=part,
                     field_b=part.get_field('widget')),
    ])
