import unittest

from model import Staff, Role_Skill, Staff_Skill, Role, Access_Rights, Skill, Listings, Applications

# Listings
class TestListings(unittest.TestCase):
    def setUp(self):
        self.l1 = Listings(Role_Name='Teacher', Closing_Date='2023-12-12')
        self.l2 = Listings(Role_Name='Doctor', Closing_Date='2023-12-08')
        self.l3 = Listings(Role_Name='Pianist', Closing_Date='2023-11-12')

    def tearDown(self):
        self.l1 = None
        self.l2 = None
        self.l3 = None

    def test_to_dict1(self):
        self.assertEqual(self.l1.to_dict(), {
            'Listing_ID': None,
            'Role_Name': 'Teacher',
            'Opening_Date': None,
            'Closing_Date': '2023-12-12'}
        )
    
    def test_to_dict2(self):    
        self.assertEqual(self.l2.to_dict(), {
            'Listing_ID': None,
            'Role_Name': 'Doctor',
            'Opening_Date': None,
            'Closing_Date': '2023-12-08'}
        )
    
    def test_to_dict3(self):
        self.assertEqual(self.l3.to_dict(), {
            'Listing_ID': None,
            'Role_Name': 'Pianist',
            'Opening_Date': None,
            'Closing_Date': '2023-11-12'}
        )


# Role Skills
class TestRoleSkill(unittest.TestCase):
    def test_to_dict(self):
        
        rs1 = Role_Skill(Role_Name='Account Manager', Skill_Name='Accounting')
        self.assertEqual(rs1.to_dict(), {
            'Role_Name': 'Account Manager',
            'Skill_Name': 'Accounting'}
        )
        
    def test_get_role_skill(self):
        # Test the get_role_skill method of Role_Skill
        role_skill = Role_Skill(Role_Name='Accounting Manager', Skill_Name='Accounting')
        skill_name = role_skill.get_role_skill()
        self.assertEqual(skill_name, 'Accounting')
     
        
# Staff Skills     
class TestStaffSkill(unittest.TestCase):
    def test_to_dict(self):
        
        # Test the to_dict method of Staff_Skill
        ss1 = Staff_Skill(Staff_ID='140001', Skill_Name='Accounting')
        result = ss1.to_dict()
        self.assertEqual(result, {
            'Staff_ID': '140001', 
            'Skill_Name': 'Accounting'}
        )

    def test_get_staff_skill(self):
        # Test the get_staff_skill method of Staff_Skill
        ss1 = Staff_Skill(Staff_ID='140001', Skill_Name='Accounting')
        skill_name = ss1.get_staff_skill()
        self.assertEqual(skill_name, 'Accounting')
        
        
if __name__ == "__main__":
    unittest.main()
