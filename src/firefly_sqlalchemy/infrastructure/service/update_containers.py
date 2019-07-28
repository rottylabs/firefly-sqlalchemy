from __future__ import annotations

import firefly as ff
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.orm import sessionmaker, Session

import firefly_sqlalchemy as fsi


@ff.listener(ff.ContextsLoaded)
class UpdateContainers(ff.Service):
    _context_map: ff.ContextMap = None

    def __call__(self, **kwargs):
        for context in self._context_map.contexts.values():
            config = context.config
            if isinstance(config, dict) and 'extensions' in config and 'firefly_sqlalchemy' in config['extensions']:
                self._update_container(context, config)

    def _update_container(self, context: ff.Context, config: dict):
        container = context.container
        params = config.get('extensions', {}).get('firefly_sqlalchemy', {})

        c = container.__class__
        c.__annotations__ = {}
        c.sqlalchemy_engine_factory = lambda self: self.build(fsi.EngineFactory, **params)
        c.__annotations__['sqlalchemy_engine_factory'] = fsi.EngineFactory
        c.sqlalchemy_engine = lambda self: self.sqlalchemy_engine_factory.create(False)
        c.__annotations__['sqlalchemy_engine'] = Engine
        c.sqlalchemy_connection = fsi.ConnectionFactory
        c.__annotations__['sqlalchemy_connection'] = fsi.ConnectionFactory
        c.sqlalchemy_sessionmaker = lambda self: sessionmaker(bind=self.sqlalchemy_engine)
        c.__annotations__['sqlalchemy_sessionmaker'] = sessionmaker
        c.sqlalchemy_session = fsi.SessionFactory
        c.__annotations__['sqlalchemy_session'] = fsi.SessionFactory
        c.sqlalchemy_metadata = lambda self: MetaData(bind=self.sqlalchemy_engine)
        c.__annotations__['sqlalchemy_metadata'] = MetaData

        # TODO registry repository factory only for entities that are configured to use it.
        self._context_map.extensions['firefly'].container.registry.set_default_factory(
            container.build(fsi.RepositoryFactory)
        )

    def _find_sqlalchemy_config(self, context_name: str):
        if context_name not in self._context_map.contexts:
            return

        config = self._context_map.get_context(context_name).config
        if isinstance(config, dict) and 'extensions' in config and 'firefly_sqlalchemy' in config['extensions']:
            return config.get('extensions').get('firefly_sqlalchemy')

        config = self._context_map.get_context('firefly_sqlalchemy').config
        if isinstance(config, dict) and 'default' in config:
            return config.get('default')
