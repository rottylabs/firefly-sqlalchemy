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

import importlib
import inspect
from dataclasses import is_dataclass
from typing import List, Type, TypeVar

import firefly as ff

import firefly_sqlalchemy as sql

E = TypeVar('E', bound=ff.Entity)


@ff.on(ff.DomainEntitiesLoaded)
class GenerateMappings(ff.Service, ff.LoggerAware):
    _metadata_registry: sql.MetadataRegistry = None
    _context_map: ff.ContextMap = None

    def __init__(self):
        self._mappings = sql.Mappings()

    def __call__(self, context: str, **kwargs):
        if context not in self._context_map.contexts:
            return

        context = self._context_map.get_context(context)
        if context.name == 'firefly_sqlalchemy' or context.config is None:
            return

        metadata = context.container.sqlalchemy_metadata
        entities = self._load_entities(context.name, context.config)
        self._mappings.initialize(entities)
        self._mappings.add_mappings(metadata)
        self._metadata_registry.add(context.name, metadata)

    def _load_entities(self, context_name: str, config: dict) -> List[Type[E]]:
        self.debug(f'Loading entities for {context_name}')
        try:
            module_name = config.get('entity_module', '{}.domain.entity')
            module = importlib.import_module(module_name.format(context_name))
            return [cls for cls in module.__dict__.values() if
                    inspect.isclass(cls) and issubclass(cls, ff.Entity) and is_dataclass(cls)]
        except ImportError:
            self.debug('Import failed... ignoring')
            return []
