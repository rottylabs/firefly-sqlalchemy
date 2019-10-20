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

from firefly_sqlalchemy import Table, Relationship


def test_props(sut: Table):
    assert sut.name == 'widgets'
    assert len(sut.columns) == 6


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
