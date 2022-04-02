from typing import List

from sqlalchemy.orm import Session

from whoopbot.actions.base import Action
from whoopbot.models import LockedResource, OrgResource


class DeleteAction(Action):
    """
    Action to delete a resource from list of resources

    Syntax: /whoop delete resource <resource_name> for <environment>

    Eg: /whoop delete resource api-service
    Eg: /whoop delete resource api-service for testing
    """

    DEFAULT_MESSAGE = (
        "The command to add resources is "
        "`/whoop delete resource <resource_name> <environment: optional>`")

    def should_contain_only_service(self) -> bool:
        if len(self.params) == 2:
            return self.params[0] == "resource"
        return False

    def should_contain_both_service_and_environment(self) -> bool:
        if len(self.params) == 4:
            return self.params[0] == "resource" and self.params[2] == "for"
        return False

    def should_be_valid_length(self) -> bool:
        if len(self.params) in [2, 4]:
            return True
        return False

    def is_valid(self) -> bool:
        if (self.should_be_valid_length() and (
                self.should_contain_only_service() or
                self.should_contain_both_service_and_environment())):
            return True
        return False

    def process(self) -> str:
        if not self.is_valid():
            return self.DEFAULT_MESSAGE

        return "processing delete action"


def process_delete_action(db: Session, params: List[str]) -> str:
    """Delete the resource from the database."""

    default_environment = "Default"
    # Parse the params of the action
    environment = default_environment
    if len(params) == 2:
        _, resource_name = params
    else:
        _, resource_name, _, environment = params

    # Check if the resource exists for the environment
    resource = db.query(OrgResource).filter(
        OrgResource.resource_name == resource_name,
        OrgResource.environment == environment).first()

    if not resource:
        return f"Resource {resource_name} not found " \
               f"for {environment} environment"

    # Check if the resource is currently locked by an owner
    locked_resource = db.query(LockedResource).filter(
        LockedResource.org_resource_id == resource.id).first()

    if locked_resource:
        return f"Resource {resource_name} for {environment} environment" \
               f"is currently locked by {locked_resource.owner_id}"

    # Delete the resource if it is present and not locked
    db.delete(resource)
    db.commit()

    return f"Resource {resource_name} for {environment} environment deleted"
