#!/usr/bin/python3
# tests/test_user.py

import unittest
from models.user import User
from datetime import datetime

class TestUser(unittest.TestCase):
    """Test cases for the User class"""

    def setUp(self):
        """Set up test environment"""
        self.user = User()

    def test_user_instance(self):
        """Test that a new User instance is correctly created"""
        self.assertIsInstance(self.user, User)

    def test_user_attributes(self):
        """Test the attributes of the User class"""
        self.assertTrue(hasattr(self.user, "email"))
        self.assertEqual(self.user.email, "")
        self.assertTrue(hasattr(self.user, "password"))
        self.assertEqual(self.user.password, "")
        self.assertTrue(hasattr(self.user, "first_name"))
        self.assertEqual(self.user.first_name, "")
        self.assertTrue(hasattr(self.user, "last_name"))
        self.assertEqual(self.user.last_name, "")

    def test_user_to_dict(self):
        """Test to_dict method of User class"""
        user_dict = self.user.to_dict()
        self.assertEqual(user_dict["__class__"], "User")
        self.assertIsInstance(user_dict["created_at"], str)
        self.assertIsInstance(user_dict["updated_at"], str)
        self.assertEqual(user_dict["email"], "")
        self.assertEqual(user_dict["password"], "")
        self.assertEqual(user_dict["first_name"], "")
        self.assertEqual(user_dict["last_name"], "")

    def test_user_str(self):
        """Test the __str__ method of User class"""
        user_str = str(self.user)
        self.assertIn("[User]", user_str)
        self.assertIn("id", user_str)
        self.assertIn("created_at", user_str)
        self.assertIn("updated_at", user_str)

    def test_user_save(self):
        """Test the save method of User class"""
        old_updated_at = self.user.updated_at
        self.user.save()
        self.assertNotEqual(self.user.updated_at, old_updated_at)
        self.assertIsInstance(self.user.updated_at, datetime)

if __name__ == '__main__':
    unittest.main()
