from flask import Flask
from flask_login import LoginManager, login_required
import os
from routes import register,doctor_registration,login, logout, book_appointment, update_appointment,get_location_of_clinics,update_location_of_clinics,delete_location_of_clinics,add_location_of_clinics,get_appointment,delete_appointment
from models import db,User,Doctor

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize the database
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# User loader for login manager
@login_manager.user_loader
def load_user(user_id):
    print("user_id->",user_id)
    user = User.query.get(user_id)
    if not user:
        user = Doctor.query.get(user_id)
    return user

# Associate routes to the app
#general routes
app.add_url_rule('/auth/login', view_func=login, methods=['POST'])
app.add_url_rule('/auth/logout', view_func=logout, methods=['POST'])

#user routes
app.add_url_rule('/auth/register', view_func=register, methods=['POST'])
app.add_url_rule('/appointments/book', view_func=login_required(book_appointment), methods=['POST'])
app.add_url_rule('/appointments/get/<userId>', view_func=login_required(get_appointment), methods=['GET'])
app.add_url_rule('/appointments/delete/<appointmentId>', view_func=login_required(delete_appointment), methods=['DELETE'])
app.add_url_rule('/appointments/update/<int:appointment_id>', view_func=login_required(update_appointment), methods=['PUT'])

# doctor routes
app.add_url_rule('/auth/doctor/register', view_func=doctor_registration, methods=['POST'])
app.add_url_rule('/doctor/getclinics/<doctorId>', view_func=get_location_of_clinics, methods=['GET'])
app.add_url_rule('/doctor/addclinics/<doctorId>', view_func=add_location_of_clinics, methods=['POST'])
app.add_url_rule('/doctor/updateclinics/<clinicId>', view_func=update_location_of_clinics, methods=['PUT'])
app.add_url_rule('/doctor/deleteclinics/<clinicId>', view_func=delete_location_of_clinics, methods=['DELETE'])



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
