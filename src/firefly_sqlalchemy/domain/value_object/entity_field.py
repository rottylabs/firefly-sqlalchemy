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

import datetime
from dataclasses import dataclass, Field
from typing import TypeVar

import firefly as ff
from sqlalchemy import String, Text, Boolean, Float, Integer, DateTime, Date

import firefly_sqlalchemy as sql

E = TypeVar('E', bound=ff.Entity)


@dataclass
class EntityField:
    entity: sql.Entity = ff.required()
    field: Field = ff.required()
    annotations: dict = ff.required()

    def __post_init__(self):
        pass

    def __getattr__(self, item):
        return getattr(self.field, item)

    @property
    def fk_column_string(self):
        return f'{self.entity.table_name}.{self.field.name}'

    def is_list(self):
        type_ = self.annotations[self.field.name]
        if hasattr(type_, '__dict__') and '_name' in type_.__dict__ and type_.__dict__['_name'] == 'List':
            return True

        return False

    def type(self):
        t = self.annotations[self.field.name]
        if self.is_list():
            return t.__dict__['__args__'][0]
        return t

    def is_pk(self):
        return self.field.metadata.get('pk', False)

    @property
    def sqlalchemy_type(self):
        try:
            return self._sqlalchemy_type()
        except sql.UnknownColumnType:
            return None

    def _sqlalchemy_type(self):
        type_ = self.annotations[self.field.name]

        if type_ == str:
            if 'length' in self.field.metadata:
                return String(length=self.field.metadata.get('length'))
            else:
                return Text

        if type_ == bool:
            return Boolean

        if type_ == float:
            if 'precision' in self.field.metadata:
                return Float(precision=self.field.metadata.get('precision'))
            return Float

        if type_ == int:
            return Integer

        if type_ == datetime.datetime:
            return DateTime

        if type_ == datetime.date:
            return Date

        raise sql.UnknownColumnType(self.field.type)
