#!/usr/bin/python3
"""Unittest module for the Review class"""

import unittest
import os
import sys

# Add parent directory to path to make imports work
sys.path.insert(0, os.path.abspath(os.path.join
                                   (os.path.dirname(__file__), '../..')))

from models.review import Review
from models.base_model import BaseModel


class TestReview(unittest.TestCase):
    """Test suite for the Review class"""

    def setUp(self):
        """Set up test cases"""
        self.review = Review()

    def tearDown(self):
        """Clean up after each test"""
        try:
            os.remove("file.json")
        except:
            pass

    def test_review_inherits_from_basemodel(self):
        """Test if Review inherits from BaseModel"""
        self.assertIsInstance(self.review, BaseModel)

    def test_review_attributes(self):
        """Test Review class attributes"""
        self.assertTrue(hasattr(self.review, "place_id"))
        self.assertTrue(hasattr(self.review, "user_id"))
        self.assertTrue(hasattr(self.review, "text"))
        self.assertEqual(self.review.place_id, "")
        self.assertEqual(self.review.user_id, "")
        self.assertEqual(self.review.text, "")

    def test_review_attributes_types(self):
        """Test if Review attributes are the correct type"""
        self.assertIsInstance(self.review.place_id, str)
        self.assertIsInstance(self.review.user_id, str)
        self.assertIsInstance(self.review.text, str)

if __name__ == '__main__':
    unittest.main()
