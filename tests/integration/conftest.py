#  Copyright (c) 2019 JD Williams
#
#  This file is part of Firefly, a Python SOA framework built by JD Williams. Firefly is free software; you can
#  redistribute it and/or modify it under the terms of the GNU General Public License as published by the
#  Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#
#  Firefly is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
#  implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details. You should have received a copy of the GNU Lesser General Public
#  License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  You should have received a copy of the GNU General Public License along with Firefly. If not, see
#  <http://www.gnu.org/licenses/>.

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
