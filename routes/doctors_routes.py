from datetime import datetime
from flask import  jsonify, request
from models import db, Appointment, AppointmentHistory,Doctor, Payment,Clinic,TimeSlot
from flask_login import login_required,current_user 


def generate_clinicId():
    count = db.session.query(Clinic).count()
    return f"C_{count+1}"


################clinic routes################

@login_required
def get_info_of_clinics(doctorId):
    doctor=Doctor.query.get(doctorId)
    doctor_clinics=doctor.clinics
    print(doctor_clinics)
    clinic_list = [data.clinicId for data in doctor_clinics]
    return jsonify({"clinic list":clinic_list}),201

# need to add uniqueness
@login_required
def add_info_of_clinics(doctorId):
   
    # print(dir(current_user))
    try:
        if current_user.doctorId != doctorId:
            return jsonify({"Error":"You are adding clinic to another doctor's profile"}),400
        
        data = request.get_json()
        required_fields = ["address", "city", "pincode", "state", "fees","discount_percentage"]

        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Insufficient data!!"}), 400

        new_clinic= Clinic(
        clinicId=generate_clinicId(),
        doctor_at_clinic=doctorId,
        address =data["address"],
        active_status = data["active_status"],
        city = data["city"],
        pincode=data["pincode"],
        state= data["state"],
        fees= data["fees"],
        discount_percentage= float(data["discount_percentage"]),
        fees_after_discount = data["fees"] - float(data["fees"] * data["discount_percentage"] / 100))

        #add to database
        db.session.add(new_clinic)
        db.session.commit() 
        return jsonify({"message":"Successfull added the clinic"}),201
    except Exception as e:
        return jsonify({"Error":f"There is error in adding clinic info {str(e)}"}),500

#not to give doctorId option to update
@login_required
def update_info_of_clinics(clinicId):
    data = request.get_json() #this may contain dicount percentage and fees
    temp_clinic = Clinic.query.filter_by(clinicId=clinicId).first()
    
    if not data:
        return jsonify({"Error":"Nothing to update"}),400
    
    if not temp_clinic:
        return jsonify({"error": "Clinic not found"}), 404

    for field, value in data.items():
        if hasattr(temp_clinic, field):
            setattr(temp_clinic, field, value)
    
    #Handle fees after discount
    if data["discount_percentage"]:
        temp_clinic.fees_after_discount = temp_clinic.fees - float(temp_clinic.fees * data["discount_percentage"] / 100)

    db.session.commit()
    return jsonify({"Success":"Updated the info info."}),201


@login_required
def delete_info_of_clinics(clinicId):
    temp_clinic = Clinic.query.filter_by(clinicId=clinicId).first()

    if not temp_clinic:
        return jsonify({"error": "Clinic not found"}), 404

    db.session.delete(temp_clinic)
    db.session.commit()

    return jsonify({"message": "Clinic deleted successfully"}), 200


#############time slots####################

@login_required
def add_time_slots(clinicId):
    data = request.get_json()
    slot_date = data.get("slot_date")
    slot_time = data.get("slot_time")
    status = data.get("status")
    if not clinicId or not slot_date or not slot_time:
        return jsonify({"error": "clinic_id, slot_date, and slot_time are required"}), 400

    # Determine the day of the week from the date
    slot_day = datetime.strptime(slot_date, '%Y-%m-%d').strftime('%A')

    new_slot = TimeSlot(clinic_id=clinicId, slot_date=slot_date, slot_day=slot_day, slot_time=slot_time,status=status)
    db.session.add(new_slot)
    db.session.commit()

    return jsonify(new_slot.to_dict()), 201

####Storing Week wise available time slots #####
##so can be accessed with clinicId and weekDay
@login_required
def get_time_slots(clinicId):
    data = request.get_json()
    clinic_id = clinicId
    slot_day = data["day"]

    query = TimeSlot.query
    if clinic_id:
        query = query.filter_by(clinic_id=clinic_id)
    if slot_day:
        query = query.filter_by(slot_day=slot_day)

    slots = query.all()
    return jsonify([slot.to_dict() for slot in slots]), 200


#not tested
@login_required
def delete_time_slots(slot_id):
    slot = TimeSlot.query.get(slot_id)

    if not slot:
        return jsonify({"error": "Time slot not found"}), 404

    db.session.delete(slot)
    db.session.commit()
    return jsonify({"message": "Time slot deleted successfully"}), 200
