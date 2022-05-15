from whoopbot.actions.base import Action
from whoopbot.models import OrgResource


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

        return process_list_resources()


def process_list_resources() -> str:
    """
    Return a list of resources added by the organization
    """

    resources_list = list(OrgResource.scan())

    if len(resources_list) == 0:
        return "No resources added yet"

    return "Resources added by the organization:\n" + \
           "\n".join(["• " + resource.to_string()
                      for resource in resources_list])
