#!/usr/bin/python3
"""Unittest module for the Amenity class"""

import unittest
import os
import sys

# Add parent directory to path to make imports work
sys.path.insert(0, os.path.abspath(os.path.join
                                   (os.path.dirname(__file__), '../..')))

from models.amenity import Amenity
from models.base_model import BaseModel


class TestAmenity(unittest.TestCase):
    """Test suite for the Amenity class"""

    def setUp(self):
        """Set up test cases"""
        self.amenity = Amenity()

    def tearDown(self):
        """Clean up after each test"""
        try:
            os.remove("file.json")
        except:
            pass

    def test_amenity_inherits_from_basemodel(self):
        """Test if Amenity inherits from BaseModel"""
        self.assertIsInstance(self.amenity, BaseModel)

    def test_amenity_attributes(self):
        """Test Amenity class attributes"""
        self.assertTrue(hasattr(self.amenity, "name"))
        self.assertEqual(self.amenity.name, "")

    def test_amenity_attributes_types(self):
        """Test if Amenity attributes are the correct type"""
        self.assertIsInstance(self.amenity.name, str)

    def test_amenity_representation(self):
        """Test string representation of Amenity instance"""
        string = str(self.amenity)
        self.assertIn("[Amenity]", string)
        self.assertIn("id", string)
        self.assertIn("created_at", string)
        self.assertIn("updated_at", string)


if __name__ == '__main__':
    unittest.main()
