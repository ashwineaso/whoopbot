from whoopbot.actions.list import process_list_resources
from whoopbot.models import OrgResource


def test_list_resource():
    """
    Test case to list all resources
    """

    org_resource = OrgResource(
        resource_name="resource_1",
        environment="environment_1",
    )
    org_resource.save()

    org_resource = OrgResource(
        resource_name="resource_2",
        environment="environment_2",
    )
    org_resource.save()

    result = process_list_resources()
    expected_result = "Resources added by the organization:\n" \
        "• resource_1 - environment_1" \
        "\n• resource_2 - environment_2"

    assert result == expected_result


def test_list_empty_resources():
    """
    Test case to list resources when there are no resources
    """

    result = process_list_resources()
    expected_result = "No resources added yet"
    assert result == expected_result
