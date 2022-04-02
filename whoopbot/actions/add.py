from typing import List

from sqlalchemy.orm import Session

from whoopbot.actions.base import Action
from whoopbot.models import OrgResource


class AddAction(Action):
    """
    Action to add resources

    Syntax: /whoop add resource <resource_name> for <environment>

    Eg: /whoop add resource api-service
    Eg: /whoop add resource api-service for testing
    """

    DEFAULT_MESSAGE = (
        "The command to add resources is "
        "`/whoop add resources <resource_name> <environment: optional>`")

    def should_contain_only_service(self) -> bool:
        if len(self.params) == 2:
            return self.params[0] == "resource"
        return False

    def should_contain_both_service_and_environment(self) -> bool:
        if len(self.params) == 4:
            return self.params[0] == "resource" and self.params[2] == "for"
        return False

    def should_be_valid_length(self) -> bool:
        if len(self.params)  in [2, 4]:
            return True
        return False

    def is_valid(self) -> bool:
        if (self.should_be_valid_length() and (
                self.should_contain_only_service() or
                self.should_contain_both_service_and_environment())):
            return True
        return False

    def process(self):
        if not self.is_valid():
            return self.DEFAULT_MESSAGE

        return "processing add action"


def process_action(db: Session, params: List[str]) -> str:
    """Process the action and return the result of it."""

    default_environment = "Default"
    # Parse the params of the action
    environment = None
    if len(params) == 2:
        _, resource_name = params
    else:
        _, resource_name, _, environment = params

    resources_list: List[OrgResource] = fetch_resource(db, resource_name)

    resource = None
    for each in resources_list:
        if each.environment in [environment, default_environment]:
            resource = each
            break

    # if the resource is not found for the environment,
    # add the resource to the database for the new environment
    if not (resources_list and resource):
        return create_new_resource(db, resource_name, environment)

    # If the resource exists for the default environment,
    # the return the message to the user asking them to remove the resource
    # and add again with the environment
    if resource.environment == default_environment:
        return f"Resource {resource_name} already exists " \
               f"for {default_environment} environment"

    # If the resource exists for the non-default environment,
    # return the message to the user informing them of its presence
    return f"Resource {resource_name} already exists " \
           f"for {resource.environment} environment"


def fetch_resource(db: Session, resource_name: str):
    # Check if the resource exists already for the environment
    return db.query(OrgResource).filter(
        OrgResource.resource_name == resource_name).all()


def create_new_resource(db: Session, resource_name: str, environment: str):
    # Create a new resource for the environment
    resource = OrgResource(resource_name=resource_name, environment=environment)
    db.add(resource)
    db.commit()
    return f"Resource {resource_name} added to {environment} environment"

