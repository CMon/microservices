import pytest

def pytest_addoption(parser):
    group = parser.getgroup('microservices')
    group.addoption("--databaseFile", dest='microservices_databaseFile', action="store", default=":memory:", help="Override database file to use for tests")

@pytest.fixture
def databaseFile(request):
    return request.config.option.microservices_databaseFile
