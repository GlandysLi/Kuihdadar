from flask import Flask, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from os import environ
import os, sys
from sqlalchemy import func, and_, text
from datetime import date
from model import Staff, Role_Skill, Staff_Skill, Role, Access_Rights, Skill, Listings, Applications

from model import JobApplication, mock_applications, Staff, Role_Skill, Staff_Skill, Role, Access_Rights, Skill, Listings, Applications

import requests 

app = Flask(__name__)

if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://' + \
                                             'root:root' + \
                                            '@localhost:8889/kuihdadar'
    ##app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/kuihdadar'
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                               'pool_recycle': 280}
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# # check db connection 
# @app.route('/test_db_connection')
# def test_db_connection():
#     try:
#         db.engine.execute("SELECT 1")  # A simple query to test the connection
#         return jsonify({"message": "Database connection is working"})
#     except Exception as e:
#         return jsonify({"error": "Database connection error", "details": str(e)})


import requests 
CORS(app)


# For KD1 - Create Role Listing (HR)


## DISPLAY ALL ROLE LISTINGS 
@app.route('/roles', methods=['GET'])
def get_roles():
    roles = Role.query.all()
    role_data = [role.to_dict() for role in roles]
    return jsonify({'data': role_data})

#create role listing
@app.route('/create_listing', methods=['POST'])
def create_listing():
    data= request.get_json()
    if not all(key in data.keys() for
               key in ('Role_Name',
                       'Closing_Date')):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 400


    # (1): Check if role already exists today
    listing = db.session.execute(
            db.select(Listings).
                    where(
                        and_(
                            Listings.Role_Name == data['Role_Name'],
                            Listings.Closing_Date >= func.curdate()
                        )
                    )
            ).scalar_one_or_none()
    
    if listing is not None:
        return jsonify({
          "message": "Role Listing with the same Role Name already exists. Please select another Role Name."
        }), 409

    else:
    # # (2) : Check if closing date is after today's date 
        closing_date = date.fromisoformat(data['Closing_Date'])
        today_date = date.today()
        if closing_date <= today_date:
            return jsonify({
                "message": "Closing date must be after today's date. Kindly select another date"
            }), 422
        
        else:
            # (3): Create listing record
            new_listing = Listings(
                Role_Name=data['Role_Name'], 
                Opening_Date=func.curdate(),
                Closing_Date=data['Closing_Date']
            )

            # (4): Commit to DB
            try:
                db.session.add(new_listing)
                db.session.commit()
                return jsonify(new_listing.to_dict()), 201
            except Exception as e:
                print("Database Error:", str(e))
                return jsonify({
                    "message": "Unable to commit to database."
                }), 500




#Get listing by Listing_ID
@app.route("/listing/<int:listing_id>")
def listing_by_id(listing_id):
    listing_by_id = db.session.execute(
                db.select(Listings).
                filter_by(Listing_ID=listing_id)
             ).scalar_one_or_none()
    if listing_by_id:
        return jsonify({
            "data": listing_by_id.to_dict()
        }), 200
    else:
        return jsonify({
            "message": "Listing not found."
        }), 404  
    
#search for role description by role name
# @app.route("/role_description")
# def role_description():
#     role_name = request.args.get('role_name')

#     if role_name:
#         # Query the "role" table for role description of the role name
#         sql = text("SELECT role_desc FROM role WHERE role_name = :role_name")
#         result = db.session.execute(sql, {"role_name": role_name})
#         description = [row[0] for row in result]

#         if description:
#             return jsonify({"description": description}), 200

#     # If no description or no role_name provided, return a message
#     return jsonify({"message": "No role description found."}), 404



## SEARCH / GET LIST OF ROLES BY ROLE NAME
@app.route("/role")
def role():
    search_name = request.args.get('name')
    if search_name:
        role_list = db.session.execute(
                         db.select(Role).
                         where(Role.Role_Name.contains(search_name))
                      ).scalars()
            
 
## SEARCH / GET LIST OF ROLES BY ROLE NAME DUPLICATE CHECKKKKKK
# @app.route("/role")
# def role():
#     search_name = request.args.get('name')
#     if search_name:
#         role_list = db.session.execute(
#                          db.select(Role).
#                          where(Role.Role_Name.contains(search_name))
#                       ).scalars()
#     else:
#         role_list = db.session.execute(db.select(Role)).scalars()
#     return jsonify(
#         {
#             "data": [role.to_dict() for role in role_list]
#         }
#     ), 200
          
            

#KD2 - Browse Listings (HR)
# Get all listings
@app.route("/listings")
def get_all_listings():
    listings = db.session.execute(db.select(Listings)).scalars()
    return jsonify(
        {
            "data": [listing.to_dict() for listing in listings]
        }
    ), 200


## GET ROLE DESC BY ROLE NAME
@app.route("/role_desc/<string:rolename>")
def getRoleDesc(rolename):
    role = db.session.execute(
                db.select(Role).
                filter_by(Role_Name = rolename)
            ).scalar_one_or_none()
    if role:
        return jsonify({
            "data": role.to_dict()
        }), 200
    else:
        return jsonify({
            "message": "Person not found."
        }), 404

