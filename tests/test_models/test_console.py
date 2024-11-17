#!/us/bin/python3
"""Unittest module for the Console (HBNBCommand) class"""

import unittest
import os
import sys
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestHBNBCommand (unittest.TestCase):
    """Test suite for the HBNBCommand class"""

    @classmethod
    def setUpClass(cls):
        """Set up test class"""
        cls.console = HBNBCommand()

    def setUp(self):
        """Set up for each test"""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        storage._FileStorage__objects = {}

    def tearDown(self):
        """Clean up after each test"""
        try:
            os.remove = ("file.json")
        except FileNotFoundError:
            pass

    def test_module_docstring(self):
        """Test for module docstring"""
        self.assertIsNot(self.console.__doc__, None,
                         "console.py needs a docstring")
        self.assertTrue(len(self.console.__doc__) >= 1,
                        "console.py needs a docstring")

    def test_class_docstring(self):
        """Test for class docstring"""
        self.assertIsNot(HBNBCommand.__doc__, None,
                         "HBNBCommand class needs a docstring")
        self.assertTrue(len(HBNBCommand.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")

    def test_quit(self):
        """Test quit command"""
        with self.assertRaises(SystemExit):
            self.console.onecmd("quit")

    def test_EOF(self):
        """Test EOF command"""
        with self.assertRaises(SystemExit):
            self.console.onecmd("EOF")

    def test_emptyline(self):
        """Test empty line"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("\n")
            self.assertEqual(f.getvalue(), "")

    def test_create(self):
        """Test create command"""
        # Test with missing class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create")
            self.assertEqual(f.getvalue().strip(),
                             "** class name missing **")

        # Test with invalid class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create MyModel")
            self.assertEqual(f.getvalue().strip(),
                             "** class doesn't exist **")

        # Test with valid class
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            self.assertRegex(f.getvalue().strip(),
                             '^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')

    def test_show(self):
        """Test show command"""
        # Test with missing class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show")
            self.assertEqual(f.getvalue().strip(),
                             "** class name missing **")

        # Test with invalid class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show MyModel")
            self.assertEqual(f.getvalue().strip(),
                             "** class doesn't exist **")

        # Test with missing instance id
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show BaseModel")
            self.assertEqual(f.getvalue().strip(),
                             "** instance id missing **")

    def test_destroy(self):
        """Test destroy command"""
        # Test with missing class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy")
            self.assertEqual(f.getvalue().strip(),
                             "** class name missing **")

        # Test with invalid class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy MyModel")
            self.assertEqual(f.getvalue().strip(),
                             "** class doesn't exist **")

        # Test with missing instance id
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy BaseModel")
            self.assertEqual(f.getvalue().strip(),
                             "** instance id missing **")

    def test_all(self):
        """Test all command"""
        # Test with invalid class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all MyModel")
            self.assertEqual(f.getvalue().strip(), "[]")

        # Test with valid class
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            self.console.onecmd("all BaseModel")
            self.assertIn("BaseModel", f.getvalue())

    def test_update(self):
        """Test update command"""
        # Test with missing class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update")
            self.assertEqual(f.getvalue().strip(),
                             "** class name missing **")

        # Test with invalid class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update MyModel")
            self.assertEqual(f.getvalue().strip(),
                             "** class doesn't exist **")

        # Test with missing instance id
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update BaseModel")
            self.assertEqual(f.getvalue().strip(),
                             "** instance id missing **")

    def test_count(self):
        """Test count command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            self.console.onecmd("count BaseModel")
            self.assertEqual(f.getvalue().strip()[-1], "1")


if __name__ == '__main__':
    unittest.main()
