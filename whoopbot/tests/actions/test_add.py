from whoopbot.actions.add import process_action
from whoopbot.models import OrgResource


def test_add_new_resource(db_session):
    """
    Test adding a new resource to the database.
    """
    params = ["resource", "service_name", "for", "environment"]
    result = process_action(db_session, params)
    assert result == f"Resource {params[1]} added to {params[3]} environment"


def test_add_existing_resource(db_session):
    """
    Test adding an existing resource to the database.
    """
    params = ["resource", "service_name", "for", "environment"]

    org_resource = OrgResource(
        resource_name=params[1],
        environment=params[3],
    )
    db_session.add(org_resource)
    db_session.commit()

    result = process_action(db_session, params)
    assert result == f"Resource {params[1]} already exists " \
                     f"for {params[3]} environment"


def test_add_for_existing_default_environment(db_session):
    """
    Test adding a resource to the default environment.
    """
    params = ["resource", "service_name"]

    org_resource = OrgResource(
        resource_name=params[1],
        environment="Default",
    )
    db_session.add(org_resource)
    db_session.commit()

    result = process_action(db_session, params)
    assert result == f"Resource {params[1]} already exists " \
                     f"for Default environment"


def test_add_new_env_over_existing_default(db_session):
    """
    Test adding a resource to an environment that is not the default.
    """
    params = ["resource", "service_name", "for", "environment"]

    org_resource = OrgResource(
        resource_name=params[1],
        environment="Default",
    )
    db_session.add(org_resource)
    db_session.commit()

    result = process_action(db_session, params)
    assert result == f"Resource {params[1]} already exists " \
                     f"for Default environment"


def test_add_new_env_over_existing_non_default(db_session):
    """
    Test adding a resource to an environment that is not the default.
    """
    params = ["resource", "service_name", "for", "environment"]

    org_resource = OrgResource(
        resource_name=params[1],
        environment="Non-Default",
    )
    db_session.add(org_resource)
    db_session.commit()

    result = process_action(db_session, params)
    assert result == f"Resource {params[1]} added to {params[3]} environment"
