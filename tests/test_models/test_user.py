#!/usr/bin/python3
"""Unittest module for the User class"""

import unittest
import os
import sys
from models.base_model import BaseModel
from models.user import User

# Add parent directory to path to make imports work
sys.path.insert(0, os.path.abspath(os.path.join
                                   (os.path.dirname(__file__), '../..')))




class TestUser(unittest.TestCase):
    """Test suite for the User class"""

    def setUp(self):
        """Set up test cases"""
        self.user = User()

    def tearDown(self):
        """Clean up after each test"""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_user_inherits_from_basemodel(self):
        """Test if User inherits from BaseModel"""
        self.assertIsInstance(self.user, BaseModel)

    def test_user_attributes(self):
        """Test User class attributes"""
        self.assertTrue(hasattr(self.user, "email"))
        self.assertTrue(hasattr(self.user, "password"))
        self.assertTrue(hasattr(self.user, "first_name"))
        self.assertTrue(hasattr(self.user, "last_name"))
        self.assertEqual(self.user.email, "")
        self.assertEqual(self.user.password, "")
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")

    def test_user_attributes_types(self):
        """Test if User attributes are the correct type"""
        self.assertIsInstance(self.user.email, str)
        self.assertIsInstance(self.user.password, str)
        self.assertIsInstance(self.user.first_name, str)
        self.assertIsInstance(self.user.last_name, str)

if __name__ == '__main__':
    unittest.main()
