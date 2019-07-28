import firefly as ff
import firefly.infrastructure as ffi
import pytest


@pytest.fixture(scope="session")
def firefly_configuration():
    return {
        'contexts': {
            'test': {
                'entity_module': 'tests.entities',
                'container_module': 'firefly_sqlalchemy.application',
                'extensions': {
                    'firefly_sqlalchemy': {
                        'db_type': 'sqlite',
                        'db_host': '',
                    }
                }
            },
        },
        'extensions': {
            'firefly_sqlalchemy': None,
        },
    }


@pytest.fixture(scope="session")
def container(firefly_configuration):
    from firefly.application import Container
    Container.configuration = lambda self: ffi.MemoryConfiguration(firefly_configuration)
    return Container()


@pytest.fixture(scope="session")
def kernel(container):
    return ff.Kernel(container)


@pytest.fixture(scope="session")
def context_map(kernel):
    return kernel.context_map


@pytest.fixture(scope="function", autouse=True)
def db(context_map, request):
    container = context_map.contexts['test'].container
    container.sqlalchemy_metadata.create_all(container.sqlalchemy_engine)

    def teardown():
        container.sqlalchemy_connection.clear()
        container.sqlalchemy_session.clear()
        container.sqlalchemy_engine.dispose()

    request.addfinalizer(teardown)


@pytest.fixture(scope="function")
def connection(context_map):
    return context_map.contexts['test'].container.sqlalchemy_connection()
