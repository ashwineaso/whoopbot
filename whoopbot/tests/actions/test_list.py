from whoopbot.actions.list import process_list_resources
from whoopbot.models import OrgResource


def test_list_resource(db_session):
    """
    Test case to list all resources
    """

    resource = OrgResource(
        resource_name="resource_1",
        environment="environment_1",
    )
    db_session.add(resource)
    db_session.commit()

    resource = OrgResource(
        resource_name="resource_2",
        environment="environment_2",
    )
    db_session.add(resource)
    db_session.commit()

    result = process_list_resources(db_session)
    expected_result = "Resources added by the organization:\n" \
        "• resource_1 - environment_1" \
        "\n• resource_2 - environment_2"

    assert result == expected_result


def test_list_empty_resources(db_session):
    """
    Test case to list resources when there are no resources
    """

    result = process_list_resources(db_session)
    expected_result = "No resources added yet"
    assert result == expected_result
