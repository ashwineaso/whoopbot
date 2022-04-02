import datetime
import uuid

from whoopbot.actions.release import process_release_action
from whoopbot.models import LockedResource, OrgResource


def test_release_locked_resource(db_session):
    """
    Test releasing a locked resource
    """
    user_id = uuid.uuid4().hex

    org_resource = OrgResource(
        resource_name="resource_name",
        environment="environment",
    )
    db_session.add(org_resource)
    db_session.commit()

    db_session.refresh(org_resource)

    locked_resource = LockedResource(
        owner_id=user_id,
        org_resource_id=org_resource.id,
        locked_at=datetime.datetime.utcnow(),
        expires_at=datetime.datetime.utcnow(),
    )
    db_session.add(locked_resource)
    db_session.commit()

    params = ["resource_name", "environment"]

    result = process_release_action(db_session, user_id, params)
    expected_result = (f"{user_id} has released resource_name "
                       f"for environment environment")

    assert result == expected_result


def test_failed_due_lock_by_diff_user(db_session):
    """
    Test failure due to resource being locked by different user
    """

    user_id = uuid.uuid4().hex
    user_id_2 = uuid.uuid4().hex

    org_resource = OrgResource(
        resource_name="resource_name",
        environment="environment",
    )
    db_session.add(org_resource)
    db_session.commit()

    db_session.refresh(org_resource)

    locked_resource = LockedResource(
        owner_id=user_id_2,
        org_resource_id=org_resource.id,
        locked_at=datetime.datetime.utcnow(),
        expires_at=datetime.datetime.utcnow(),
    )
    db_session.add(locked_resource)
    db_session.commit()

    params = ["resource_name", "environment"]

    result = process_release_action(db_session, user_id, params)
    expected_result = (
            f"Resource resource_name for environment environment "
            f"is locked by {user_id_2}. You can't release it"
    )

    assert result == expected_result
