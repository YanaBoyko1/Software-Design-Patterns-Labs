from abc import ABC, abstractmethod


class IClinicRepository(ABC):

    @abstractmethod
    def read_csv(self, file_path: str) -> list:
        pass

    @abstractmethod
    def save_models(self, models_list: list):
        pass
