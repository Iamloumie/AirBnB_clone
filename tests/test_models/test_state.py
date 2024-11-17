#!/usr/bin/python3
"""Unittest module for the State class"""

import unittest
import os
import sys

# Add parent directory to path to make imports work
sys.path.insert(0, os.path.abspath(os.path.join
                                   (os.path.dirname(__file__), '../..')))

from models.state import State
from models.base_model import BaseModel


class TestState(unittest.TestCase):
    """Test suite for the User class"""

    def setUp(self):
        """Set up test cases"""
        self.state = State()

    def tearDown(self):
        """Clean up after each test"""
        try:
            os.remove("file.json")
        except:
            pass

    def test_state_inherits_from_basemodel(self):
        """Test if State inherits from BaseModel"""
        self.assertIsInstance(self.state, BaseModel)

    def test_state_attributes(self):
        """Test State class attributes"""
        self.assertTrue(hasattr(self.state, "name"))
        self.assertEqual(self.state.name, "")

    def test_state_attributes_types(self):
        """Test if State attributes are the correct type"""
        self.assertIsInstance(self.state.name, str)

if __name__ == '__main__':
    unittest.main()
