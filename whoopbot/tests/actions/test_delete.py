import datetime

from whoopbot.actions.delete import process_delete_action
from whoopbot.models import LockedResource, OrgResource


def test_delete_resource():
    """
    Test deleting a resource which is not locked
    """
    params = ["resource", "test_resource"]

    org_resource = OrgResource(
        resource_name="test_resource",
        environment="Default",
    )
    org_resource.save()

    result = process_delete_action(params)
    assert result == "Resource test_resource for Default environment deleted"


def test_delete_locked_resource():
    """
    Test deleting a resource which is locked

    Case where the resource should not be deleted if it is locked by a user.
    """
    params = ["resource", "test_resource", "for", "environment"]

    org_resource = OrgResource(
        resource_name="test_resource",
        environment="environment",
    )
    org_resource.save()
    org_resource.refresh()

    locked_resource = LockedResource(
        resource_name=org_resource.resource_name,
        environment=org_resource.environment,
        owner_id="user_1",
        expires_at=datetime.datetime.now() + datetime.timedelta(days=1),
    )
    locked_resource.save()
    locked_resource.refresh()

    result = process_delete_action(params)
    assert result == f"Resource test_resource " \
                     f"for {org_resource.environment} environment " \
                     f"is currently locked by {locked_resource.owner_id}"


def test_delete_resource_which_doesnt_exist():
    """
    Test deleting a resource which does not exist
    """

    params = ["resource", "test_resource"]
    result = process_delete_action(params)
    assert result == "Resource test_resource not found for Default environment"
