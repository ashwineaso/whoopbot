from whoopbot.actions.base import Action


class LockAction(Action):
    """
    Action to lock resource for an environment

    Syntax: /whoop lock <resource_name> <environment> <message> <duration>

    Eg: /whoop lock api-service testing "Testing" 2h
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

        return "processing lock action"
