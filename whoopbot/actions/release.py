from typing import List

from sqlalchemy.orm import Session

from whoopbot.actions.base import Action
from whoopbot.db import SessionLocal
from whoopbot.models import LockedResource, OrgResource


class ReleaseAction(Action):
    """
    Action to release a resource

    Syntax: /whoop release <resource_name> <environment>

    Eg: /whoop release api-service
    Eg: /whoop release api-service <environment: optional>
    """

    DEFAULT_MESSAGE = (
        "The command to release a resource is "
        "`/whoop release <resource_name> <environment: optional>`")

    def should_be_valid_length(self) -> bool:
        if len(self.params) in [2, 3]:
            return True
        return False

    def is_valid(self) -> bool:
        if self.should_be_valid_length():
            return True
        return False

    def process(self) -> str:
        if not self.is_valid():
            return self.DEFAULT_MESSAGE

        return process_release_action(SessionLocal(), self.user_id, self.params)


def process_release_action(
        db: Session, user_id: str, params: List[str]) -> str:

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
        return f"Resource {resource_name} for {environment} environment " \
               f"is not locked. Nothing to release"

    if locked_resource.owner_id != user_id:
        return f"Resource {resource_name} for {environment} environment " \
               f"is locked by {locked_resource.owner_id}. You can't release it"

    # Release the resource
    db.delete(locked_resource)
    db.commit()

    return f"{locked_resource.owner_id} has released {resource_name} " \
           f"for {environment} environment"
