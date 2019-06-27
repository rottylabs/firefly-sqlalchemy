from __future__ import annotations

import firefly as ff
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.orm import sessionmaker, Session

import firefly_sqlalchemy as fsi


class UpdateContainers:
    def __call__(self, context: ff.Context, context_map: ff.ContextMap):
        config = self._find_sqlalchemy_config(context, context_map)
        if config is None:
            return

        container = context_map.get_container(context.name)
        if container is None:
            return

        container = container.__class__
        container.__annotations__ = {}
        container.sqlalchemy_engine_factory = lambda self: self.build(fsi.EngineFactory, **config)
        container.__annotations__['sqlalchemy_engine_factory'] = fsi.EngineFactory
        container.sqlalchemy_engine = lambda self: self.sqlalchemy_engine_factory.create(False)
        container.__annotations__['sqlalchemy_engine'] = Engine
        container.sqlalchemy_connection = lambda self: self.sqlalchemy_engine.connect()
        container.__annotations__['sqlalchemy_connection'] = Connection
        container.sqlalchemy_sessionmaker = lambda self: sessionmaker(bind=self.sqlalchemy_engine)
        container.__annotations__['sqlalchemy_sessionmaker'] = sessionmaker
        container.sqlalchemy_session = lambda self: self.sqlalchemy_sessionmaker()
        container.__annotations__['sqlalchemy_session'] = Session
        container.sqlalchemy_metadata = lambda self: MetaData(bind=self.sqlalchemy_engine)
        container.__annotations__['sqlalchemy_metadata'] = MetaData
        container.registry = fsi.Registry
        container.__annotations__['registry'] = fsi.Registry

    @staticmethod
    def _find_sqlalchemy_config(context: ff.Context, context_map: ff.ContextMap):
        if 'extensions' in context.config and 'firefly_sqlalchemy' in context.config['extensions']:
            return context.config.get('extensions').get('firefly_sqlalchemy')

        config = context_map.get_context('firefly_sqlalchemy').config
        if 'default' in config:
            return config.get('default')
