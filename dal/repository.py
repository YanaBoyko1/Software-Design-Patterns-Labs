import csv
from sqlalchemy.orm import Session
from .interfaces import IClinicRepository


class ClinicRepository(IClinicRepository):
    def __init__(self, db_session: Session):
        self.session = db_session

    def read_csv(self, file_path: str) -> list:
        data = []
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data

    def save_models(self, models_list: list):
        self.session.add_all(models_list)
        self.session.commit()
