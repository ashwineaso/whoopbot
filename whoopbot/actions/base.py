from abc import abstractmethod
from typing import List


class Action:

    def __init__(self, user_id: str, params: List[str]):
        self.user_id = user_id
        self.params = params

    @abstractmethod
    def process(self):
        raise NotImplementedError("Action.process() not implemented")

    @abstractmethod
    def is_valid(self):
        return NotImplementedError("Action.is_valid() not implemented")

