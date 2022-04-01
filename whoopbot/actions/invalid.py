from whoopbot.actions.base import Action


class InvalidAction(Action):
    """
    Action is invalid
    """

    def is_valid(self) -> bool:
        return True

    def process(self) -> str:
        return "Invalid action"
