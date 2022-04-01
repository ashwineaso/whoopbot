from whoopbot.actions.base import Action


class ReleaseAction(Action):
    """
    Action to release a resource

    Syntax: /whoop release <resource_name> <environment>

    Eg: /whoop release api-service
    Eg: /whoop release api-service
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

        return "processing release action"
