#!/usr/bin/python3
"""Unittest module for the BaseModel class"""

import unittest
from datetime import datetime
import os
import sys

# Add parent directory to path to make imports work
sys.path.insert(0, os.path.abspath(os.path.join
                                   (os.path.dirname(__file__), '../..')))

from models.base_model import BaseModel

class TestBaseModel(unittest.TestCase):
    """Test suite for the BaseModel class"""

    def setUp(self):
        """Set up test cases"""
        self.base = BaseModel()

    def tearDown(self):
        """Clean up after each test"""
        try:
            os.remove("file.json")
        except:
            pass

    def test_id_generation(self):
        """Tests if id is generated correctly"""
        model1 = BaseModel()
        model2 = BaseModel()
        self.assertNotEqual(model1.id, model2.id)
        self.assertIsInstance(model1.id, str)

    def test_created_at_updated_at(self):
        """Test if timestamps are created correctly"""
        model = BaseModel()
        self.assertIsNotNone(model.created_at)
        self.assertIsNotNone(model.updated_at)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

    def test_save_method(self):
        """Test save method"""
        model = BaseModel()
        old_updated_at = model.updated_at
        model.save()
        self.assertNotEqual(old_updated_at, model.updated_at)

    def test_to_dict_method(self):
        """Test to_dict method"""
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertIn('__class__', model_dict)
        self.assertEqual(model_dict['__class__'], 'BaseModel')
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)
        self.assertIn('id', model_dict)

if __name__ == '__main__':
    unittest.main()
