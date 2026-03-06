from abc import ABC, abstractmethod


class IClinicView(ABC):

    @abstractmethod
    def show_message(self, message: str):
        pass

    @abstractmethod
    def display_data(self, data: list):
        pass
