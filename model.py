"""
models.py
- Data classes for the application
"""
# from email.policy import default
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import func

db = SQLAlchemy()

# Create a JobApplication model
class JobApplication():

# Put this code back when database is created!!!
# class JobApplication(db.Model):
    # __tablename__ = 'job_applications'
    # Application_ID = db.Column(db.Integer, primary_key=True)
    # ApplicationDate = db.Column(db.Integer, nullable=False)
    # Listing_ID = db.Column(db.Integer, db.ForeignKey('listings.Listing_ID'), nullable=False)
    # Staff_ID = db.Column(db.Integer, db.ForeignKey('staff.Staff_ID'), nullable=False)

    # Define a constructor if needed
    def __init__(self, Application_ID, ApplicationDate, Listing_ID, Staff_ID):
        self.Application_ID = Application_ID
        self.ApplicationDate = ApplicationDate
        self.Listing_ID = Listing_ID
        self.Staff_ID = Staff_ID

# Define mock data for testing
mock_applications = [
    JobApplication(Application_ID=1, ApplicationDate='2023-10-01', Listing_ID=101, Staff_ID=201),
    JobApplication(Application_ID=2, ApplicationDate='2023-10-02', Listing_ID=101, Staff_ID=202),
    JobApplication(Application_ID=3, ApplicationDate='2023-10-03', Listing_ID=102, Staff_ID=203),
]

class Staff(db.Model):
    __tablename__ = 'Staff'

    Staff_ID = db.Column(db.Integer, primary_key=True)
    Staff_FName = db.Column(db.String(50), nullable=False)
    Staff_LName = db.Column(db.String(50), nullable=False)
    Dept = db.Column(db.String(50), nullable=False)
    Country = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Access_ID = db.Column(db.Integer, db.ForeignKey('Access_Rights.Access_ID'))

    access_rights = db.relationship('Access_Rights', backref='staff')

    def to_dict(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

class Role_Skill(db.Model):
    __tablename__ = 'Role_Skill'

    Role_Name = db.Column(db.String(20), db.ForeignKey('Role.Role_Name'), primary_key=True)
    Skill_Name = db.Column(db.String(50), db.ForeignKey('Skill.Skill_Name'), primary_key=True)

    role = db.relationship('Role', backref='role_skill')
    skill = db.relationship('Skill', backref='role_skill')

    def to_dict(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
    
    def get_role_skill(self):
        return self.Skill_Name

class Staff_Skill(db.Model):
    __tablename__ = 'Staff_Skill'

    Staff_ID = db.Column(db.Integer, db.ForeignKey('Staff.Staff_ID'), primary_key=True)
    Skill_Name = db.Column(db.String(50), db.ForeignKey('Skill.Skill_Name'), primary_key=True)

    staff = db.relationship('Staff', backref='staff_skill')
    skill = db.relationship('Skill', backref='staff_skill')

    def to_dict(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
   
    def get_staff_skill(self):
        return self.Skill_Name

class Role(db.Model):
    __tablename__ = 'Role'

    Role_Name = db.Column(db.String(20), primary_key=True)
    Role_Desc = db.Column(db.Text, nullable=False)

    def to_dict(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

class Access_Rights(db.Model):
    __tablename__ = 'Access_Rights'

    Access_ID = db.Column(db.Integer, primary_key=True)
    Access_Control_Name = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

class Skill(db.Model):
    __tablename__ = 'Skill'

    Skill_Name = db.Column(db.String(50), primary_key=True)
    Skill_Desc = db.Column(db.Text, nullable=False)

    def to_dict(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

class Listings(db.Model):
    __tablename__ = 'Listings'

    Listing_ID = db.Column(db.Integer, primary_key=True)
    Role_Name = db.Column(db.String(20), db.ForeignKey('Role.Role_Name'))
    Opening_Date = db.Column(db.Date, nullable=False, default=func.now())
    Closing_Date = db.Column(db.Date, nullable=False)

    role = db.relationship('Role', backref='listings')

    def to_dict(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

class Applications(db.Model):
    __tablename__ = 'Applications'

    Application_ID = db.Column(db.Integer, primary_key=True)
    ApplicationDate = db.Column(db.Integer, nullable=False)
    Listing_ID = db.Column(db.Integer, db.ForeignKey('Listings.Listing_ID'))
    Staff_ID = db.Column(db.Integer, db.ForeignKey('Staff.Staff_ID'))

    listing = db.relationship('Listings', backref='applications')
    staff = db.relationship('Staff', backref='applications')

    def to_dict(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

