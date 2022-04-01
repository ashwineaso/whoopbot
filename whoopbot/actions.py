from abc import abstractmethod
from typing import List


class Action:

    def __init__(self, params: List[str]):
        self.params = params

    @abstractmethod
    def process(self):
        raise NotImplementedError("Action.process() not implemented")

    @abstractmethod
    def is_valid(self):
        return NotImplementedError("Action.is_valid() not implemented")


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


class InvalidAction(Action):
    """
    Action is invalid
    """

    def is_valid(self) -> bool:
        return True

    def process(self) -> str:
        return "Invalid action"


# Map of action to their action classes
ACTION_MAP = {
    'list': ListAction,
    'add': AddAction,
    'delete': DeleteAction,
    'lock': LockAction,
    'release': ReleaseAction
}
