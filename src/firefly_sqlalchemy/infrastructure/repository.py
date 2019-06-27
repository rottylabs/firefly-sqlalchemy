from typing import TypeVar, List

from firefly.domain import Repository
from firefly.domain.error import NoResultFound
from firefly.domain.utils import retry
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.orm import Session

T = TypeVar('T')


class SqlalchemyRepository(Repository[T]):
    _session: Session = None

    def all(self) -> List[T]:
        return self._try_with_backoff(lambda: self._session.query(self._type()).all())

    def add(self, entity: T):
        self._session.add(entity)
        return self

    def remove(self, entity: T):
        self._session.delete(entity)
        return self

    def update(self, entity: T):
        self._session.add(entity)
        return self

    def find(self, uuid) -> T:
        if uuid is None:
            raise NoResultFound()

        ret = self._try_with_backoff(lambda: self._session.query(self._type()).get(uuid))
        if ret is None:
            raise NoResultFound()
        return ret

    def find_all_by(self, **kwargs) -> List[T]:
        return self._try_with_backoff(lambda: self._session.query(self._type()).filter_by(**kwargs).all())

    def find_one_by(self, **kwargs) -> T:
        from sqlalchemy.orm.exc import NoResultFound as Nrf
        try:
            return self._try_with_backoff(lambda: self._session.query(self._type()).filter_by(**kwargs).all())
        except Nrf:
            raise NoResultFound()

    def commit(self):
        try:
            self._try_with_backoff(lambda: self._session.commit())
        except Exception as e:
            self._session.rollback()
            self._session.close()
            raise e

        return self

    def flush(self):
        self._session.flush()

    def _type(self):
        for b in self.__class__.__dict__['__orig_bases__']:
            if len(b.__dict__['__args__']) == 1:
                return b.__dict__['__args__'][0]

    def set_session(self, session: Session):
        self._session = session

    @staticmethod
    def _try_with_backoff(cb):
        return retry(cb, catch=(OperationalError, DatabaseError))
