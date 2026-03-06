from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    user_type = Column(String)

    __mapper_args__ = {"polymorphic_on": user_type, "polymorphic_identity": "user"}

    def login(self):
        pass

    def logout(self):
        pass


class Dentist(User):
    __tablename__ = "dentists"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    specialization = Column(String)
    licenseID = Column(String)

    appointments = relationship("Appointment", back_populates="dentist")

    __mapper_args__ = {"polymorphic_identity": "dentist"}

    def examinePatient(self):
        pass

    def makeDiagnosis(self):
        pass

    def createTreatmentPlan(self):
        pass


class Patient(User):
    __tablename__ = "patients"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    patientCardID = Column(Integer)
    medicalHistory = Column(String)

    appointments = relationship("Appointment", back_populates="patient")

    __mapper_args__ = {"polymorphic_identity": "patient"}

    def viewTreatmentPlan(self):
        pass

    def bookAppointment(self):
        pass


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    date = Column(String)
    time = Column(String)
    status = Column(String)

    dentist_id = Column(Integer, ForeignKey("dentists.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))

    dentist = relationship("Dentist", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")

    treatment_plan = relationship(
        "TreatmentPlan", uselist=False, back_populates="appointment"
    )

    xray_images = relationship(
        "XRayImage", back_populates="appointment", cascade="all, delete-orphan"
    )

    def schedule(self):
        pass

    def cancel(self):
        pass


class TreatmentPlan(Base):
    __tablename__ = "treatment_plans"
    id = Column(Integer, primary_key=True)
    diagnosis = Column(String)
    estimatedCost = Column(Float)

    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    appointment = relationship("Appointment", back_populates="treatment_plan")

    def addProcedure(self):
        pass

    def printPlan(self):
        pass


class XRayImage(Base):
    __tablename__ = "xray_images"
    id = Column(Integer, primary_key=True)
    imageID = Column(Integer)
    uploadDate = Column(String)

    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    appointment = relationship("Appointment", back_populates="xray_images")

    def upload(self):
        pass

    def view(self):
        pass
