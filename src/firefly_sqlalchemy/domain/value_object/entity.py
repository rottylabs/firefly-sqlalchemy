from __future__ import annotations

from dataclasses import dataclass, fields
from typing import TypeVar, List, Type, get_type_hints, Dict

import firefly as ff
import inflection

import firefly_sqlalchemy as sql

E = TypeVar('E', bound=ff.Entity)


@dataclass
class Entity:
    entity: Type[E] = ff.required()
    fields: List[sql.EntityField] = ff.list_()

    def __post_init__(self):
        annotations_ = get_type_hints(self.entity)
        for field_ in fields(self.entity):
            self.fields.append(sql.EntityField(entity=self, field=field_, annotations=annotations_))

    @property
    def type(self):
        return self.entity

    @property
    def primary_key_column(self):
        for field_ in self.fields:
            if field_.is_pk():
                return field_

    @property
    def table_name(self):
        return inflection.tableize(self.entity.__name__)

    @property
    def fk_column_string(self):
        return f'{self.table_name}.{self.primary_key_column.name}'

    @property
    def foreign_id_column_name(self):
        return f'{self.entity.__name__.lower()}_id'

    def get_field(self, name: str):
        for f in self.fields:
            if f.name == name:
                return f

    def get_relationship_fields(self) -> List[sql.EntityField]:
        ret = []
        for field_ in self.fields:
            if field_.sqlalchemy_type is None:
                ret.append(field_)
        return ret

    def add_id_column(self, field_: sql.EntityField, foreign_entity: sql.Entity):
        name = f'{field_.name}_id'
        setattr(self.entity, name, None)

    def __eq__(self, other):
        try:
            if issubclass(other, ff.Entity):
                return self.entity == other
        except TypeError:
            pass

        try:
            if isinstance(other, sql.Entity):
                return self.entity == other.entity
        except TypeError:
            pass

        return False
