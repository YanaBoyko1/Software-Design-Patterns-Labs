from flask import Flask, render_template, request, redirect, url_for, flash
from bll.services import ClinicService
from dal.repository import ClinicRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dal.models import Base

app = Flask(__name__)

# SECRET KEY (required for flash messages to work)
app.secret_key = "clinic_secret_key_123"

# Database configuration
engine = create_engine("sqlite:///clinic.db")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
db_session = SessionLocal()

repo = ClinicRepository(db_session)
clinic_service = ClinicService(repo)


@app.route("/")
def index():
    appointments_list = clinic_service.get_appointments_with_details()
    return render_template("patients.html", appointments=appointments_list)


@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    if request.method == "POST":
        # Get result from the service (success status and message)
        success, message = clinic_service.create_new_patient_with_doctor(
            name=request.form.get("name"),
            email=request.form.get("email"),
            card_id=request.form.get("card_id"),
            dentist_id=request.form.get("dentist_id"),
        )

        if success:
            flash(message, "success")
            return redirect(url_for("index"))
        else:
            flash(message, "danger")
            return redirect(url_for("add_patient"))

    return render_template(
        "add_patient.html", dentists=clinic_service.get_dentists_list()
    )


@app.route("/edit_patient/<int:id>", methods=["GET", "POST"])
def edit_patient(id):
    if request.method == "POST":
        # ADDED: accepting dentist_id from the form
        success, message = clinic_service.update_patient_details(
            patient_id=id,
            name=request.form.get("name"),
            email=request.form.get("email"),
            card_id=request.form.get("card_id"),
            dentist_id=request.form.get("dentist_id"),  # <--- Passing the dentist
            history=request.form.get("history"),
        )

        if success:
            flash(message, "success")
            return redirect(url_for("index"))
        else:
            flash(message, "danger")
            return redirect(url_for("edit_patient", id=id))

    # PASSING PATIENT AND DENTISTS LIST TO THE TEMPLATE
    patient = clinic_service.get_patient_by_id(id)
    dentists = (
        clinic_service.get_dentists_list()
    )  # <--- Providing options to choose from
    return render_template("edit_patient.html", patient=patient, dentists=dentists)


@app.route("/delete_appointment/<int:id>", methods=["POST"])
def delete_appointment(id):
    clinic_service.remove_appointment(id)
    # This was the blue notification from your screenshot:
    flash("Record deleted successfully", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
