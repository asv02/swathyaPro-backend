from datetime import datetime
from flask import  jsonify, request
from models import db, Facilities,facility_test_parameter,FacilityFaq,AllFacilities
from sqlalchemy import delete
from flask_login import login_required,current_user 

#Facility headers routes
@login_required
def add_facilities():
    data = request.get_json()
    try:
        if not data or not data['facility_name']:
            return jsonify({"error":"Insufficient data"}),400
        facility= Facilities(facility_name=data['facility_name'])
        db.session.add(facility)
        db.session.commit()
        return jsonify({"message":"Successfull added the facility"}),201
    except Exception as e:
        return jsonify({"Error":f"There is error in adding facility info {str(e)}"}),500

@login_required
def get_facilities():
    facilties=Facilities.query.all()
    facility_list=[{data.id:data.facility_name} for data in facilties]
    return jsonify({"facility list":facility_list}),201

#id
@login_required
def update_facilities(id):
    data = request.get_json()
    if not data or not data['facility_name']:
        return jsonify({"Error":"Nothing to Update"}),400
    facility = Facilities.query.get(id)
    facility.facility_name = data['facility_name']
    db.session.commit()
    return jsonify({"Success":"Updated the facility."}),201    

#id = id
@login_required
def delete_facilities(id):
    try:
        # Fetch all test IDs related to the facility ID
        test_ids = db.session.query(AllFacilities.test_id).filter(AllFacilities.facility_id == id).all()
                
        # Extract test IDs from the result
        test_ids = [row.test_id for row in test_ids]

        # Bulk delete related FAQs and parameters using test IDs
        db.session.query(FacilityFaq).filter(FacilityFaq.test_id.in_(test_ids)).delete(synchronize_session=False)
        db.session.query(facility_test_parameter).filter(facility_test_parameter.test_Id.in_(test_ids)).delete(synchronize_session=False)

        # Bulk delete related tests in AllFacilities
        db.session.query(AllFacilities).filter(AllFacilities.test_id.in_(test_ids)).delete(synchronize_session=False)

        # Delete the facility itself
        facility = Facilities.query.get(id)
        if not facility:
            return jsonify({"Error": "Facility not found"}), 404
        
        db.session.delete(facility)

        # Commit the transaction
        db.session.commit()

        return jsonify({"Success": "Facility and related data deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()  # Roll back the transaction in case of an error
        return jsonify({"Error": f"An error occurred: {str(e)}"}), 500

#AllFacilities routes
#takes facilityId
@login_required
def getAllFacilities(id):
    facilities = AllFacilities.query.filter_by(facility_id=id).all()
    if not facilities:
             return jsonify({"Error": "No facilities found"}), 404
    facilitiess = [{data.test_id:data.test_name} for data in facilities]
    print(facilitiess)
    return jsonify({"facilities->":facilitiess}),201

@login_required
def addAllFacilities():
    data = request.get_json()
    required_fields = ['facility_id','test_name','price_for_test','test_details','test_preparation_details','test_TAT']

    if not data or not all(field in data for field in required_fields):
        return jsonify({"error":"Insufficient data"}),400
    
    new_facility=AllFacilities(
        facility_id=data['facility_id'],
        test_name=data['test_name'],
        price_for_test=data['price_for_test'],
        test_details=data['test_details'],
        test_preparation_details=data['test_preparation_details'],
        test_TAT=data['test_TAT']
    )
    db.session.add(new_facility)
    db.session.commit()
    return jsonify({"Success":"Added facility."}),201


@login_required
def updateAllFacilities(id):
    data= request.get_json()
    allfacilities = AllFacilities.query.filter_by(test_id=id).first()
    # print(allfacilities.test_name)
    if not allfacilities:
        return jsonify({"Error":"Test not found"}),400
    for field, value in data.items():
        if hasattr(allfacilities, field):
            setattr(allfacilities, field, value) 
    print(allfacilities.test_name)
    print(allfacilities.price_for_test)
    db.session.commit()
    return jsonify({"Success":"Updates facility successfully"}),201

#here id is test_Id
@login_required
def deleteAllFacilities(id):
    #delete first Faqs and parameters  related to this test_Id
    try:
        faq = FacilityFaq.query.filter_by(test_id = id).all()
        parameters = facility_test_parameter.query.filter_by(test_Id = id).all()
        print(faq)
        print(parameters)
        db.session.execute(delete(FacilityFaq).where(FacilityFaq.test_id == id))
        db.session.execute(delete(facility_test_parameter).where(facility_test_parameter.test_Id == id))
        test_entry = AllFacilities.query.filter_by(test_id=id).first()
        if not test_entry:
                return jsonify({"Error": "Test entry not found"}), 404

        db.session.delete(test_entry)
        db.session.commit()

        return jsonify({"Success": "Deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()  # Roll back the transaction in case of an error
        return jsonify({"Error": f"An error occurred: {str(e)}"}), 500

#AllfacilitiesFaqs routes
@login_required
def addFaqs():
    data = request.get_json()
    
    if not data or not data['test_id'] or not data['faq'] or not data['faqa']:
        return jsonify({"Error":"Insufficient data"}),400
    newFaqs=FacilityFaq(
        test_id = data['test_id'],
        faq = data['faq'],
        faqa = data['faqa']
    )
    db.session.add(newFaqs)
    db.session.commit()
    return jsonify({"Success":"Added Faq successfully"}),201

@login_required
def getFaqs(id):
    try:
        # Query all FAQs related to the given test_id
        faqs = FacilityFaq.query.filter_by(test_id=id).all()
        
        # If no FAQs are found, return an error message
        if not faqs:
            return jsonify({"error": "No FAQs found related to this test"}), 404
        
        # Process the FAQs into a list of dictionaries
        faqs_list = [
            {   "id":data.id,
                "test_id": data.test_id,
                "faq": data.faq,
                "faqa": data.faqa
            }
            for data in faqs
        ]
        
        # Return the list of FAQs as a JSON response
        return jsonify({"success": True, "faqs": faqs_list}), 200
    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@login_required #here id is faqId
def updateFaqs(id):
    data = request.get_json()
    faq = FacilityFaq.query.get(id)
    if not faq:
        return jsonify({"Error":"faq not found"}),400
    for field,value in data.items():
        if hasattr(faq,field):
            setattr(faq,field,value)
    db.session.commit()
    return jsonify({"Success":"Updated Successfully"}),201

@login_required
def deleteFaqs():
    try:
        faq = FacilityFaq.query.get(id)
        db.session.delete(faq)
        db.session.commit()
        return jsonify({"Success":"Deleted Successfully"}),201
    except Exception as e:
        db.session.rollback()  # Roll back the transaction in case of an error
        return jsonify({"Error": f"An error occurred: {str(e)}"}), 500


#Testparameters routes
@login_required
def addParameters():
    data = request.get_json()
    if not data or not data['test_Id'] or not data['parameter_name'] or not data['parameter_child_name']:
        return jsonify({"Error":"Insufficient data"}),400
    newParameter=facility_test_parameter(
        test_Id = data['test_Id'],
        parameter_name = data['parameter_name'],
        parameter_child_name = data['parameter_child_name']
    )
    db.session.add(newParameter)
    db.session.commit()
    return jsonify({"Success":"Added Parameter successfully"}),201

#this is is test_Id
@login_required
def getParameters(id):
    try:
        # Query all FAQs related to the given test_id
        parameters = facility_test_parameter.query.filter_by(test_Id=id).all()
        
        # If no FAQs are found, return an error message
        if not parameters:
            return jsonify({"error": "No Parameters found related to this test"}), 404
        
        # Process the FAQs into a list of dictionaries
        parameters_list = [
            {   "id":data.id,
                "test_Id": data.test_Id,
                "parameter_name": data.parameter_name,
                "parameter_child_name": data.parameter_child_name
            }
            for data in parameters
        ]
        
        # Return the list of FAQs as a JSON response
        return jsonify({"success": True, "Parameters": parameters_list}), 200
    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@login_required #here id is parameterId
def updateParameters(id):
    data = request.get_json()
    parameters = facility_test_parameter.query.get(id)
    if not parameters:
        return jsonify({"Error":"faq not found"}),400
    for field,value in data.items():
        if hasattr(parameters,field):
            setattr(parameters,field,value)
    db.session.commit()
    return jsonify({"Success":"Updated Successfully"}),201

#id is id
@login_required
def deleteParameters(id):
    try:
        params = facility_test_parameter.query.get(id)
        db.session.delete(params)
        db.session.commit()
        return jsonify({"Success":"Deleted Successfully"}),201
    except Exception as e:
        db.session.rollback()  # Roll back the transaction in case of an error
        return jsonify({"Error": f"An error occurred: {str(e)}"}), 500

