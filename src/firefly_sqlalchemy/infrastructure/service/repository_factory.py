import firefly as ff
from sqlalchemy.orm import Session

from .sqlalchemy_repository import SqlalchemyRepository


class RepositoryFactory(ff.RepositoryFactory):
    _session: Session = None

    def __init__(self):
        self.cache = {}

    def __call__(self, type_: type) -> SqlalchemyRepository:
        if type_ not in self.cache:
            class Repo(SqlalchemyRepository[type_]):
                pass
            self.cache[type_] = Repo()
            self.cache[type_].set_session(self._session)
        return self.cache[type_]
