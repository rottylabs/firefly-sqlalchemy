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
from typing import TypeVar, List

import firefly as ff
import inflection
from sqlalchemy import Column, String, ForeignKey, Table

import firefly_sqlalchemy as sql

E = TypeVar('E', bound=ff.Entity)


@dataclass
class JoinTable:
    relationship: sql.Relationship = ff.required()
    name: str = None
    columns: List[Column] = ff.list_()
    sql_table: Table = None

    def __post_init__(self):
        self._initialize()

    def _initialize(self):
        terms = [
            inflection.tableize(self.relationship.entity_a.entity.__name__),
            inflection.tableize(self.relationship.entity_b.entity.__name__),
        ]
        terms.sort()

        self.name = f'{terms[0]}_{terms[1]}'
        self.columns.append(Column(
            self.relationship.entity_a.foreign_id_column_name,
            String(length=36),
            ForeignKey(self.relationship.entity_a.fk_column_string)
        ))

        self.columns.append(Column(
            self.relationship.entity_b.foreign_id_column_name,
            String(length=36),
            ForeignKey(self.relationship.entity_b.fk_column_string)
        ))

    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.name
        return other.name == self.name

    def __hash__(self):
        return hash(self.name)
