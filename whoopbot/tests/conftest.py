import pytest

from whoopbot.models import OrgResource, LockedResource


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Setup test database.

    Creates all database tables as declared in SQLAlchemy models,
    then proceeds to drop all the created tables after all tests
    have finished running.
    """
    OrgResource.create_table(read_capacity_units=1, write_capacity_units=1)
    LockedResource.create_table(read_capacity_units=1, write_capacity_units=1)
    yield
    OrgResource.delete_table()
    LockedResource.delete_table()
