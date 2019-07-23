from __future__ import annotations

from dataclasses import dataclass
from typing import Type, TypeVar, List

from sqlalchemy import Column, String, ForeignKey

import firefly_sqlalchemy as sql
import firefly as ff
import inflection

E = TypeVar('E', bound=ff.Entity)


@dataclass
class Table:
    entity: sql.Entity = ff.required()
    relationships: List[sql.Relationship] = ff.required()
    name: str = None
    columns: List[Column] = ff.list_()

    def __post_init__(self):
        self._initialize()

    def _initialize(self):
        self.name = inflection.tableize(self.entity.entity.__name__)
        for field_ in self.entity.fields:
            st = field_.sqlalchemy_type
            if st is not None:
                self.columns.append(self._build_regular_column(field_, st))
            elif self._needs_relation_column(field_):
                self.columns.append(self._build_relation_column(field_))

    @staticmethod
    def _build_regular_column(field_: sql.EntityField, sqlalchemy_type: Type):
        args = [field_.name, sqlalchemy_type]
        kwargs = {}
        if field_.is_pk():
            kwargs['primary_key'] = True

        return Column(*args, **kwargs)

    def _needs_relation_column(self, field_: sql.EntityField):
        return self._find_relationship(field_).type != sql.Relationship.MANY_TO_MANY

    def _build_relation_column(self, field_: sql.EntityField):
        name = f'{field_.name}_id'
        setattr(self.entity.entity, name, None)
        relationship = self._find_relationship(field_)
        table_name = inflection.tableize(relationship.entity_b.entity.__name__)
        return Column(name, String(), ForeignKey(
            f'{table_name}.{relationship.entity_b.primary_key_column.name}'
        ))

    def _find_relationship(self, field_: sql.EntityField):
        for relationship in self.relationships:
            if relationship.field_a == field_:
                return relationship
        raise RuntimeError(f'Could not find relationship for field {field_.name}')
