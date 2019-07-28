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
