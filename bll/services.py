from dal.interfaces import IClinicRepository
from dal.models import Patient, Dentist, Appointment, TreatmentPlan, XRayImage
from sqlalchemy.exc import IntegrityError
import random
from datetime import datetime


class ClinicService:
    def __init__(self, repository: IClinicRepository):
        # Dependency Injection of the repository
        self.repository = repository

    def process_data_to_db(self, csv_filepath: str):
        """Logic for initial database population from a CSV file"""
        print("1. Business Logic: Reading file...")
        raw_data = self.repository.read_csv(csv_filepath)

        patients_dict = {}
        dentists_dict = {}
        appointments_to_save = []

        for row in raw_data:
            p_email = row["PatientEmail"]
            d_email = row["DentistEmail"]

            # Patient uniqueness by Email
            if p_email not in patients_dict:
                patients_dict[p_email] = Patient(
                    name=row["PatientName"],
                    email=p_email,
                    patientCardID=int(row["PatientCardID"]),
                    medicalHistory=row["MedicalHistory"],
                )

            # Dentist uniqueness by Email
            if d_email not in dentists_dict:
                dentists_dict[d_email] = Dentist(
                    name=row["DentistName"],
                    email=d_email,
                    specialization=row["Specialization"],
                    licenseID=row["LicenseID"],
                )

            # Create an Appointment object
            appointment = Appointment(
                date=row["ApptDate"],
                time=row["ApptTime"],
                status=row["ApptStatus"],
                patient=patients_dict[p_email],
                dentist=dentists_dict[d_email],
            )

            # Treatment Plan (Composition)
            TreatmentPlan(
                diagnosis=row["Diagnosis"],
                estimatedCost=float(row["EstimatedCost"]),
                appointment=appointment,
            )

            # Add X-ray image if available
            if row["HasXRay"] == "Yes":
                XRayImage(
                    imageID=random.randint(1000, 9999),
                    uploadDate=row["XRayUploadDate"],
                    appointment=appointment,
                )

            appointments_to_save.append(appointment)

        print("2. Business Logic: Saving object tree (UML Composition)...")
        self.repository.save_models(appointments_to_save)
        print("Done!")

    # --- READ METHODS ---

    def get_all_patients(self):
        """Get a list of all patients"""
        return self.repository.get_all_patients()

    def get_appointments_with_details(self):
        """Get a list of appointments for the main table"""
        return self.repository.get_all_appointments()

    def get_dentists_list(self):
        """Get a list of dentists for the form dropdown"""
        return self.repository.get_all_dentists()

    def get_patient_by_id(self, patient_id):
        """Find a single patient by ID for the edit form"""
        return self.repository.get_patient_by_id(patient_id)

    # --- CREATE & UPDATE METHODS ---

    def create_new_patient_with_doctor(
        self, name, email, card_id, dentist_id, history="None"
    ):
        """Creates a patient with prior uniqueness check for Email and Card ID"""
        final_card_id = int(card_id) if card_id else random.randint(1000, 9999)

        # Check for duplicates in the database
        existing_patients = self.repository.get_all_patients()
        for p in existing_patients:
            if p.email == email:
                return False, "This Email is already registered!"
            if p.patientCardID == final_card_id:
                return False, f"Card ID {final_card_id} is already taken!"

        try:
            # 1. Create patient
            new_patient = Patient(
                name=name,
                email=email,
                patientCardID=final_card_id,
                medicalHistory=history,
            )
            saved_patient = self.repository.add_patient(new_patient)

            # 2. Create appointment record
            new_appt = Appointment(
                date=datetime.now().strftime("%Y-%m-%d"),
                time=datetime.now().strftime("%H:%M"),
                status="Scheduled",
                patient_id=saved_patient.id,
                dentist_id=int(dentist_id),
            )
            self.repository.add_appointment(new_appt)
            return True, "Patient added successfully!"
        except IntegrityError:
            return False, "An error occurred while saving (uniqueness violation)."

    def update_patient_details(
        self, patient_id, name, email, card_id, dentist_id, history="None"
    ):
        """
        Updates patient data and their attending dentist.
        """
        new_card_id = int(card_id)

        # 1. Check uniqueness among other patients
        existing_patients = self.repository.get_all_patients()
        for p in existing_patients:
            if p.id != patient_id:
                if p.email == email:
                    return False, "This Email is already in use by another patient!"
                if p.patientCardID == new_card_id:
                    return False, "This Card ID already belongs to someone else!"

        try:
            # 2. Update basic patient data via repository
            self.repository.update_patient(
                patient_id=patient_id,
                name=name,
                email=email,
                card_id=new_card_id,
                history=history,
            )

            # 3. Update dentist in appointments for this patient
            all_appointments = self.repository.get_all_appointments()
            for appt in all_appointments:
                if appt.patient_id == patient_id:
                    appt.dentist_id = int(dentist_id)

            # Save changes in the session
            self.repository.session.commit()

            return True, "Patient data updated successfully!"
        except Exception as e:
            return False, f"Failed to update data: {str(e)}"

    # --- DELETE METHOD ---

    def remove_appointment(self, appt_id):
        """Deletes a specific appointment from the table"""
        self.repository.delete_appointment(appt_id)
