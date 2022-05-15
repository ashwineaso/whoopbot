import datetime
import uuid

from whoopbot.actions.release import process_release_action
from whoopbot.models import LockedResource, OrgResource


def test_release_locked_resource():
    """
    Test releasing a locked resource
    """
    user_id = uuid.uuid4().hex

    org_resource = OrgResource(
        resource_name="resource_name",
        environment="environment",
    )
    org_resource.save()
    org_resource.refresh()

    locked_resource = LockedResource(
        resource_name=org_resource.resource_name,
        environment=org_resource.environment,
        owner_id=user_id,
        locked_at=datetime.datetime.utcnow(),
        expires_at=datetime.datetime.utcnow(),
    )
    locked_resource.save()

    params = ["resource_name", "environment"]

    result = process_release_action(user_id, params)
    expected_result = (f"{user_id} has released resource_name "
                       f"for environment environment")

    assert result == expected_result


def test_failed_due_lock_by_diff_user():
    """
    Test failure due to resource being locked by different user
    """

    user_id = uuid.uuid4().hex
    user_id_2 = uuid.uuid4().hex

    org_resource = OrgResource(
        resource_name="resource_name",
        environment="environment",
    )
    org_resource.save()
    org_resource.refresh()

    locked_resource = LockedResource(
        resource_name=org_resource.resource_name,
        environment=org_resource.environment,
        owner_id=user_id_2,
        locked_at=datetime.datetime.utcnow(),
        expires_at=datetime.datetime.utcnow(),
    )
    locked_resource.save()

    params = ["resource_name", "environment"]

    result = process_release_action(user_id, params)
    expected_result = (
            f"Resource resource_name for environment environment "
            f"is locked by {user_id_2}. You can't release it"
    )

    assert result == expected_result
