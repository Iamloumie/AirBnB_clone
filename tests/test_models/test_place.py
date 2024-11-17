#!/usr/bin/python3
"""Unittest module for the Place Class."""


import unittest
import os
import sys

# Add parent directory to path to make imports work
sys.path.insert(0, os.path.abspath
                (os.path.join(os.path.dirname(__file__), '../..')))

from models.place import Place
from models.base_model import BaseModel


class TestPlace(unittest.TestCase):
    """Test suite for the Place class"""

    def setUp(self):
        """Set up test cases"""
        self.place = Place()

    def tearDown(self):
        """Clean up after each test"""
        try:
            os.remove("file.json")
        except:
            pass

    def test_place_inherits_from_basemodel(self):
        """Test if Place inherits from BaseModel"""
        self.assertIsInstance(self.place, BaseModel)

    def test_place_attributes(self):
        """Test Place class attributes"""
        # Test string attributes
        self.assertTrue(hasattr(self.place, "city_id"))
        self.assertTrue(hasattr(self.place, "user_id"))
        self.assertTrue(hasattr(self.place, "name"))
        self.assertTrue(hasattr(self.place, "description"))
        self.assertEqual(self.place.city_id, "")
        self.assertEqual(self.place.user_id, "")
        self.assertEqual(self.place.name, "")
        self.assertEqual(self.place.description, "")

        # Test integer attributes
        self.assertTrue(hasattr(self.place, "number_rooms"))
        self.assertTrue(hasattr(self.place, "number_bathrooms"))
        self.assertTrue(hasattr(self.place, "max_guest"))
        self.assertTrue(hasattr(self.place, "price_by_night"))
        self.assertEqual(self.place.number_rooms, 0)
        self.assertEqual(self.place.number_bathrooms, 0)
        self.assertEqual(self.place.max_guest, 0)
        self.assertEqual(self.place.price_by_night, 0)

        # Test float attributes
        self.assertTrue(hasattr(self.place, "latitude"))
        self.assertTrue(hasattr(self.place, "longitude"))
        self.assertEqual(self.place.latitude, 0.0)
        self.assertEqual(self.place.longitude, 0.0)

        # Test list attribute
        self.assertTrue(hasattr(self.place, "amenity_ids"))
        self.assertEqual(self.place.amenity_ids, [])

    def test_place_attributes_types(self):
        """Test if Place attributes are the correct type"""
        # Test string attributes types
        self.assertIsInstance(self.place.city_id, str)
        self.assertIsInstance(self.place.user_id, str)
        self.assertIsInstance(self.place.name, str)
        self.assertIsInstance(self.place.description, str)

        # Test integer attributes types
        self.assertIsInstance(self.place.number_rooms, int)
        self.assertIsInstance(self.place.number_bathrooms, int)
        self.assertIsInstance(self.place.max_guest, int)
        self.assertIsInstance(self.place.price_by_night, int)

        # Test float attributes types
        self.assertIsInstance(self.place.latitude, float)
        self.assertIsInstance(self.place.longitude, float)

        # Test list attribute type
        self.assertIsInstance(self.place.amenity_ids, list)

    def test_place_str_representation(self):
        """Test string representation of Place instance"""
        string = str(self.place)
        self.assertIn("[Place]", string)
        self.assertIn("id", string)
        self.assertIn("created_at", string)
        self.assertIn("updated_at", string)


if __name__ == '__main__':
    unittest.main()
