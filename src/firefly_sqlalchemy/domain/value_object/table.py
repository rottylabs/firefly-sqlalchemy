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
from typing import Type, TypeVar, List

from sqlalchemy import Column, String, ForeignKey, PrimaryKeyConstraint

import firefly_sqlalchemy as sql
import firefly as ff
import inflection

E = TypeVar('E', bound=ff.Entity)


@dataclass
class Table:
    entity: sql.Entity = ff.required()
    relationships: List[sql.Relationship] = ff.required()
    name: str = None
    columns: List[Column] = ff.list_()
    constraints: List = ff.list_()
    _pks: List[str] = ff.list_()

    def __post_init__(self):
        self._initialize()

    def _initialize(self):
        self.name = inflection.tableize(self.entity.entity.__name__)
        for field_ in self.entity.fields:
            st = field_.sqlalchemy_type
            if st is not None:
                self._build_regular_column(field_, st)
            elif self._needs_relation_column(field_):
                self._build_relation_column(field_)
        self._build_pk()

    def _build_pk(self):
        self.constraints.append(PrimaryKeyConstraint(*self._pks, name=f'{self.name}_pk'))

    def _build_regular_column(self, field_: sql.EntityField, sqlalchemy_type: Type):
        args = [field_.name, sqlalchemy_type]
        kwargs = {}
        if field_.is_pk():
            self._pks.append(field_.name)

        self.columns.append(Column(*args, **kwargs))

    def _needs_relation_column(self, field_: sql.EntityField):
        r = self._find_relationship(field_)
        if r.type == sql.Relationship.ONE_TO_ONE and not r.needs_uselist:
            return False

        return not field_.is_list() and r.type != sql.Relationship.MANY_TO_MANY

    def _build_relation_column(self, field_: sql.EntityField):
        name = f'{field_.name}_id'
        setattr(self.entity.entity, name, None)
        relationship = self._find_relationship(field_)
        table_name = inflection.tableize(relationship.entity_b.entity.__name__)
        self.columns.append(Column(name, String(length=36), ForeignKey(
            f'{table_name}.{relationship.entity_b.primary_key_column.name}'
        )))

    def _find_relationship(self, field_: sql.EntityField):
        for relationship in self.relationships:
            if relationship.field_a == field_:
                return relationship
        raise RuntimeError(f'Could not find relationship for field {field_.name}')
