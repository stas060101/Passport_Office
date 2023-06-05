import pytest
from passport_office.models import Base
from manager_lib.lib import get_connection_string
from sqlalchemy import create_engine


@pytest.fixture(scope="session")
def import_db_models():

    """This fixture is responsible for importing the necessary DB models. You can and should extend items listed here"""

    return []


@pytest.fixture(scope="session")
def db_engine():
    connstr = get_connection_string("passport_office_test")
    test_engine = create_engine(connstr, pool_size=200)

    yield test_engine
    test_engine.dispose()


@pytest.fixture(scope="session")
def tables(import_db_models, db_engine):

    Base.metadata.create_all(db_engine)
    yield
    Base.metadata.drop_all(db_engine)
