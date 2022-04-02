import datetime
from datetime import timedelta
from typing import List

import humanize
from sqlalchemy.orm import Session

from whoopbot.actions.base import Action
from whoopbot.db import SessionLocal
from whoopbot.models import LockedResource, OrgResource


class LockAction(Action):
    """
    Action to lock resource for an environment

    Syntax: /whoop lock <resource_name> <environment> <message> <duration>

    Eg: /whoop lock api-service
    Eg: /whoop lock api-service testing
    """

    DEFAULT_MESSAGE = (
        "The command to lock a resource is "
        "`/whoop lock <resource_name> <environment: optional> "
        "<message: optional> <duration: optional>`")

    def should_be_valid_length(self) -> bool:
        if len(self.params) in list(range(1, 4)):
            return True
        return False

    def is_valid(self) -> bool:
        if self.should_be_valid_length():
            return True
        return False

    def process(self) -> str:
        if not self.is_valid():
            return self.DEFAULT_MESSAGE

        return process_lock_action(
            SessionLocal(), self.user_id, self.params)


def process_lock_action(db: Session, user_id: str, params: List[str]) -> str:
    """Process the action to lock a resource."""

    if len(params) == 1:
        resource_name, environment = params[0], "Default"
    else:
        resource_name, environment = params[0], params[1]

    # Check if the resource exists for the environment
    resource = db.query(OrgResource).filter(
        OrgResource.resource_name == resource_name,
        OrgResource.environment == environment).first()

    if not resource:
        return f"Resource {resource_name} not found " \
               f"for {environment} environment"

    # Check if resource is already locked
    locked_resource = db.query(LockedResource).filter(
        LockedResource.org_resource_id == resource.id).first()

    if not locked_resource:
        # Create a new locked resource
        return lock_resource_for_user(db, user_id, resource.id)

    # Check if the resource is locked by the user
    if locked_resource.owner_id == user_id:
        return f"Resource {resource_name} for {environment} environment " \
               f"is already locked by you"

    return (
        "Resource {} for {} environment is already locked by {} "
        "and will be released in {}".format(
            locked_resource.org_resource.resource_name,
            locked_resource.org_resource.environment,
            locked_resource.owner_id,
            humanize.precisedelta(
                locked_resource.expires_at, minimum_unit="minutes"
            )
        )
    )


def lock_resource_for_user(
        db: Session, user_id: str, org_resource_id: str) -> str:
    """Lock a resource for a user."""
    current_time = datetime.datetime.now()
    expiration_time = current_time + timedelta(days=1)
    locked_resource = LockedResource(
        owner_id=user_id,
        org_resource_id=org_resource_id,
        locked_at=current_time,
        expires_at=expiration_time,
    )
    db.add(locked_resource)
    db.commit()

    return (
        "{} has locked {} for {} environment "
        "and will released in {}".format(
            locked_resource.owner_id,
            locked_resource.org_resource.resource_name,
            locked_resource.org_resource.environment,
            humanize.precisedelta(expiration_time, minimum_unit="minutes")
        )
    )
