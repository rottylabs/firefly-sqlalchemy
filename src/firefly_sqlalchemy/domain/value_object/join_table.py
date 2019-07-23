from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, List

import firefly as ff
import inflection
from sqlalchemy import Column, String, ForeignKey, Table

import firefly_sqlalchemy as sql

E = TypeVar('E', bound=ff.Entity)


@dataclass
class JoinTable:
    relationship: sql.Relationship = ff.required()
    name: str = None
    columns: List[Column] = ff.list_()
    sql_table: Table = None

    def __post_init__(self):
        self._initialize()

    def _initialize(self):
        terms = [
            inflection.tableize(self.relationship.entity_a.entity.__name__),
            inflection.tableize(self.relationship.entity_b.entity.__name__),
        ]
        terms.sort()

        self.name = f'{terms[0]}_{terms[1]}'
        self.columns.append(Column(
            self.relationship.entity_a.foreign_id_column_name,
            String(),
            ForeignKey(self.relationship.entity_a.foreign_id_column_name)
        ))

        self.columns.append(Column(
            self.relationship.entity_b.foreign_id_column_name,
            String(),
            ForeignKey(self.relationship.entity_b.foreign_id_column_name)
        ))

    def __eq__(self, other):
        return other.name == self.name