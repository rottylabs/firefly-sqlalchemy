import pytest
from firefly import Attr

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


def test_find_all_matching_equality(sut: SqlalchemyRepository, widgets):
    result = sut.find_all_matching(Attr('name') == 'foo')

    assert len(result) == 1
    assert result[0] is widgets['foo']


def test_find_one_matching_equality(sut: SqlalchemyRepository, widgets):
    assert sut.find_one_matching(Attr('name') == 'foo') is widgets['foo']


def test_find_all_matching_not_equal(sut: SqlalchemyRepository, widgets):
    result = sut.find_all_matching(Attr('name') != 'foo')

    assert len(result) == 3
    assert widgets['foo'] not in result


def test_find_all_matching_contains(sut: SqlalchemyRepository, widgets):
    result = sut.find_all_matching(Attr('name').contains('foo*'))

    assert len(result) == 2
    assert widgets['foo'] in result
    assert widgets['foobar'] in result


def test_find_all_matching_is_none(sut: SqlalchemyRepository, widgets):
    result = sut.find_all_matching(Attr('priority').is_none())

    assert len(result) == 1
    assert widgets['baz'] in result


def test_find_one_matching_is_none(sut: SqlalchemyRepository, widgets):
    assert sut.find_one_matching(Attr('priority').is_none()) is widgets['baz']


def test_find_all_matching_is_false(sut: SqlalchemyRepository, widgets):
    result = sut.find_all_matching(Attr('deleted').is_false())

    assert len(result) == 3
    assert widgets['baz'] not in result


def test_find_all_matching_is_true(sut: SqlalchemyRepository, widgets):
    result = sut.find_all_matching(Attr('deleted').is_true())

    assert len(result) == 1
    assert widgets['baz'] in result


def test_find_one_matching_is_true(sut: SqlalchemyRepository, widgets):
    assert sut.find_one_matching(Attr('deleted').is_true()) is widgets['baz']


def test_find_all_matching_in(sut: SqlalchemyRepository, widgets):
    result = sut.find_all_matching(Attr('name').is_in(['foo', 'foobar']))

    assert len(result) == 2
    assert widgets['foo'] in result
    assert widgets['foobar'] in result


def test_find_all_matching_gt(sut: SqlalchemyRepository, widgets):
    result = sut.find_all_matching(Attr('priority') > 1)

    assert len(result) == 2
    assert widgets['bar'] in result
    assert widgets['foobar'] in result


def test_find_all_matching_lt(sut: SqlalchemyRepository, widgets):
    result = sut.find_all_matching(Attr('priority') < 3)

    assert len(result) == 2
    assert widgets['foo'] in result
    assert widgets['bar'] in result


def test_find_all_matching_gte(sut: SqlalchemyRepository, widgets):
    result = sut.find_all_matching(Attr('priority') >= 1)

    assert len(result) == 3
    assert widgets['foo'] in result
    assert widgets['bar'] in result
    assert widgets['foobar'] in result


def test_find_all_matching_lte(sut: SqlalchemyRepository, widgets):
    result = sut.find_all_matching(Attr('priority') <= 3)

    assert len(result) == 3
    assert widgets['foo'] in result
    assert widgets['bar'] in result
    assert widgets['foobar'] in result


def test_find_all_matching_and_clause(sut: SqlalchemyRepository, widgets):
    result = sut.find_all_matching((Attr('name').contains('foo*')) & (Attr('priority') > 1))

    assert len(result) == 1
    assert widgets['foobar'] in result


def test_find_one_matching_and_clause(sut: SqlalchemyRepository, widgets):
    assert sut.find_one_matching((Attr('name').contains('foo*')) & (Attr('priority') > 1)) is widgets['foobar']


def test_find_all_matching_or_clause(sut: SqlalchemyRepository, widgets):
    result = sut.find_all_matching((Attr('name') == 'foo') | (Attr('name') == 'baz'))

    assert len(result) == 2
    assert widgets['foo'] in result
    assert widgets['baz'] in result


def test_find_all_matching_and_or_clauses(sut: SqlalchemyRepository, widgets):
    result = sut.find_all_matching(
        (Attr('name').contains('foo*')) & ((Attr('priority') == 1) | (Attr('name') == 'foobar'))
    )

    assert len(result) == 2
    assert widgets['foo'] in result
    assert widgets['foobar'] in result


@pytest.fixture(scope="function")
def sut(container):
    return container.registry(Widget)


@pytest.fixture()
def widgets(sut):
    ret = {
        'foo': Widget(name='foo', priority=1),
        'bar': Widget(name='bar', priority=2),
        'foobar': Widget(name='foobar', priority=3),
        'baz': Widget(name='baz', deleted=True),
    }

    for w in ret.values():
        sut.add(w)
    sut.commit()

    return ret
