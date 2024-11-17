#!/usr/bin/python3
"""
Module for FileStorage class
"""

import json
import os


class FileStorage:
    """
    Serializes instances to JSON files and 
    Deserializes JSON files to instances
    """

    # Private class attributes
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        json_objects = {}

        # Convert each object to dictionary representation
        for key, obj in FileStorage.__objects.items():
            json_objects[key] = obj.to_dict()

        # Write to JSON file
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Deserializes the JSON file to instances"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                'BaseModel': BaseModel,
                'User': User,
                'Place': Place,
                'State': State,
                'City': City,
                'Amenity': Amenity,
                'Review': Review

                }

        try:
            if os.path.isfile(FileStorage.__file_path):
                with open (FileStorage.__file_path, 'r', encoding='utf-8') as f:
                    obj_dict = json.load(f)
                    for key, value in obj_dict.items():
                        class_name = value["__class__"]
                        # Create instance using dictionary
                        obj = classes[class_name](**value)
                        self.new(obj)
        except Exception:
            pass
