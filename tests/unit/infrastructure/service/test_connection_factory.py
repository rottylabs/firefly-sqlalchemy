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

from unittest.mock import MagicMock

import pytest
from sqlalchemy.engine import Engine

from firefly_sqlalchemy import ConnectionFactory


def test_factory(sut: ConnectionFactory):
    sut()
    assert sut._engine.connect.call_count == 1


def test_caching(sut: ConnectionFactory):
    sut()
    sut()
    assert sut._engine.connect.call_count == 1


def test_clear(sut: ConnectionFactory):
    sut()
    sut.clear()
    sut()
    assert sut._engine.connect.call_count == 2


def test_set_connection(sut: ConnectionFactory):
    c = MagicMock()
    sut.set_connection(c)

    assert sut() is c


@pytest.fixture()
def sut():
    ret = ConnectionFactory()
    ret._engine = MagicMock(spec=Engine)

    return ret
