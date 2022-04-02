import datetime
import uuid
from datetime import timedelta

from whoopbot.actions.lock import process_lock_action
from whoopbot.models import LockedResource, OrgResource


def test_lock_resource_default_env(db_session):
    """
    Test locking a resource for a default environment
    """
    # Create a resource
    resource = OrgResource(
        resource_name="service_name",
        environment="Default",
    )
    db_session.add(resource)
    db_session.commit()

    user_id = uuid.uuid4().hex
    params = ["service_name"]
    result = process_lock_action(db_session, user_id, params)
    expected_result = f"{user_id} has locked service_name " \
                      f"for Default environment"
    assert expected_result in result


def test_lock_resource_for_env(db_session):
    """
    Test locking a resource for an environment
    """
    # Create a resource
    resource = OrgResource(
        resource_name="service_name",
        environment="staging",
    )
    db_session.add(resource)
    db_session.commit()

    user_id = uuid.uuid4().hex
    params = ["service_name", "staging"]
    result = process_lock_action(db_session, user_id, params)
    expected_result = f"{user_id} has locked service_name " \
                      f"for staging environment"
    assert expected_result in result


def test_lock_failed_due_to_existing_lock_by_same_user(db_session):
    """
    Test lock failure due to an existing lock.
    """
    user_id = uuid.uuid4().hex
    params = ["service_name", "staging"]

    # Create a resource
    resource = OrgResource(
        resource_name="service_name",
        environment="staging",
    )
    db_session.add(resource)
    db_session.commit()

    db_session.refresh(resource)

    current_time = datetime.datetime.now()
    expiration_time = current_time + timedelta(days=1)
    locked_resource = LockedResource(
        org_resource_id=resource.id,
        owner_id=user_id,
        locked_at=current_time,
        expires_at=expiration_time,
    )
    db_session.add(locked_resource)
    db_session.commit()

    result = process_lock_action(db_session, user_id, params)
    expected_result = f"Resource service_name for staging environment " \
                      f"is already locked by you"

    assert expected_result in result


def test_lock_failed_due_to_existing_lock_by_diff_user(db_session):
    """
    Test case where lock fails due to existing lock by a different user.
    """
    user_id = uuid.uuid4().hex
    params = ["service_name", "staging"]

    # Create a resource
    resource = OrgResource(
        resource_name="service_name",
        environment="staging",
    )
    db_session.add(resource)
    db_session.commit()

    db_session.refresh(resource)

    current_time = datetime.datetime.now()
    expiration_time = current_time + timedelta(days=1)
    locked_resource = LockedResource(
        org_resource_id=resource.id,
        owner_id="some_other_user",
        locked_at=current_time,
        expires_at=expiration_time,
    )
    db_session.add(locked_resource)
    db_session.commit()

    result = process_lock_action(db_session, user_id, params)
    expected_result = f"Resource service_name for staging environment " \
                      f"is already locked by some_other_user"

    assert expected_result in result
