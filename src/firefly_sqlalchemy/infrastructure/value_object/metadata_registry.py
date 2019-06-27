from typing import Dict

from sqlalchemy import MetaData


class MetadataRegistry:
    def __init__(self):
        self._metadata = {}

    def add(self, context_name: str, metadata: MetaData):
        self._metadata[context_name] = metadata

    def get(self, context_name: str) -> MetaData:
        return self._metadata.get(context_name)

    def all(self) -> Dict[str, MetaData]:
        return self._metadata
