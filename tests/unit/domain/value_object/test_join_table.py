import pytest

from firefly_sqlalchemy import Relationship, JoinTable


def test_props(sut: JoinTable):
    assert sut.name == 'addresses_widgets'
    assert len(sut.columns) == 2


def test_equality(sut: JoinTable, widget, address):
    jt = JoinTable(Relationship(
        entity_a=address,
        field_a=address.fields[2],
        entity_b=widget,
        field_b=widget.fields[3]
    ))

    assert sut == jt


@pytest.fixture()
def sut(widget, address):
    relationship = Relationship(
        entity_a=widget,
        field_a=widget.fields[3],
        entity_b=address,
        field_b=address.fields[2]
    )
    return JoinTable(relationship=relationship)
