from __future__ import annotations

import datetime
import importlib
from dataclasses import is_dataclass, fields, Field
from typing import Dict, List

import firefly as ff
from sqlalchemy.orm import mapper

import firefly_sqlalchemy as sql
import inflection
from sqlalchemy import MetaData, Column, String, Text, Boolean, Float, Integer, DateTime, Date, Table


class GenerateMappings(ff.LoggerAware):
    _metadata_registry: sql.MetadataRegistry = None

    def __init__(self):
        self.mappings = sql.Mappings()

    def __call__(self, context: ff.Context, context_map: ff.ContextMap):
        if context.name == 'firefly_sqlalchemy':
            return

        metadata = context_map.get_container(context.name).sqlalchemy_metadata
        self._map_entities(self._load_entities(context.name), metadata)
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

    def _map_entity(self, entity: type, metadata: MetaData):
        table_name = inflection.tableize(entity.__name__)
        columns = []
        for field in fields(entity):
            args = [
                field.name,
                self._get_sqlalchemy_type(field)
            ]
            kwargs = {}
            if field.metadata.get('pk', False):
                kwargs['primary_key'] = True

            columns.append(Column(*args, **kwargs))

        table = Table(table_name, metadata, *columns)
        setattr(self.mappings, table_name, table)
        mapper(entity, table)

    def _get_sqlalchemy_type(self, field: Field):
        if field.type == str:
            if 'length' in field.metadata:
                return String(length=field.metadata.get('length'))
            else:
                return Text

        if field.type == bool:
            return Boolean

        if field.type == float:
            if 'precision' in field.metadata:
                return Float(precision=field.metadata.get('precision'))
            return Float

        if field.type == int:
            return Integer

        if field.type == datetime.datetime:
            return DateTime

        if field.type == datetime.date:
            return Date

        raise sql.UnknownColumnType(field.type)
