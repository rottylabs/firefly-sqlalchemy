from __future__ import annotations

import datetime
import importlib
from dataclasses import is_dataclass, fields, Field
from typing import List, get_type_hints

import firefly as ff
import inflection
from sqlalchemy import MetaData, Column, String, Text, Boolean, Float, Integer, DateTime, Date, Table, ForeignKey
from sqlalchemy.orm import mapper, relationship

import firefly_sqlalchemy as sql


@ff.listener(ff.DomainEntitiesLoaded)
class GenerateMappings(ff.Service, ff.LoggerAware):
    _metadata_registry: sql.MetadataRegistry = None
    _context_map: ff.ContextMap = None

    def __init__(self):
        self._mappings = sql.Mappings()
        self._relationships = {}
        self._join_tables = {}
        self._foreign_keys = {}

    def __call__(self, context: str, **kwargs):
        print(context)
        if context not in self._context_map.contexts:
            return

        context = self._context_map.get_context(context)
        if context.name == 'firefly_sqlalchemy' or context.config is None:
            return

        metadata = context.container.sqlalchemy_metadata
        entities = self._load_entities(context.name)
        self._relationships = self._find_relationships(entities)
        self._create_join_tables(metadata)
        self._map_entities(entities, metadata)
        self._metadata_registry.add(context.name, metadata)

    def _load_entities(self, context_name: str) -> List[type]:
        self.debug(f'Loading entities for {context_name}')
        try:
            module = importlib.import_module(f'{context_name}.domain.entity')
            return [cls for cls in module.__dict__.values() if is_dataclass(cls)]
        except ImportError:
            self.debug('Import failed... ignoring')
            return []

    def _map_entities(self, entities: List[type], metadata: MetaData):
        for entity in entities:
            self._map_entity(entity, metadata)

    def _map_entity(self, entity, metadata: MetaData):
        annotations_ = get_type_hints(entity)
        table_name = inflection.tableize(entity.__name__)
        columns = []
        for field_ in fields(entity):
            args = [
                field_.name,
                self._get_sqlalchemy_type(entity, field_, annotations_)
            ]
            if args[1] is None:
                continue

            if entity in self._foreign_keys and field_.name in self._foreign_keys[entity]:
                args.append(ForeignKey(self._foreign_keys[entity][field_.name]))

            kwargs = {}
            if field_.metadata.get('pk', False):
                kwargs['primary_key'] = True

            columns.append(Column(*args, **kwargs))

        table = Table(table_name, metadata, *columns)
        setattr(self._mappings, table_name, table)

        props = {}
        if entity in self._relationships:
            for field_name, config in self._relationships[entity].items():
                if 'table' in config:
                    relation_name, relation = self._find_many_relation(config['type'], entity)
                    props[field_name] = relationship(
                        config['type'],
                        secondary=config['table'],
                        back_populates=relation_name,
                        cascade='all'
                    )
                elif config['rel'] == 'one':
                    # TODO Fix this
                    props[field_name] = relationship(
                        config['type'],
                        uselist=False
                    )

        mapper(entity, table, properties=props)

    def _get_sqlalchemy_type(self, entity, field_: Field, annotations_: dict):
        if entity in self._relationships and field_.name in self._relationships[entity]:
            return None

        type_ = annotations_[field_.name]

        if type_ == str:
            if 'length' in field_.metadata:
                return String(length=field_.metadata.get('length'))
            else:
                return Text

        if type_ == bool:
            return Boolean

        if type_ == float:
            if 'precision' in field_.metadata:
                return Float(precision=field_.metadata.get('precision'))
            return Float

        if type_ == int:
            return Integer

        if type_ == datetime.datetime:
            return DateTime

        if type_ == datetime.date:
            return Date

        raise sql.UnknownColumnType(field_.type)

    def _find_relationships(self, entities: list):
        relationships = {}

        for entity in entities:
            annotations_ = get_type_hints(entity)
            for field_ in fields(entity):
                try:
                    self._get_sqlalchemy_type(entity, field_, annotations_)
                    continue
                except sql.UnknownColumnType as e:
                    type_ = annotations_[field_.name]
                    rel = 'one'
                    if '_name' in type_.__dict__ and type_.__dict__['_name'] == 'List':
                        type_ = type_.__dict__['__args__'][0]
                        rel = 'many'

                    if is_dataclass(type_):
                        if entity not in relationships:
                            relationships[entity] = {}
                        relationships[entity][field_.name] = {
                            'type': type_,
                            'rel': rel,
                        }
                        if rel == 'one':
                            if entity not in self._foreign_keys:
                                self._foreign_keys[entity] = {}
                            self._foreign_keys[entity][f'{field_.name}_id'] = \
                                f'{inflection.tableize(type_.__name__)}.{self._get_primary_key_field(type_).name}'
                        continue

                    raise e

        return relationships

    def _create_join_tables(self, metadata):
        for entity, fields_ in self._relationships.items():
            for field_name, config in fields_.items():
                if 'table' in config:
                    continue
                if config['rel'] == 'many' and config['type'] in self._relationships:
                    field = self._get_primary_key_field(config['type'])
                    r_field_name, r_config = self._find_many_relation(config['type'], entity)
                    if r_config['rel'] == 'many':
                        l_field = self._get_primary_key_field(entity)
                        table_name = f'{inflection.tableize(entity.__name__)}_{inflection.tableize(config["type"].__name__)}'
                        join_table = Table(
                            table_name,
                            metadata,
                            Column(
                                f'{inflection.underscore(entity.__name__)}_{l_field.name}',
                                self._get_sqlalchemy_type(entity, l_field, get_type_hints(entity)),
                                ForeignKey(f'{inflection.tableize(entity.__name__)}.{l_field.name}')
                            ),
                            Column(
                                f'{inflection.underscore(config["type"].__name__)}_{field.name}',
                                self._get_sqlalchemy_type(config['type'], field, get_type_hints(config['type'])),
                                ForeignKey(f'{inflection.tableize(config["type"].__name__)}.{field.name}')
                            )
                        )
                        setattr(self._mappings, table_name, join_table)
                        self._relationships[entity][field_name]['table'] = join_table
                        self._relationships[config['type']][r_field_name]['table'] = join_table

    def _find_many_relation(self, other_type: type, self_type: type):
        print(other_type)
        print(self_type)
        for field_name, config in self._relationships[other_type].items():
            if config['rel'] == 'many' and config['type'] == self_type:
                return field_name, config

    def _get_primary_key_field(self, entity):
        for field_ in fields(entity):
            if 'pk' in field_.metadata:
                return field_

    def _get_primary_key_type(self, entity):
        annotations_ = get_type_hints(entity)
        field_ = self._get_primary_key_field(entity)
        if field_ is not None:
            return self._get_sqlalchemy_type(entity, field_, annotations_)
