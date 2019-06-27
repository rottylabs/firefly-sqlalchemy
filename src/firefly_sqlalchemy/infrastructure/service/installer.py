import firefly as ff

from .update_containers import UpdateContainers
from .generate_mappings import GenerateMappings


class Installer(ff.Installer):
    _generate_mappings: GenerateMappings = None

    def __init__(self):
        self._update_containers = UpdateContainers()

    def containers_created(self, context: ff.Context, context_map: ff.ContextMap):
        self._update_containers(context, context_map)

    def ports_created(self, context: ff.Context, context_map: ff.ContextMap):
        pass

    def initialize_complete(self, context: ff.Context, context_map: ff.ContextMap):
        self._generate_mappings(context, context_map)
