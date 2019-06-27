import firefly as ff


class FireflySqlalchemyError(ff.FrameworkError):
    pass


class UnknownColumnType(FireflySqlalchemyError):
    pass
