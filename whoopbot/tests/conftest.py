import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from whoopbot import models


@pytest.fixture(scope="session")
def connection():
    engine = create_engine("sqlite:///:memory:")
    return engine.connect()


@pytest.fixture(scope="session")
def setup_database(connection):
    """Setup test database.

    Creates all database tables as declared in SQLAlchemy models,
    then proceeds to drop all the created tables after all tests
    have finished running.
    """
    models.Base.metadata.bind = connection
    models.Base.metadata.create_all()
    yield
    models.Base.metadata.drop_all()


@pytest.fixture()
def db_session(setup_database, connection):
    transaction = connection.begin()
    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection))
    transaction.rollback()
