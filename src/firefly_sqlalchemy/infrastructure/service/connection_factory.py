from __future__ import annotations

from sqlalchemy.engine import Engine, Connection


class ConnectionFactory:
    _engine: Engine = None

    def __init__(self):
        self._connection = None

    def __call__(self):
        if self._connection is None:
            self._connection = self._engine.connect()
        return self._connection

    def clear(self):
        self._connection = None

    def set_connection(self, connection: Connection):
        self._connection = connection
