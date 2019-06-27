import firefly as ff
import firefly_sqlalchemy as sql


@ff.cli(app_id='firefly')
class FireflySqlalchemyCli:

    @ff.cli(description='Object-Relational Mapper tools')
    class Orm:

        @ff.cli(for_=sql.CreateTables)
        def create_tables(self):
            pass
