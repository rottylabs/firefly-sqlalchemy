from __future__ import annotations

from dataclasses import dataclass
from typing import List

import firefly as ff


@dataclass
class Address(ff.AggregateRoot):
    id: str = ff.pk()
    name: str = ff.required()
    widgets: List[Widget] = ff.list_()


@dataclass
class Widget(ff.AggregateRoot):
    id: str = ff.pk()
    name: str = ff.required()
    addresses: List[Address] = ff.list_()
    category: Category = None
    part: Part = None


@dataclass
class Category(ff.Entity):
    id: str = ff.pk()
    name: str = ff.required()
    widgets: List[Widget] = ff.list_()


@dataclass
class Part(ff.Entity):
    id: str = ff.pk()
    widget: Widget = None
