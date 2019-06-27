from __future__ import annotations

from typing import Optional, Union

import firefly as ff
from firefly import domain as ffd

import firefly_sqlalchemy as sql


class CreateTables(ff.Service):
    _metadata_registry: sql.MetadataRegistry = None

    def __call__(self, context: str = None, **kwargs) -> Optional[Union[ffd.Message, object]]:
        for context_name, metadata in self._metadata_registry.all().items():
            if context is None or context == context_name:
                metadata.create_all()
        return
