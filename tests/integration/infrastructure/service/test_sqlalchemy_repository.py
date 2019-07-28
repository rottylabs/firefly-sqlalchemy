import pytest

from firefly_sqlalchemy import SqlalchemyRepository
from tests.entities import Widget, Address, Category, Part


def test_add(sut: SqlalchemyRepository, connection):
    sut.add(Widget(name='foo'))
    sut.commit()
    results = connection.execute("select * from widgets").fetchall()

    assert len(results) == 1
    assert results[0][1] == 'foo'


def test_remove(sut: SqlalchemyRepository, connection):
    w = Widget(name='foo')
    sut.add(w).commit()

    assert len(connection.execute('select * from widgets').fetchall()) == 1

    sut.remove(w).commit()

    assert len(connection.execute('select * from widgets').fetchall()) == 0


def test_update(sut: SqlalchemyRepository, connection):
    w = Widget(name='foo')
    sut.add(w).commit()
    id_ = w.id
    w = sut.find(id_)
    w.name = 'bar'
    sut.update(w).commit()

    assert len(connection.execute('select * from widgets').fetchall()) == 1
    assert len(connection.execute("select * from widgets where name = 'bar'").fetchall()) == 1


def test_many_to_many(sut: SqlalchemyRepository, connection, container):
    w = Widget(name='foo')
    w.addresses.append(Address(name='Address 1'))
    sut.add(w).commit()

    address = container.registry(Address).find(w.addresses[0].id)
    assert address.name == 'Address 1'
    assert address.widgets[0] is w

    assert len(connection.execute("select * from addresses").fetchall()) == 1
    assert len(connection.execute("select * from widgets").fetchall()) == 1
    assert len(connection.execute("select * from addresses_widgets").fetchall()) == 1

    address.widgets.append(Widget(name='bar'))
    container.registry(Address).update(address).commit()

    assert len(connection.execute("select * from addresses").fetchall()) == 1
    assert len(connection.execute("select * from widgets").fetchall()) == 2
    assert len(connection.execute("select * from addresses_widgets").fetchall()) == 2


def test_many_to_one(sut: SqlalchemyRepository, connection):
    w = Widget(name='foo')
    w.category = Category(name='cat1')
    sut.add(w).commit()

    assert len(connection.execute("select * from widgets").fetchall()) == 1
    assert len(connection.execute("select * from widgets where category_id is not null").fetchall()) == 1
    assert len(connection.execute("select * from categories").fetchall()) == 1

    w = sut.find(w.id)
    assert w.category.name == 'cat1'


def test_one_to_one(sut: SqlalchemyRepository, connection):
    p = Part()
    w = Widget(name='foo', part=p)
    sut.add(w).commit()

    assert len(connection.execute("select * from widgets").fetchall()) == 1
    assert len(connection.execute("select * from widgets where part_id is not null").fetchall()) == 1
    assert len(connection.execute("select * from parts").fetchall()) == 1


@pytest.fixture(scope="function")
def sut(container):
    return container.registry(Widget)
