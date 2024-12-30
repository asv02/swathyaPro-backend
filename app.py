from flask import Flask
from flask_login import LoginManager, login_required
import os
from routes import register,doctor_registration,login, logout, book_appointment, update_appointment,get_info_of_clinics,update_info_of_clinics,delete_info_of_clinics,get_time_slots,add_time_slots,delete_time_slots,add_info_of_clinics,get_appointment,delete_appointment,get_facilities,add_facilities,update_facilities,delete_facilities,addAllFacilities,getAllFacilities,updateAllFacilities,deleteAllFacilities,addFaqs,addParameters,getFaqs,getParameters,updateFaqs,updateParameters,deleteParameters,deleteFaqs
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

#doctor's routes
app.add_url_rule('/auth/doctor/register', view_func=doctor_registration, methods=['POST'])
######clinic routes
app.add_url_rule('/doctor/getclinics/<int:doctorId>', view_func=get_info_of_clinics, methods=['GET'])
app.add_url_rule('/doctor/addclinics/<int:doctorId>', view_func=add_info_of_clinics, methods=['POST'])
app.add_url_rule('/doctor/updateclinics/<int:clinicId>', view_func=update_info_of_clinics, methods=['PUT'])
app.add_url_rule('/doctor/deleteclinics/<int:clinicId>', view_func=delete_info_of_clinics, methods=['DELETE'])
######time slots routes
app.add_url_rule('/doctor/addtime/<int:clinicId>',view_func=add_time_slots,methods=['POST'])
app.add_url_rule('/doctor/gettime/<int:clinicId>',view_func=get_time_slots,methods=['GET'])
app.add_url_rule('/doctor/deletetime/<int:Timeid>',view_func=get_time_slots,methods=['DELETE'])

#Admin routes
####Facility header APIs
app.add_url_rule('/admin/addfacilityheader',view_func=add_facilities,methods=['POST'])
app.add_url_rule('/admin/getfacilityheader',view_func=get_facilities,methods=['GET'])
app.add_url_rule('/admin/updatefacilityheader/<id>',view_func=update_facilities,methods=['PUT'])
app.add_url_rule('/admin/deletefacilityheader/<id>',view_func=delete_facilities,methods=['DELETE'])

####Facilities APIs
app.add_url_rule('/admin/addfacility',view_func=addAllFacilities,methods=['POST'])
app.add_url_rule('/admin/getfacility/<id>',view_func=getAllFacilities,methods=['GET'])
app.add_url_rule('/admin/updatefacility/<id>',view_func=updateAllFacilities,methods=['PUT'])
app.add_url_rule('/admin/deletefacility/<id>',view_func=deleteAllFacilities,methods=['DELETE'])
####FAQs APIs
app.add_url_rule('/admin/addfaq',view_func=addFaqs,methods=['POST'])
app.add_url_rule('/admin/getfaq/<id>',view_func=getFaqs,methods=['GET'])
app.add_url_rule('/admin/updatefaq/<id>',view_func=updateFaqs,methods=['PUT'])
app.add_url_rule('/admin/deletefaq',view_func=deleteFaqs,methods=['DELETE'])
####Testparameters APIs
app.add_url_rule('/admin/addparameters',view_func=addParameters,methods=['POST'])
app.add_url_rule('/admin/getparameters/<id>',view_func=getParameters,methods=['GET'])
app.add_url_rule('/admin/updateparameters/<id>',view_func=updateParameters,methods=['PUT'])
app.add_url_rule('/admin/deleteparameters/<id>',view_func=deleteParameters,methods=['DELETE'])



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
