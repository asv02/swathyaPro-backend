from flask import Flask, jsonify, request
from flask_login import current_user 
from models import db, User,Doctor,datetime
from flask_login import LoginManager,login_user,logout_user
import cloudinary.uploader
import bcrypt  
import os


def gen_patient_id():
   count = db.session.query(User).count()
   return f"P_{count+1}"

def gen_doctor_id():
   count = db.session.query(Doctor).count()
   return f"D_{count+1}"


# Cloudinary configuration
cloudinary.config(
    cloud_name="dni5wcbsz",
    api_key="271365318367474",
    api_secret="L2ZC4nw7qdIjYZsLI1DlIX7JUc4"
)

#user register and send a verification email to personal email, if verified then only access.
def register():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate input data
        required_fields = ["userId","first_name", "last_name", "email", "password", "date_of_birth", "contact"]
        if not data or not all(key in data for key in required_fields):
            return jsonify({"error": "Invalid input data"}), 400

        # Check if the userId is already in use
        if User.query.filter_by(userId=data["userId"]).first():
            return jsonify({"error": "User with this userId is already registered"}), 409

        # Check if the email is already in use
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already registered"}), 409

        # Hash the password
        hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())

        # Create a new User instance
        new_user = User(
            first_name=data["first_name"],
            userId=data["userId"],
            last_name=data["last_name"],
            email=data["email"],
            password=hashed_password.decode('utf-8'),  # Store the hashed password as a string
            date_of_birth=data["date_of_birth"],
            contact=int(data["contact"]),
            alternate_contact=(data.get("alternate_contact")),
            address=data["address"],
            pincode=int(data["pincode"]),
            state=data["state"]
        )

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

def doctor_registration():
    try:
        data = request.form
        image = request.files.get('image')

        # Validate input data
        required_fields = ["doctorId","first_name", "last_name", "email", "password", "contact", "specialization", "years_of_experience", "clinic_address", "clinic_pincode", "state", "available_time_start"]
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Invalid input data"}), 400

        # Check if the email is already in use
        if Doctor.query.filter_by(doctorId=data["doctorId"]).first():
            return jsonify({"error": "Doctor with this doctorId is already registered"}), 409

        # Check if the email is already in use
        if Doctor.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already registered"}), 409
        
                # Hash the password
        hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())

        # Upload image to Cloudinary
        image_url = None
        #change implementation of uploading image at later stage:
        #store the image first at temp folder on machine and then upload it to cloudinary and after successfull uploading, delete from temp folder.
        try:
            if image:
                upload_result = cloudinary.uploader.upload(image)
                image_url = upload_result.get("secure_url")
                print("image url->",image_url)
        except Exception as e:
            print("Error during uploading image ->",e)
        # Create a new Doctor instance
        new_doctor = Doctor(
            first_name=data["first_name"],
            last_name=data["last_name"],
            doctorId=data["doctorId"],
            email=data["email"],
            password=hashed_password.decode('utf-8'),  #hashed password is provided
            contact=data["contact"],
            alternate_contact=data.get("alternate_contact"),
            specialization=data["specialization"],
            years_of_experience=int(data["years_of_experience"]),
            clinic_address=data["clinic_address"],
            clinic_pincode=data["clinic_pincode"],
            state=data["state"],
            available_time_start=datetime.strptime(data["available_time_start"], "%H:%M").time(),
            available_time_end=datetime.strptime(data["available_time_end"], "%H:%M").time(),
            image_url=image_url
        )

        # Add the doctor to the database
        db.session.add(new_doctor)
        db.session.commit()

        return jsonify({"message": "Doctor registered successfully", "doctor_id": new_doctor.doctorId}), 201

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

#should be used for user and doctors both
def login():
    
    data = request.get_json()
    # Validate input
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password are required"}), 400

    if request.method=='POST': 
        data = request.get_json()
        email=data['email']
        password=data['password']
        user= User.query.filter_by(email=email).first()
        doctor = Doctor.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)
            loginUser={"userId":current_user.userId,"firstName":current_user.first_name,"lastName":current_user.last_name,"dob":current_user.date_of_birth,"contact":current_user.contact,"alternate_contact":current_user.alternate_contact,"email":current_user.email,"address":current_user.address,"pincode":current_user.pincode,"state":current_user.state}
            print(current_user)
            return jsonify(loginUser), 201
        elif doctor and bcrypt.checkpw(password.encode('utf-8'), doctor.password.encode('utf-8')):
            login_user(doctor) 
            logindoctor={"firstName":current_user.first_name,
                         "last_name":current_user.last_name,
                         "doctorId":current_user.doctorId,
                         "email":current_user.email,
                         "contact":current_user.contact,
                         "alternate_contact":current_user.alternate_contact,"specialization":current_user.specialization,"yearsOfExperience":current_user.years_of_experience,"state":current_user.state,"is_active":current_user.is_active,
                         "image_url":current_user.image_url}
            # print("current_user directory->",current_user,dir(current_user))
            return jsonify(logindoctor), 201
        else:
         return jsonify({"error": "Invalid credentials"}), 400
    
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

def recoverPassword():
    pass