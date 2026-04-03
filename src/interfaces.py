from abc import ABC, abstractmethod


class IOutputStrategy(ABC):

    @abstractmethod
    def write(self, data: list):
        pass
