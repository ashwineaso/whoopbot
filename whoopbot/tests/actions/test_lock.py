import datetime
import uuid
from datetime import timedelta

from whoopbot.actions.lock import process_lock_action
from whoopbot.models import LockedResource, OrgResource


def test_lock_resource_default_env():
    """
    Test locking a resource for a default environment
    """
    # Create a resource
    org_resource = OrgResource(
        resource_name="service_name",
        environment="Default",
    )
    org_resource.save()

    user_id = uuid.uuid4().hex
    params = ["service_name"]
    result = process_lock_action(user_id, params)
    expected_result = f"{user_id} has locked service_name " \
                      f"for Default environment"
    assert expected_result in result


def test_lock_resource_for_env():
    """
    Test locking a resource for an environment
    """
    # Create a resource
    org_resource = OrgResource(
        resource_name="service_name",
        environment="staging",
    )
    org_resource.save()

    user_id = uuid.uuid4().hex
    params = ["service_name", "staging"]
    result = process_lock_action(user_id, params)
    expected_result = f"{user_id} has locked service_name " \
                      f"for staging environment"
    assert expected_result in result


def test_lock_failed_due_to_existing_lock_by_same_user():
    """
    Test lock failure due to an existing lock.
    """
    user_id = uuid.uuid4().hex
    params = ["service_name", "staging"]

    # Create a resource
    org_resource = OrgResource(
        resource_name="service_name",
        environment="staging",
    )
    org_resource.save()
    org_resource.refresh()

    current_time = datetime.datetime.now()
    expiration_time = current_time + timedelta(days=1)
    locked_resource = LockedResource(
        resource_name=org_resource.resource_name,
        environment=org_resource.environment,
        owner_id=user_id,
        locked_at=current_time,
        expires_at=expiration_time,
    )
    locked_resource.save()

    result = process_lock_action(user_id, params)
    expected_result = f"Resource service_name for staging environment " \
                      f"is already locked by you"

    assert expected_result in result


def test_lock_failed_due_to_existing_lock_by_diff_user():
    """
    Test case where lock fails due to existing lock by a different user.
    """
    user_id = uuid.uuid4().hex
    params = ["service_name", "staging"]

    # Create a resource
    org_resource = OrgResource(
        resource_name="service_name",
        environment="staging",
    )
    org_resource.save()
    org_resource.refresh()

    current_time = datetime.datetime.now()
    expiration_time = current_time + timedelta(days=1)
    locked_resource = LockedResource(
        resource_name=org_resource.resource_name,
        environment=org_resource.environment,
        owner_id="some_other_user",
        locked_at=current_time,
        expires_at=expiration_time,
    )
    locked_resource.save()
    locked_resource.refresh()

    result = process_lock_action(user_id, params)
    expected_result = f"Resource service_name for staging environment " \
                      f"is already locked by some_other_user"

    assert expected_result in result
