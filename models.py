from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.schema import Sequence
test_id_seq = Sequence('test_id_seq', start=9900001) #testId starts from 990001
user_id_seq = Sequence('user_id_seq', start=55000001) #testId starts from 990001
doctor_id_seq = Sequence('doctor_id_seq', start=99000001) #testId starts from 990001
clinic_id_seq = Sequence('doctor_id_seq', start=11000001) #testId starts from 990001

db = SQLAlchemy()

# Define models (tables)
class User(UserMixin,db.Model):
    __tablename__ = 'users'  
    # id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing primary key
    userId = db.Column(db.Integer, unique=True, server_default=user_id_seq.next_value(),primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    alternate_contact = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)  

    def get_id(self):
        return self.userId 

    # Relationship to Appointment
    appointments = db.relationship('Appointment', backref='user', lazy=True)

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'), nullable=False)  # Foreign key to the User model
    appointment_time = db.Column(db.DateTime, nullable=False)
    appointment_location = db.Column(db.Integer, nullable=False) #will store location as clinicID.
    status_of_appointment = db.Column(db.Boolean, default=False)  # False = Not completed, True = Completed/Cancelled
    doctorId = db.Column(db.Integer,nullable=False)  # will select doctor and will be stored as doctorId.
    is_payment_made = db.Column(db.Boolean, default=False)
    user_informed = db.Column(db.Boolean, default=False)
    doctor_informed = db.Column(db.Boolean, default=False)
    payment_to_doctor = db.Column(db.Boolean, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # Relationship to Payment
    payment = db.relationship('Payment', backref='appointment', lazy=True)

    # Relationship to AppointmentHistory
    history = db.relationship('AppointmentHistory', backref='appointment', lazy=True)

class AppointmentHistory(db.Model):
    __tablename__ = 'appointment_history'

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)  # Foreign key to Appointment
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'), nullable=False)  # Foreign key to User
    doctor_id = db.Column(db.String(50), nullable=False)  # The doctor ID for the historical appointment
    original_appointment_time = db.Column(db.DateTime, nullable=False)  # Original appointment time
    updated_appointment_time = db.Column(db.DateTime, nullable=True)  # Updated appointment time (if changed)
    status = db.Column(db.String(50), nullable=False, default="Scheduled")  # Status of the appointment (Scheduled, Cancelled, Rescheduled, etc.)
    cancellation_reason = db.Column(db.String(200), nullable=True)  # Reason for cancellation (if applicable)
    payment_status = db.Column(db.String(50), nullable=True)  # Payment status at the time of the history record
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)  # When the history entry was created
    # updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)  # When the history entry was last updated


    # Relationship to User (optional if you want to track which user made changes)
    # user = db.relationship('User', backref='history', lazy=True)


##############Doctor's Models################

class Doctor(UserMixin,db.Model):
    __tablename__ = 'doctors'

    # id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the doctor
    first_name = db.Column(db.String(100), nullable=False)  # First name of the doctor
    last_name = db.Column(db.String(100), nullable=False)  # Last name of the doctor
    doctorId = db.Column(db.Integer, unique=True, server_default=doctor_id_seq.next_value(),primary_key=True) #doctor would get option to set doctorId
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email of the doctor (must be unique)
    password = db.Column(db.String(200), nullable=False)  # Hashed password for login
    contact = db.Column(db.String(15), nullable=False)  # Contact number of the doctor
    alternate_contact = db.Column(db.String(15), nullable=True)  # Optional alternate contact
    specialization = db.Column(db.String(100), nullable=False)  # Doctor's specialization (e.g., Cardiologist, Dentist)
    years_of_experience = db.Column(db.Integer, nullable=False)  # Number of years of experience
    state = db.Column(db.String(50), nullable=False)  # State of the clinic
    available_time_start = db.Column(db.Time, nullable=False)  # Start time of availability
    available_time_end = db.Column(db.Time, nullable=False)  # End time of availability
    is_active = db.Column(db.Boolean, default=True, nullable=False)  # Active status of the doctor
    image_url = db.Column(db.String(255), nullable=True)  # URL for storing image path or reference
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)  # Timestamp when the doctor was added
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)  # Timestamp for last update
    
    def get_id(self):
        return self.doctorId
    
    # appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    clinics = db.relationship('Clinic', backref='doctor', lazy=True)

class Clinic(db.Model):
    __tablename__='clinics'
    # id=db.Column(db.Integer,primary_key=True)
    clinicId=db.Column(db.Integer, unique=True, server_default=clinic_id_seq.next_value(),primary_key=True)
    doctor_at_clinic=db.Column(db.Integer,db.ForeignKey('doctors.doctorId'),nullable=False)
    active_status = db.Column(db.Boolean,default=True,nullable=False) # True-> active / False  -> Inactive
    address= db.Column(db.String(200),nullable=False)
    city= db.Column(db.String(200),nullable=False)
    pincode= db.Column(db.Integer,nullable=False)
    state= db.Column(db.String(50),nullable=False)
    fees= db.Column(db.Integer,nullable=False)
    discount_percentage= db.Column(db.Float,nullable=False)
    fees_after_discount=db.Column(db.Float,nullable=False)

    timeslots=db.relationship('TimeSlot', backref='Clinic', lazy=True)

