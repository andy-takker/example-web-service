import pytest
import uvloop

pytest_plugins = (
    "tests.plugins.factories.book",
    "tests.plugins.factories.user",
    "tests.plugins.instances.db",
    "tests.plugins.instances.faststream",
    "tests.plugins.instances.open_library",
    "tests.plugins.instances.nats",
    "tests.plugins.instances.redis",
    "tests.plugins.instances.rest",
    "tests.plugins.instances.services",
    "tests.plugins.instances.storages",
)


@pytest.fixture(scope="session")
def event_loop_policy():
    return uvloop.EventLoopPolicy()
