from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.pool import NullPool


class EngineFactory:
    def __init__(
            self,
            db_name: str = None,
            db_username: str = None,
            db_password: str = None,
            db_host: str = '',
            db_type: str = 'sqlite',
            db_port: str = ''
    ):
        self.host = db_host
        self.name = db_name
        self.user = db_username
        self.password = db_password
        self.db_type = db_type
        self.port = db_port

    def create(self, do_echo=False) -> Engine:
        if 'sqlite' == self.db_type and '' == self.host:
            import sqlite3

            @event.listens_for(Engine, "connect")
            def set_sqlite_pragma(connection, record):
                cursor = connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

            creator = lambda: sqlite3.connect('file::memory:?cache=shared', uri=True)
            return create_engine('sqlite:///:memory:', creator=creator, echo=do_echo, poolclass=NullPool)

        return create_engine(self.get_connection_string(), echo=do_echo, poolclass=NullPool)

    def get_connection_string(self):
        if self.db_type == 'sqlite':
            return f"sqlite:///{self.host}"

        return f"{self.db_type}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
