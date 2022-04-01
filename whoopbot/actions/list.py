from whoopbot.actions.base import Action


class ListAction(Action):
    """
    Action to list resources

    Eg: /whoop list resources
    """

    DEFAULT_MESSAGE = "The command to list resources is " \
                      "`/whoop list resources`"

    def is_valid(self) -> bool:
        if (not len(self.params) or len(self.params) > 1 or
                self.params[0] != "resources"):
            return False
        return True

    def process(self):
        if not self.is_valid():
            return self.DEFAULT_MESSAGE

        return "processing list resources"
