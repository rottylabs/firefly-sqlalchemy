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
