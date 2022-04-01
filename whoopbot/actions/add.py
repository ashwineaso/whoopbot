from whoopbot.actions.base import Action


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


def process_action(params):
    """Process the action and return the result of it."""

    environment = "Default"
    # Parse the params of the action
    if len(params) == 2:
        _, resource_name = params
    else:
        _, resource_name, _, environment = params

    # Check if the resource exists already for the environment
    # If the resource exists for the default environment,
    # the return the message to the user asking them to remove the resource
    # and add again with the environment

    # If the resource exists for the environment,
    # return the message to the user informing them of its presence

    # If the resource does not exist for the environment,
    # Add the resource to the database for the environment
