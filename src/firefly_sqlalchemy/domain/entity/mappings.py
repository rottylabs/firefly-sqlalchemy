#  Copyright (c) 2019 JD Williams
#
#  This file is part of Firefly, a Python SOA framework built by JD Williams. Firefly is free software; you can
#  redistribute it and/or modify it under the terms of the GNU General Public License as published by the
#  Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#
#  Firefly is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
#  implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details. You should have received a copy of the GNU Lesser General Public
#  License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  You should have received a copy of the GNU General Public License along with Firefly. If not, see
#  <http://www.gnu.org/licenses/>.

from __future__ import annotations

from dataclasses import dataclass
from typing import List, TypeVar, Type, Dict

import firefly as ff
from sqlalchemy import Table
from sqlalchemy.orm import relationship, mapper

import firefly_sqlalchemy.domain as sql

E = TypeVar('E', bound=ff.Entity)


@dataclass
class Mappings(ff.AggregateRoot):
    relationships: List[sql.Relationship] = ff.list_()
    tables: List[sql.Table] = ff.list_()
    join_tables: Dict[str, sql.JoinTable] = ff.dict_()
    entities: List[sql.Entity] = ff.list_()

    def initialize(self, entities: List[Type[E]]):
        for entity in entities:
            self.entities.append(sql.Entity(entity))

        for entity in self.entities:
            relationships = []
            for field_ in entity.get_relationship_fields():
                relationships.append(self._create_relationship(entity, field_))
            self.tables.append(sql.Table(entity=entity, relationships=relationships))
            self.relationships.extend(relationships)

        for r in self.relationships:
            if r.type == sql.Relationship.MANY_TO_MANY:
                jt = sql.JoinTable(r)
                if jt not in self.join_tables:
                    r.join_table = jt
                    self.join_tables[jt.name] = jt
                else:
                    r.join_table = self.join_tables[jt.name]

    def add_mappings(self, metadata):
        for table in self.join_tables.values():
            table.sql_table = Table(table.name, metadata, *table.columns)
            setattr(self, table.name, table.sql_table)

        for table in self.tables:
            sql_table = Table(table.name, metadata, *table.columns, *table.constraints)
            props = {}
            for r in table.relationships:
                if r.type == sql.Relationship.MANY_TO_MANY:
                    props[r.field_a.name] = relationship(
                        r.entity_b.entity,
                        secondary=r.join_table.sql_table,
                        back_populates=r.field_b.name,
                        cascade='all'
                    )
                else:
                    args = [r.entity_b.entity]
                    kwargs = {'cascade': 'all'}
                    if r.field_b is not None:
                        kwargs['back_populates'] = r.field_b.name
                    if r.type == sql.Relationship.ONE_TO_ONE:
                        kwargs['uselist'] = False

                    props[r.field_a.name] = relationship(*args, **kwargs)

            mapper(table.entity.entity, sql_table, properties=props, primary_key=sql_table.primary_key)

    def _create_relationship(self, entity: sql.Entity, field_: sql.EntityField):
        entity_b = None
        for e in self.entities:
            if e == field_.type():
                entity_b = e
                break

        if entity_b is None:
            raise RuntimeError(f'Entity "{field_.type().__name__}" in relationship is unmapped.')

        return sql.Relationship(
            entity_a=entity,
            field_a=field_,
            entity_b=entity_b
        )
