from whoopbot.actions.base import Action


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