#Get all ACTIVE listings
@app.route("/listings/active")
def active_listings():
    list_active = db.session.execute(db.select(Listings).
                         where(Listings.Closing_Date >= func.curdate())).scalars()
    return jsonify(
        {
            "Listings": [listings.to_dict() for listings in list_active]
        }
    ), 200

#Get all EXPIRED listings
@app.route("/listings/expired")
def expired_listings():
    list_expired = db.session.execute(db.select(Listings).
                         where(Listings.Closing_Date < func.curdate())).scalars()
    return jsonify(
        {
            "Listings": [listings.to_dict() for listings in list_expired]
        }
    ), 200


#search for possible roles by role name
@app.route("/role_search")
def role_search():
    search_name = request.args.get('search_name')

    if search_name:
        # Query the "role" table for role names containing the search term
        sql = text("SELECT role_name FROM role WHERE role_name LIKE :search_name")
        result = db.session.execute(sql, {"search_name": f"%{search_name}%"})
        suggestions = [row[0] for row in result]

        if suggestions:
            return jsonify({"suggestions": suggestions}), 200

    # If no suggestions or no search_name provided, return a message
    return jsonify({"message": "Invalid role name. Please select the correct role name."}), 404


#search for role description by role name
@app.route("/role_description")
def role_description():
    role_name = request.args.get('role_name')

    if role_name:
        # Query the "role" table for role description of the role name
        sql = text("SELECT role_desc FROM role WHERE role_name = :role_name")
        result = db.session.execute(sql, {"role_name": role_name})
        description = [row[0] for row in result]

        if description:
            return jsonify({"description": description}), 200

    # If no description or no role_name provided, return a message
    return jsonify({"message": "Invalid role name. No role description found."}), 404

@app.route("/active_listing_description")
def active_listing_description():
    # Query the "listings" table to get active listings' role names
    active_listings = db.session.execute(
        db.select(Listings)
        ##.where(Listings.Closing_Date >= func.curdate())
    ).scalars()
    role_names = [listing.Role_Name for listing in active_listings]

    # Fetch role descriptions from the "role" table based on the role names
    role_descriptions = {}
    for role_name in role_names:
        sql = text("SELECT role_desc FROM role WHERE role_name = :role_name")
        result = db.session.execute(sql, {"role_name": role_name})
        description = result.scalar()
        if description:
            role_descriptions[role_name] = description

    if role_descriptions:
        return jsonify(role_descriptions), 200

    # If no descriptions found, return a message
    return jsonify({"message": "No role descriptions found for active listings."}), 404

#find out if role name in role table
@app.route('/check_role_name')
def check_role_name():
    role_name = request.args.get('role_name')
    query = text("SELECT Role_Name FROM Role WHERE Role_Name = :role_name")
    result = db.session.execute(query, {"role_name": role_name}).fetchone()

    if result:
        return jsonify({"message": "Role name is valid."}), 200
    else:
        return jsonify({"message": "Invalid role name. Please select the correct role name."}), 404


        
## SEARCH / GET LIST OF SKILLS BY STAFF ID


@app.route("/staff_skills/<int:staff_id>")
def getSkillByStaff(staff_id):
    staff_skill_list = db.session.execute(
                db.select(Staff_Skill).
                filter_by(Staff_ID = staff_id)
      ).scalars()
    
    if staff_skill_list:
        result = []

        for staff_skill in staff_skill_list:
            result.append(staff_skill.get_staff_skill())
        return jsonify({
            "data": result
        }), 200
    else:
        return jsonify({
            "message": "Staff Skill not found."
        }), 404
        
        
## SEARCH / GET LIST OF SKILLS BY ROLE NAME

@app.route("/role_skills/<string:rolename>")
def getSkillByRole(rolename):
    role_skill_list = db.session.execute(
                db.select(Role_Skill).
                filter_by(Role_Name = rolename)
             ).scalars()
    if role_skill_list:
        result = []

        for role_skill in role_skill_list:
            result.append(role_skill.get_role_skill())
        return jsonify({
            "data": result
        }), 200
    else:
        return jsonify({
            "message": "Role Skill not found."
        }), 404
      
      


## ROLE SKILL MATCH 