class TimeSlot(db.Model):
    __tablename__ = "timeslots"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clinic_id = db.Column(db.Integer,db.ForeignKey('clinics.clinicId'),nullable=False, index=True)
    slot_date = db.Column(db.Date, nullable=False)  # Store the specific date
    slot_day = db.Column(db.String(20), nullable=False)  # Store the day of the week
    slot_time = db.Column(db.Time, nullable=False)  # Store the time of the slot
    status = db.Column(db.String(12),nullable=False,default="Available")

    def to_dict(self):
        return {
            "id": self.id,
            "clinic_id": self.clinic_id,
            "slot_date": str(self.slot_date),
            "slot_day": self.slot_day,
            "slot_time": str(self.slot_time)
        }

############Test Models##############
class Facilities(db.Model):
    __tablename__="facilitiess"
    id = db.Column(db.Integer,primary_key=True,unique=True,autoincrement=True,nullable=False)
    facility_name=db.Column(db.String(100),nullable=False)
    allfacilitiess=db.relationship('AllFacilities', backref='Facilities', lazy=True)

class AllFacilities(db.Model):
    __tablename__="allfacilitiess"
    id= db.Column(db.Integer,primary_key=True)
    facility_id = db.Column(db.Integer,db.ForeignKey('facilitiess.id'),nullable=False)
    test_id = db.Column(db.Integer, unique=True, server_default=test_id_seq.next_value()) # first column need to be inserted manually with id=990001
    test_name=db.Column(db.String(100),nullable=False)
    price_for_test = db.Column(db.Integer,nullable=False)
    discount_on_test=db.Column(db.Integer,nullable=True,default=0)
    test_details=db.Column(db.String(100),nullable=True)
    test_preparation_details=db.Column(db.String(100),nullable=True)
    test_TAT=db.Column(db.String(100),nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    facilityFaq=db.relationship('FacilityFaq',backref='AllFacilities',lazy=True)
    test_parameters=db.relationship('facility_test_parameter',backref='AllFacilities',lazy=True)
class FacilityFaq(db.Model):
    __tablename__='facilityFaqs'
    id = db.Column(db.Integer,primary_key=True)
    test_id=db.Column(db.Integer,db.ForeignKey('allfacilitiess.test_id'))
    faq= db.Column(db.String(200),nullable=False)
    faqa=db.Column(db.String(500),nullable=False)

class facility_test_parameter(db.Model):
    __tablename__='testParameters'
    id = db.Column(db.Integer,primary_key=True)
    test_Id=db.Column(db.Integer,db.ForeignKey('allfacilitiess.test_id'))
    parameter_name=db.Column(db.String(50),nullable=False)
    parameter_child_name=db.Column(db.String(100),nullable=False)

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'), nullable=False,unique=True)  # Foreign key to the User model
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    total_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    payment_method = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), default="Completed", nullable=False)


#Events to start Ids
#Event for test_id_seq to set test_id start=990001
###test_id_seq
@db.event.listens_for(db.metadata, 'before_create')
def create_sequences(target, connection, **kwargs):
    test_id_seq.create(connection)
#Event to drop sequence after table is dropped
@db.event.listens_for(db.metadata, 'after_drop')
def drop_sequences(target, connection, **kwargs):
    test_id_seq.drop(connection)
###user_id_seq
@db.event.listens_for(db.metadata, 'before_create')
def create_sequences(target, connection, **kwargs):
    user_id_seq.create(connection)
#Event to drop sequence after table is dropped
@db.event.listens_for(db.metadata, 'after_drop')
def drop_sequences(target, connection, **kwargs):
    user_id_seq.drop(connection)
###doctor_id_seq
@db.event.listens_for(db.metadata, 'before_create')
def create_sequences(target, connection, **kwargs):
    doctor_id_seq.create(connection)
#Event to drop sequence after table is dropped
@db.event.listens_for(db.metadata, 'after_drop')
def drop_sequences(target, connection, **kwargs):
    doctor_id_seq.drop(connection)
###clinic_id_seq
@db.event.listens_for(db.metadata, 'before_create')
def create_sequences(target, connection, **kwargs):
    clinic_id_seq.create(connection)
#Event to drop sequence after table is dropped
@db.event.listens_for(db.metadata, 'after_drop')
def drop_sequences(target, connection, **kwargs):
    clinic_id_seq.drop(connection)
