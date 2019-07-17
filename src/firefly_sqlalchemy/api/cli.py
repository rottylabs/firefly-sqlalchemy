import firefly as ff
import firefly_sqlalchemy as sql


@ff.cli(device_id='firefly')
class FireflySqlalchemyCli:

    @ff.cli(description='Object-Relational Mapper tools')
    class Orm:

        @ff.cli(target=sql.CreateTables)
        def create_tables(self):
            pass
