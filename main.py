from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dal.models import Base
from dal.repository import ClinicRepository
from bll.services import ClinicService


def main():
    print("--- Starting Clinic Program ---")

    engine = create_engine("sqlite:///clinic.db")
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    db_session = SessionLocal()

    repository = ClinicRepository(db_session)
    service = ClinicService(repository)

    csv_file = "clinic_data.csv"
    service.process_data_to_db(csv_file)

    print("--- Operation completed successfully! Check clinic.db file ---")


if __name__ == "__main__":
    main()
