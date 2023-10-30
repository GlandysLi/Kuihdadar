import unittest
# import flask_testing
import json
from app import app, db
from model import Staff, Role, Role_Skill, Staff_Skill

# class TestApp(flask_testing.TestCase):
#     app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
#     app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
#     app.config['TESTING'] = True
#     self.client = app.test_client()

#     def create_app(self):
#         return app

#     def setUp(self):
#         db.create_all()

#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()



class TestSkillByStaffEndpoint(unittest.TestCase):
    def setUp(self):
        # Set up a test client and configure it for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
        app.config['TESTING'] = True
        self.client = app.test_client()

        # Create and set up the testing database, and add test data
        with app.app_context():
            db.create_all()
            staff_skill1 = Staff_Skill(Staff_ID=1, Skill_Name='Skill1')
            staff_skill2 = Staff_Skill(Staff_ID=1, Skill_Name='Skill2')
            db.session.add(staff_skill1)
            db.session.add(staff_skill2)
            db.session.commit()

    def tearDown(self):
        # Remove test data and the testing database
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_skill_by_staff(self):
        # Test the endpoint for getting skills by staff ID
        response = self.client.get('/staff_skills/1')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['data'], ['Skill1', 'Skill2'])

    def test_get_skill_by_staff_not_found(self):
        # Test the endpoint for a staff ID that doesn't exist
        response = self.client.get('/staff_skills/999')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Staff Skill not found.')

if __name__ == '__main__':
    unittest.main()
