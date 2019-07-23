import firefly as ff


class FireflySqlalchemyError(ff.FrameworkError):
    pass


class UnknownColumnType(FireflySqlalchemyError):
    pass


class MappingError(FireflySqlalchemyError):
    pass
