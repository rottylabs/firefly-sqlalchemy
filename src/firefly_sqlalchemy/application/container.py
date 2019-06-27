import firefly_di as di
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.orm import sessionmaker, Session

import firefly_sqlalchemy.infrastructure as fsi


class Container(di.Container):
    # sqlalchemy_engine_factory: fsi.EngineFactory = lambda self: self.build(fsi.EngineFactory)
    # sqlalchemy_engine: Engine = lambda self: self.sqlalchemy_engine_factory.create(False)
    # sqlalchemy_connection: Connection = lambda self: self.sqlalchemy_engine.connect()
    # sqlalchemy_sessionmaker: sessionmaker = lambda self: sessionmaker(bind=self.sqlalchemy_engine)
    # sqlalchemy_session: Session = lambda self: self.sqlalchemy_sessionmaker()
    # sqlalchemy_metadata: MetaData = lambda self: MetaData(bind=self.sqlalchemy_engine)
    registry: fsi.Registry = fsi.Registry
    generate_mappings: fsi.GenerateMappings = fsi.GenerateMappings
    metadata_registry: fsi.MetadataRegistry = fsi.MetadataRegistry
