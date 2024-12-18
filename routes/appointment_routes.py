from datetime import datetime
from flask import  jsonify, request
from models import db, Appointment, AppointmentHistory,Doctor, User
from flask_login import login_required,current_user 


#return dictionary
@login_required
def get_appointment(userId):
    appointments = (
        db.session.query(
            Appointment.userId,
            Appointment.appointment_time,
            Appointment.appointment_location,
            Appointment.status_of_appointment,
            Appointment.doctorId,
            Appointment.is_payment_made,
            Appointment.user_informed,
            Appointment.doctor_informed,
            Appointment.payment_to_doctor
        )
        .filter(Appointment.userId == userId)
        .all()
    )

    return [dict(zip(Appointment.__table__.columns.keys(), row)) for row in appointments]

@login_required
def book_appointment():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate input data (example: appointment_time, doctor_id)
        if not data or "appointment_time" not in data or "appointment_location" not in data or "doctorId" not in data:
            return jsonify({"error": "Appointment time,location and doctor are required"}), 400

        # Create a new Appointment instance
        new_appointment = Appointment(
            userId=current_user.userId,  # Link the appointment to the logged-in user
            appointment_time=datetime.strptime(data["appointment_time"], "%Y-%m-%d %H:%M:%S"),  # Parse the datetime string
            appointment_location=data["appointment_location"], #clinic location
            doctorId = data["doctorId"],
            status_of_appointment=False,  # (False = Not completed)
            is_payment_made=False,  # (payment not made)
            user_informed=False,  # (user not informed)
            doctor_informed=False,  # (doctor not informed)
            payment_to_doctor=None,  # value (no payment decided yet)
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # Add the appointment to the database
        db.session.add(new_appointment)
        db.session.commit()

        appointmentHistory=AppointmentHistory(
            appointment_id=new_appointment.id,
            userId=new_appointment.userId,
            doctor_id=new_appointment.doctorId,
            original_appointment_time=new_appointment.created_at,
            updated_appointment_time=new_appointment.updated_at
        )
        # Add the appointment history to the database
        db.session.add(appointmentHistory)
        db.session.commit()

        return jsonify({"message": "Appointment booked successfully", "appointment_id": new_appointment.id}), 201

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# can be used by user as well as doctors
@login_required
def update_appointment(appointment_id):
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Ensure at least one field (appointment_time or status) is provided for update
        if not data or ("appointment_time" not in data and "status" not in data):
            return jsonify({"error": "Provide appointment_time or status to update"}), 400

        # Retrieve the appointment record
        appointment = Appointment.query.filter_by(id=appointment_id).first()

        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404

        # Handle user-specific update (appointment time)
        if "appointment_time" in data:
            if current_user.id != appointment.userId:
                return jsonify({"error": "Unauthorized to update appointment time"}), 403

            # Parse and validate the new appointment time
            try:
                new_time = datetime.strptime(data["appointment_time"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return jsonify({"error": "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'"}), 400

            # Check if the new time is different from the current time
            if appointment.appointment_time == new_time:
                return jsonify({"message": "New time slot is the same as the current time"}), 200

            # Log the change in AppointmentHistory
            appointment_history_entry = AppointmentHistory(
                appointment_id=appointment.id,
                userId=appointment.userId,
                doctor_id=appointment.doctor_id,
                original_appointment_time=appointment.appointment_time,
                updated_appointment_time=new_time,
                status="Rescheduled",
                payment_status="Paid" if appointment.is_payment_made else "Unpaid",
                created_at=datetime.now()
            )

            # Update the appointment time
            appointment.appointment_time = new_time
            appointment.updated_at = datetime.now()

            # Save the history entry
            db.session.add(appointment_history_entry)

        # first validate that this user is DOCTOR #########
        # Handle doctor-specific update (status)
        if "status" in data:
            # completed will be shown only to doctors
            if data["status"].lower() == "completed":
                # Assuming the current user is a doctor, validate their ID
                #########################################################################
                is_doctor = Doctor.query.filter_by(doctorId=current_user.doctorId).first()
                if not is_doctor and  current_user.doctorId != appointment.doctorId:
                    return jsonify({"error": "Unauthorized to update appointment status"}), 403
                ##########################################################################           
                new_status = data["status"]
            else:
                new_status = data["status"]

                # Log the status change in AppointmentHistory
            appointment_history_entry = AppointmentHistory(
                appointment_id=appointment.id,
                userId=appointment.userId,
                doctor_id=appointment.doctor_id,
                original_appointment_time=appointment.appointment_time,
                updated_appointment_time=None,
                status=new_status,
                payment_status="Paid" if appointment.is_payment_made else "Unpaid",
                created_at=datetime.now()
            )

            # Update the status of the appointment
            appointment.status_of_appointment = True if new_status.lower() in ["completed", "cancelled"] else False
            appointment.updated_at = datetime.now()

            # Save the history entry
            db.session.add(appointment_history_entry)

        # Commit all changes to the database
        db.session.commit()

        return jsonify({"message": "Appointment updated successfully", "appointment_id": appointment.id}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500