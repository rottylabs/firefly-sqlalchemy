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

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

import firefly as ff

import firefly_sqlalchemy as sql

E = TypeVar('E', bound=ff.Entity)


@dataclass
class Relationship:
    ONE_TO_ONE = 1
    ONE_TO_MANY = 2
    MANY_TO_ONE = 3
    MANY_TO_MANY = 4

    entity_a: sql.Entity = ff.required()
    field_a: sql.EntityField = ff.required()
    entity_b: sql.Entity = ff.required()
    field_b: sql.EntityField = ff.optional()
    type: int = None
    _join_table: sql.JoinTable = None

    def __post_init__(self):
        self._initialize()

    def _initialize(self):
        has_many = False
        found_inverse = False
        for field_ in self.entity_b.get_relationship_fields():
            if field_.type() == self.entity_a.type:
                self.field_b = field_
                found_inverse = True
                if field_.is_list():
                    has_many = True
                break

        if self.field_a.is_list():
            if has_many:
                self.type = self.MANY_TO_MANY
            elif found_inverse:
                self.type = self.ONE_TO_MANY
        else:
            self.entity_a.add_id_column(self.field_a, self.entity_b)
            if has_many:
                self.type = self.MANY_TO_ONE
            elif found_inverse:
                self.type = self.ONE_TO_ONE

        if self.type is None:
            raise RuntimeError('Could not determine relationship type')

    @property
    def is_bidirectional(self):
        return self.field_b is not None

    @property
    def join_table(self):
        return self._join_table

    @join_table.setter
    def join_table(self, value: sql.JoinTable):
        if self.type != self.MANY_TO_MANY:
            raise sql.MappingError('Many to many relationships do not use a join table')
        self._join_table = value

    @property
    def needs_uselist(self):
        fields = [self.field_a.name, self.field_b.name]
        fields.sort()
        return self.field_a.name == fields[0]
