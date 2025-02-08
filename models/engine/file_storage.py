#!/usr/bin/python3

"""
FileStorage Model
"""

import json
import os
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


class FileStorage:
    """
    storing, creating and retreving objects/instances
    """

    __file_path = "file.json"
    __objects = {}

    def new(self, obj):
        """creating new method to add objects to class attributes (storage)"""
        obj_cls_name = obj.__class__.__name__
        key = "{}.{}".format(obj_cls_name, obj.id)
        FileStorage.__objects[key] = obj

    def all(self):
        """
        for retrieving stored data in obj dictionary
        """
        return FileStorage.__objects

    def save(self):
        """
        (serialize) to save obj to json format for storing (reusing)
        """
        all_objs = FileStorage.__objects
        obj_dict = {}

        for obj in all_objs.keys():
            obj_dict[obj] = all_objs[obj].to_dict()
        with open(FileStorage.__file_path, "w", encoding="utf-8") as file:
            json.dump(obj_dict, file)

    def reload(self):
        """
        deserializes (converting json file to python object)
        """
        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r", encoding="utf-8") as file:
                try:
                    obj_dict = json.load(file)

                    for key, values in obj_dict.items():
                        class_name, obj_id = key.split(".")

                        cls = eval(class_name)

                        instance = cls(**values)

                        FileStorage.__objects[key] = instance
                except Exception:
                    pass
