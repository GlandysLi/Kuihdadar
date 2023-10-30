import unittest
from unittest.mock import MagicMock
from model import Staff, Role, Role_Skill, Staff_Skill

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
        
if __name__ == '__main__':
    unittest.main()