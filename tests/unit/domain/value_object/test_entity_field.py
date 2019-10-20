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
from sqlalchemy import Text, String

from firefly_sqlalchemy import Entity
from tests.entities import Widget, Address, Category, Part


def test_props(sut: Entity):
    assert sut.fields[0].metadata == {'pk': True, 'length': 36}
    assert sut.fields[0].fk_column_string == 'widgets.id'


def test_is_list(sut: Entity):
    assert sut.fields[0].is_list() is False
    assert sut.fields[2].is_list() is True


def test_type(sut: Entity):
    assert sut.fields[0].type() == str
    assert sut.fields[2].type() == Address
    assert sut.fields[3].type() == Category
    assert sut.fields[4].type() == Part


def test_sqlalchemy_type(sut: Entity):
    assert isinstance(sut.fields[0].sqlalchemy_type, String)
    assert sut.fields[1].sqlalchemy_type == Text
    assert sut.fields[2].sqlalchemy_type is None
    assert sut.fields[3].sqlalchemy_type is None


@pytest.fixture()
def sut():
    return Entity(Widget)
