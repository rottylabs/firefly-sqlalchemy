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

from typing import Type, TypeVar

import firefly as ff
from sqlalchemy import or_, and_, null
from sqlalchemy.orm import Query

ENTITY = TypeVar('ENTITY', bound=ff.Entity)


class CriteriaParser:
    def __init__(self):
        self.query = None
        self.entity = None

    def enhance_query(self, entity: Type[ENTITY], criteria: ff.BinaryOp, query: Query):
        self.query = query
        self.entity = entity
        return query.filter(self._handle_binary_op(criteria))

    def _handle_binary_op(self, bo: ff.BinaryOp):
        if isinstance(bo.lhv, ff.BinaryOp):
            bo.lhv = self._handle_binary_op(bo.lhv)

        if isinstance(bo.rhv, ff.BinaryOp):
            bo.rhv = self._handle_binary_op(bo.rhv)

        if bo.op == 'or':
            return or_(bo.lhv, bo.rhv)

        if bo.op == 'and':
            return and_(bo.lhv, bo.rhv)

        return self._build_filter(bo)

    def _build_filter(self, bo: ff.BinaryOp):
        if bo.op == '==':
            if isinstance(bo.lhv, ff.AttributeString):
                return getattr(self.entity, bo.lhv) == bo.rhv
            return bo.lhv == getattr(self.entity, bo.rhv)

        if bo.op == '!=':
            if isinstance(bo.lhv, ff.AttributeString):
                return getattr(self.entity, bo.lhv) != bo.rhv
            return bo.lhv != getattr(self.entity, bo.rhv)

        if bo.op == 'contains':
            return getattr(self.entity, bo.lhv).like(bo.rhv.replace('*', '%'))

        if bo.op == 'is':
            if bo.rhv == 'None':
                return getattr(self.entity, bo.lhv).is_(null())

            if bo.rhv is False:
                return getattr(self.entity, bo.lhv).is_(False)

            if bo.rhv is True:
                return getattr(self.entity, bo.lhv).is_(True)

        if bo.op == 'in':
            return getattr(self.entity, bo.lhv).in_(bo.rhv)

        if bo.op == '>':
            if isinstance(bo.lhv, ff.AttributeString):
                return getattr(self.entity, bo.lhv) > bo.rhv
            return bo.lhv > getattr(self.entity, bo.rhv)

        if bo.op == '<':
            if isinstance(bo.lhv, ff.AttributeString):
                return getattr(self.entity, bo.lhv) < bo.rhv
            return bo.lhv < getattr(self.entity, bo.rhv)

        if bo.op == '>=':
            if isinstance(bo.lhv, ff.AttributeString):
                return getattr(self.entity, bo.lhv) >= bo.rhv
            return bo.lhv >= getattr(self.entity, bo.rhv)

        if bo.op == '<=':
            if isinstance(bo.lhv, ff.AttributeString):
                return getattr(self.entity, bo.lhv) <= bo.rhv
            return bo.lhv <= getattr(self.entity, bo.rhv)
