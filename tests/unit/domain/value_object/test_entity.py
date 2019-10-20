#  Copyright (c) 2019 JD Williams
#
#  This file is part of Firefly, a Python SOA framework built by JD Williams. Firefly is free software; you can
#  redistribute it and/or modify it under the terms of the GNU General Public License as published by the
#  Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#
#  Firefly is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
#  implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details. You should have received a copy of the GNU Lesser General Public
#  License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  You should have received a copy of the GNU General Public License along with Firefly. If not, see
#  <http://www.gnu.org/licenses/>.

import pytest

from firefly_sqlalchemy import Entity
from tests.entities import Widget, Address


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
