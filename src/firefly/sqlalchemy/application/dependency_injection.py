from firefly.application.dependency_injection import DIC

from src.firefly.infrastructure.sqlalchemy import Registry


class Container(DIC):
    registry: Registry = lambda c: Registry()


container = Container()
