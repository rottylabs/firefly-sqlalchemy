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
    priority: int = ff.optional()
    deleted: bool = ff.optional(default=False)


@dataclass
class Category(ff.Entity):
    id: str = ff.pk()
    name: str = ff.required()
    widgets: List[Widget] = ff.list_()


@dataclass
class Part(ff.Entity):
    id: str = ff.pk()
    widget: Widget = None
