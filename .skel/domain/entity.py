import uuid
from datetime import datetime

from firefly.domain import Entity


class Widget(Entity):
    id: str = None
    name: str = None
    created_on: datetime = None

    def __init__(self, name: str):
        self.id = str(uuid.uuid1())
        self.name = name
        self.created_on = datetime.now()
