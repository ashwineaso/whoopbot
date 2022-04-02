import datetime
import uuid

from sqlalchemy.orm import Session

from whoopbot.actions.delete import process_delete_action
from whoopbot.models import LockedResource, OrgResource


def test_delete_resource(db_session: Session):
    """
    Test deleting a resource which is not locked
    """
    params = ["resource", "test_resource"]

    org_resource = OrgResource(
        resource_name="test_resource",
        environment="Default",
    )
    db_session.add(org_resource)
    db_session.commit()

    result = process_delete_action(db_session, params)
    assert result == "Resource test_resource for Default environment deleted"


def test_delete_locked_resource(db_session: Session):
    """
    Test deleting a resource which is locked

    Case where the resource should not be deleted if it is locked by a user.
    """
    params = ["resource", "test_resource", "for", "environment"]

    org_resource = OrgResource(
        resource_name="test_resource",
        environment="environment",
    )
    db_session.add(org_resource)
    db_session.commit()
    db_session.refresh(org_resource)

    locked_resource = LockedResource(
        org_resource_id=org_resource.id,
        owner_id=uuid.uuid4().hex,
        expires_at=datetime.datetime.now() + datetime.timedelta(days=1),
    )
    db_session.add(locked_resource)
    db_session.commit()
    db_session.refresh(locked_resource)

    result = process_delete_action(db_session, params)
    assert result == f"Resource test_resource " \
                     f"for {org_resource.environment} environment" \
                     f"is currently locked by {locked_resource.owner_id}"


def test_delete_resource_which_doesnt_exist(db_session: Session):
    """
    Test deleting a resource which does not exist
    """

    params = ["resource", "test_resource"]
    result = process_delete_action(db_session, params)
    assert result == "Resource test_resource not found for Default environment"
