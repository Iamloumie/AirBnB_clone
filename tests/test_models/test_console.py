#!/usr/bin/python3
"""Unit tests for console.py"""
import unittest
from unittest.mock import patch
from io import StringIO
import os
import sys
import json

# Add parent directory to path to make console importable
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)

from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage


class TestHBNBCommand(unittest.TestCase):
    """Test cases for the HBNBCommand class"""

    def setUp(self):
        """Set up test environment"""
        self.console = HBNBCommand()
        self.classes = {
            'BaseModel': BaseModel,
            'User': User,
            'Place': Place,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Review': Review
        }

    def tearDown(self):
        """Clean up test environment"""
        storage._FileStorage__objects = {}
        if storage._FileStorage__file_path:
            try:
                os.remove(storage._FileStorage__file_path)
            except:
                pass

    def test_help_commands(self):
        """Test help command output"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help show")
            output = f.getvalue()
            self.assertIn("Shows an individual instance of a class", output)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help create")
            output = f.getvalue()
            self.assertIn("Creates a class of any type", output)

    def test_create(self):
        """Test create command"""
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {class_name}")
                obj_id = f.getvalue().strip()
                self.assertTrue(len(obj_id) > 0)
                key = f"{class_name}.{obj_id}"
                self.assertIn(key, storage._FileStorage__objects)

        # Test invalid class name
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create InvalidClass")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

        # Test missing class name
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")

    def test_show(self):
        """Test show command"""
        # Test with valid class and id
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {class_name}")
                obj_id = f.getvalue().strip()

            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"show {class_name} {obj_id}")
                output = f.getvalue().strip()
                self.assertIn(obj_id, output)
                self.assertIn(class_name, output)

            # Test dot notation
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"{class_name}.show({obj_id})")
                output = f.getvalue().strip()
                self.assertIn(obj_id, output)
                self.assertIn(class_name, output)

        # Test invalid class
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show InvalidClass 1234-1234")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

        # Test invalid id
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel invalid_id")
            self.assertEqual(f.getvalue().strip(), "** no instance found **")

    def test_destroy(self):
        """Test destroy command"""
        # Test with valid class and id
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {class_name}")
                obj_id = f.getvalue().strip()
                key = f"{class_name}.{obj_id}"

            # Verify object exists
            self.assertIn(key, storage._FileStorage__objects)
            
            # Test destroy command
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"destroy {class_name} {obj_id}")
                self.assertNotIn(key, storage._FileStorage__objects)

            # Test dot notation
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {class_name}")
                obj_id = f.getvalue().strip()
                key = f"{class_name}.{obj_id}"

            self.assertIn(key, storage._FileStorage__objects)
            HBNBCommand().onecmd(f"{class_name}.destroy({obj_id})")
            self.assertNotIn(key, storage._FileStorage__objects)

    def test_all(self):
        """Test all command"""
        # Create some objects
        for class_name in self.classes:
            HBNBCommand().onecmd(f"create {class_name}")

        # Test all with no class name
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all")
            output = f.getvalue().strip()
            self.assertIn("BaseModel", output)
            self.assertIn("User", output)

        # Test all with valid class name
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"all {class_name}")
                output = f.getvalue().strip()
                self.assertIn(class_name, output)

        # Test dot notation
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"{class_name}.all()")
                output = f.getvalue().strip()
                self.assertIn(class_name, output)

    def test_count(self):
        """Test count command"""
        counts = {}
        
        # Create some objects and track counts
        for class_name in self.classes:
            counts[class_name] = 2
            for _ in range(2):
                HBNBCommand().onecmd(f"create {class_name}")

        # Test count for each class
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"count {class_name}")
                count = int(f.getvalue().strip())
                self.assertEqual(count, counts[class_name])

            # Test dot notation
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"{class_name}.count()")
                count = int(f.getvalue().strip())
                self.assertEqual(count, counts[class_name])

    def test_update(self):
        """Test update command"""
        for class_name in self.classes:
            # Create an object
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {class_name}")
                obj_id = f.getvalue().strip()

            # Test update with string attribute
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f'update {class_name} {obj_id} name "test_name"')
                key = f"{class_name}.{obj_id}"
                obj = storage._FileStorage__objects[key]
                self.assertEqual(obj.name, "test_name")

            # Test update with integer attribute (if applicable)
            if class_name in ['Place']:
                with patch('sys.stdout', new=StringIO()) as f:
                    HBNBCommand().onecmd(f'update {class_name} {obj_id} number_rooms 5')
                    key = f"{class_name}.{obj_id}"
                    obj = storage._FileStorage__objects[key]
                    self.assertEqual(obj.number_rooms, 5)

            # Test dot notation
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f'{class_name}.update("{obj_id}", "city", "San Francisco")')
                key = f"{class_name}.{obj_id}"
                obj = storage._FileStorage__objects[key]
                self.assertEqual(obj.city, "San Francisco")

            # Test update with dictionary
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f'{class_name}.update("{obj_id}", {{"state": "California", "stars": 5}})')
                key = f"{class_name}.{obj_id}"
                obj = storage._FileStorage__objects[key]
                self.assertEqual(obj.state, "California")
                self.assertEqual(obj.stars, 5)

    def test_quit_and_EOF(self):
        """Test quit and EOF commands"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd("quit"))

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd("EOF"))

    def test_emptyline(self):
        """Test empty line input"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("")
            self.assertEqual(f.getvalue(), "")


if __name__ == '__main__':
    unittest.main()
