from dal.interfaces import IClinicRepository
from dal.models import Patient, Dentist, Appointment, TreatmentPlan, XRayImage
import random


class ClinicService:
    def __init__(self, repository: IClinicRepository):
        self.repository = repository

    def process_data_to_db(self, csv_filepath: str):
        print("1. Business Logic: Reading file...")
        raw_data = self.repository.read_csv(csv_filepath)

        patients_dict = {}
        dentists_dict = {}
        appointments_to_save = []

        for row in raw_data:
            p_email = row["PatientEmail"]
            d_email = row["DentistEmail"]

            if p_email not in patients_dict:
                patients_dict[p_email] = Patient(
                    name=row["PatientName"],
                    email=p_email,
                    patientCardID=int(row["PatientCardID"]),
                    medicalHistory=row["MedicalHistory"],
                )

            if d_email not in dentists_dict:
                dentists_dict[d_email] = Dentist(
                    name=row["DentistName"],
                    email=d_email,
                    specialization=row["Specialization"],
                    licenseID=row["LicenseID"],
                )

            appointment = Appointment(
                date=row["ApptDate"],
                time=row["ApptTime"],
                status=row["ApptStatus"],
                patient=patients_dict[p_email],
                dentist=dentists_dict[d_email],
            )

            TreatmentPlan(
                diagnosis=row["Diagnosis"],
                estimatedCost=float(row["EstimatedCost"]),
                appointment=appointment,
            )

            if row["HasXRay"] == "Yes":
                XRayImage(
                    imageID=random.randint(1000, 9999),
                    uploadDate=row["XRayUploadDate"],
                    appointment=appointment,
                )

            appointments_to_save.append(appointment)

        print("2. Business Logic: Saving object tree (UML Composition)...")
        self.repository.save_models(appointments_to_save)
        print("Done! Database structure successfully populated.")