@app.route("/compare_skills/<int:staff_id>/<string:rolename>")
def compareSkills(staff_id, rolename):
    
    # get skill list by staff
    staff_skill_list = db.session.execute(
        db.select(Staff_Skill).
        filter_by(Staff_ID=staff_id)
    ).scalars()
    if staff_skill_list:
        staff_skills = [staff_skill.get_staff_skill() for staff_skill in staff_skill_list]

    
    # get skill list by role
    role_skill_list = db.session.execute(
        db.select(Role_Skill).
        filter_by(Role_Name=rolename)
    ).scalars()
    if role_skill_list:
        role_skills = [role_skill.get_role_skill() for role_skill in role_skill_list]

    if staff_skills and role_skills:
        matching_skills = list(set(staff_skills) & set(role_skills))
        missing_skills = list(set(role_skills) - set(staff_skills))

        return jsonify({"Staff ID:": staff_id, "Role Name": rolename,
            #"Staff_Skills": staff_skills,
            #"Role_Skills": role_skills,
            "Matching_Skills": matching_skills,
            "Missing_Skills": missing_skills
        }), 200
    else:
        return jsonify({
            "message": "Staff or Role not found."
        }), 404

      
# KD 4 Marcus Code - Get Skills of Applicants (HR)
@app.route('/applications', methods=['GET'])
def get_applications():
    try:        
        listing_id = request.args.get('listing_id')
        ### ERROR CODE
        # #for db query
        # applications = Applications.query.filter_by(Listing_ID=listing_id).all()
        # ### Simulate database query using mock data
        # # applications = [app for app in mock_applications if app.Listing_ID == int(listing_id)]
        # application_data = []
        # for application in applications:
        #     application_data.append(application.to_dict())

        # Use db.session to query the database
        applications = db.session.query(Applications).filter_by(Listing_ID=listing_id).all()
        
        application_data = [application.to_dict() for application in applications]

        return jsonify(application_data)
    except Exception as e:
        app.logger.error(e)
        return str(e), 500
    


 
# #Get all listings
# @app.route("/listings")
# def listings():
#     list_details = db.session.execute(db.select(Listings).
#                          where(Listings.Closing_Date >= func.curdate())).scalars()
#     return jsonify(
#         {
#             "Listings": [listings.to_dict() for listings in list_details]
#         }
#     ), 200



@app.route("/skills/<int:staff_id>")
def skill_by_staff(staff_id):
    staff_skill_list = db.session.execute(
                db.select(Staff_Skill).
                filter_by(Staff_ID = staff_id)
             ).scalars()
    if staff_skill_list:
        result = []
        for staff_skill in staff_skill_list:
            result.append(staff_skill.get_skill())
        return jsonify({
            "data": result
        }), 200
    else:
        return jsonify({
            "message": "Staff_Skill not found."
        }), 404
    
## SEARCH / GET STAFF DETAILS BY STAFF ID
@app.route("/staff/<int:staff_id>")
def staff_by_id(staff_id):
    staff = db.session.execute(
                db.select(Staff).
                filter_by(Staff_ID=staff_id)
             ).scalar_one_or_none()
    if staff:
        return jsonify({
            "data": staff.to_dict()
        }), 200
    else:
        return jsonify({
            "message": "Staff not found."
        }), 404


#update role listing
@app.route('/update_listing/<int:listing_id>', methods=['POST'])
def update_listing(listing_id): 
    data = request.get_json()
    if 'Closing_Date' not in data:
        return jsonify({
            "message": "Incorrect JSON object provided. Missing 'Closing_Date'."
        }), 400
        
     # # (2) : Check if closing date is after today's date 
    closing_date = date.fromisoformat(data['Closing_Date'])
    today_date = date.today()
    if closing_date <= today_date:
        return jsonify({
            "message": "Closing date must be after today's date. Kindly select another date"
        }), 422
    
    listing = db.session.execute(
                db.select(Listings).
                    where(
                            Listings.Listing_ID == listing_id
                    )
            ).scalar_one_or_none()
    if listing is not None:
        # Update the listing fields with data received in the request
        listing.Closing_Date = data.get('Closing_Date', listing.Closing_Date)

        # Commit the changes to the database
        db.session.commit()
        return jsonify({"message": "Listing updated successfully!"}), 200
    else:
        # Handle the case where the listing is not found
        return jsonify({"message": "Listing update failed :("}), 404


## KD-8 CREATE A NEW APPLICATION
@app.route('/apply', methods=['POST'])

def apply():
    data= request.get_json()
    if not all(key in data.keys() for
               key in ('Listing_ID',
                          'Staff_ID')):
               
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 400


    # (1): Check if application already exists today
    listing = db.session.execute(
            db.select(Applications).
                    where(
                        and_(
                            Applications.Listing_ID == data['Listing_ID'],
                            Applications.Staff_ID == data['Staff_ID']
                            
                        )
                    )
            ).scalar_one_or_none()
    
    if listing is not None:
        return jsonify({
          "message": "You have already applied for this listing. Please select another listing to apply for."
        }), 409

    else:
            # (2): Create listing record
            new_application = Applications(
                ApplicationDate=func.curdate(),
                Listing_ID=data['Listing_ID'],
                Staff_ID=data['Staff_ID']
            )

            # (3): Commit to DB
            try:
                db.session.add(new_application)
                db.session.commit()
                return jsonify(new_application.to_dict()), 201
            except Exception as e:
                print("Database Error:", str(e))
                return jsonify({
                    "message": "Unable to commit to database."
                }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)