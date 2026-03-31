from abc import ABC, abstractmethod


class IClinicRepository(ABC):
    @abstractmethod
    def read_csv(self, file_path: str) -> list:
        pass

    @abstractmethod
    def save_models(self, models_list: list):
        pass

    @abstractmethod
    def get_all_patients(self):
        pass

    @abstractmethod
    def get_all_appointments(self):
        pass

    @abstractmethod
    def get_all_dentists(self):
        pass

    @abstractmethod
    def get_patient_by_id(self, patient_id: int):
        pass

    @abstractmethod
    def add_patient(self, patient):
        pass

    @abstractmethod
    def add_appointment(self, appointment):
        pass

    @abstractmethod
    def update_patient(
        self, patient_id: int, name: str, email: str, card_id: int, history: str
    ):
        pass

    @abstractmethod
    def delete_appointment(self, appt_id: int):
        pass
