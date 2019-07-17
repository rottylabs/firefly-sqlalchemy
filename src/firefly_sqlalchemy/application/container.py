import firefly_di as di

import firefly_sqlalchemy.infrastructure as fsi


class Container(di.Container):
    generate_mappings: fsi.GenerateMappings = fsi.GenerateMappings
    metadata_registry: fsi.MetadataRegistry = fsi.MetadataRegistry
