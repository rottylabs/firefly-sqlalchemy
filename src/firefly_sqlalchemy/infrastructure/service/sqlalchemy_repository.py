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

from typing import TypeVar, List

from firefly import domain as ffd
from firefly.domain import Repository
from firefly.domain.error import NoResultFound
from firefly.domain.utils import retry
from sqlalchemy.exc import OperationalError, DatabaseError

import firefly_sqlalchemy as sql

T = TypeVar('T', bound=ffd.Entity)


class SqlalchemyRepository(Repository[T]):
    _session: sql.SessionFactory = None

    def __init__(self):
        self._criteria_parser = sql.CriteriaParser()

    def all(self) -> List[T]:
        return self._try_with_backoff(lambda: self._session().query(self._type()).all())

    def add(self, entity: T):
        self._session().add(entity)
        return self

    def remove(self, entity: T):
        self._session().delete(entity)
        return self

    def update(self, entity: T):
        self._session().add(entity)
        return self

    def find(self, uuid) -> T:
        if uuid is None:
            raise NoResultFound()

        ret = self._try_with_backoff(lambda: self._session().query(self._type()).get(uuid))
        if ret is None:
            raise NoResultFound()
        return ret

    def find_all_matching(self, criteria: ffd.BinaryOp) -> List[T]:
        q = self._session().query(self._type())
        q = self._criteria_parser.enhance_query(self._type(), criteria, q)
        return q.all()

    def find_one_matching(self, criteria: ffd.BinaryOp) -> T:
        q = self._session().query(self._type())
        q = self._criteria_parser.enhance_query(self._type(), criteria, q)
        return q.one()

    def commit(self):
        try:
            self._try_with_backoff(lambda: self._session().commit())
        except Exception as e:
            self._session().rollback()
            self._session().close()
            raise e

        return self

    def flush(self):
        self._session().flush()

    def _type(self):
        for b in self.__class__.__dict__['__orig_bases__']:
            if len(b.__dict__['__args__']) == 1:
                return b.__dict__['__args__'][0]

    def set_session_factory(self, session: sql.SessionFactory):
        self._session = session

    @staticmethod
    def _try_with_backoff(cb):
        return retry(cb, catch=(OperationalError, DatabaseError))
