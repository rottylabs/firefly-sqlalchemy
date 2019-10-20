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

from sqlalchemy.engine import Connection
from sqlalchemy.orm import sessionmaker, Session


class SessionFactory:
    _sessionmaker: sessionmaker = None

    def __init__(self):
        self._session = None

    def __call__(self, bind: Connection = None):
        if self._session is None:
            self._session = self._sessionmaker(bind=bind)
        return self._session

    def clear(self):
        self._session = None

    def set_session(self, session: Session):
        self._session = session
