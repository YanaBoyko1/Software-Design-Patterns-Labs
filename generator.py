import csv
import random
from datetime import datetime, timedelta


def generate_csv(filename="clinic_data.csv", num_rows=1005):
    patient_names = [
        "Oleksandr Kovalenko",
        "Mariia Boiko",
        "Ivan Melnyk",
        "Anna Tkachenko",
        "Yana Lysenko",
        "Viktor Shevchenko",
    ]
    dentist_names = ["Dr. Smith", "Dr. Koval", "Dr. House", "Dr. Frank"]
    specializations = ["Surgeon", "Therapist", "Orthodontist", "Periodontist"]
    diagnoses = [
        "Caries",
        "Pulpitis",
        "Gingivitis",
        "Healthy",
        "Teeth Cleaning",
        "Braces Installation",
    ]
    statuses = ["Scheduled", "Completed", "Cancelled"]

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            [
                "PatientName",
                "PatientEmail",
                "PatientCardID",
                "MedicalHistory",
                "DentistName",
                "DentistEmail",
                "Specialization",
                "LicenseID",
                "ApptDate",
                "ApptTime",
                "ApptStatus",
                "Diagnosis",
                "EstimatedCost",
                "HasXRay",
                "XRayUploadDate",
            ]
        )

        for _ in range(num_rows):
            p_name = random.choice(patient_names)
            p_email = f"patient{random.randint(1, 999)}@email.com"
            p_card = random.randint(1000, 9999)
            med_history = random.choice(
                ["Penicillin allergy", "None", "Diabetes", "Hypertension", "None"]
            )

            d_name = random.choice(dentist_names)
            d_email = f"doctor{random.randint(1, 50)}@clinic.com"
            spec = random.choice(specializations)
            lic_id = f"LIC-{random.randint(100, 999)}"

            date_obj = datetime.now() - timedelta(days=random.randint(0, 180))
            appt_date = date_obj.strftime("%Y-%m-%d")
            appt_time = f"{random.randint(9, 17):02d}:00"
            status = random.choice(statuses)

            diagnosis = random.choice(diagnoses)
            cost = round(random.uniform(500, 15000), 2)

            has_xray = random.choice(["Yes", "No"])
            xray_date = appt_date if has_xray == "Yes" else ""

            writer.writerow(
                [
                    p_name,
                    p_email,
                    p_card,
                    med_history,
                    d_name,
                    d_email,
                    spec,
                    lic_id,
                    appt_date,
                    appt_time,
                    status,
                    diagnosis,
                    cost,
                    has_xray,
                    xray_date,
                ]
            )

    print(f"Done! Generated {num_rows} rows in file {filename}")


if __name__ == "__main__":
    generate_csv()
