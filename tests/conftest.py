import pytest

from firefly_sqlalchemy import Entity
from .entities import Widget, Address, Part, Category


@pytest.fixture()
def widget():
    return Entity(Widget)


@pytest.fixture()
def address():
    return Entity(Address)


@pytest.fixture()
def part():
    return Entity(Part)


@pytest.fixture()
def category():
    return Entity(Category)
