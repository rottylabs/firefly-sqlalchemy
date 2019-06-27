from datetime import datetime

from sqlalchemy import MetaData, Table, Column, String, Text, DateTime


class EntityMappings(object):
    def __init__(self, meta_data: MetaData):
        self.widget = Table('widget', meta_data,
                            Column('id', String(length=36), primary_key=True),
                            Column('name', Text()),
                            Column('created_on', DateTime(), default=datetime.now())
                            )
