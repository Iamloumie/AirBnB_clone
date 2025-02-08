#!/usr/bin/python3
"""
The basemodel script that defines all coomon attributes/methods
for other classes.
"""

import uuid
from datetime import datetime, timezone
import models.engine


class BaseModel:
    """The mother model for other classes"""

    def __init__(self, *args, **kwargs):
        """
        The entry point of the program
        """
        self.id = str(uuid.uuid4())

        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.fromisoformat(value))
                else:
                    setattr(self, key, value)

        models.storage.new(self)

    def save(self):
        """
        Saves the current time an instance is created
        when save method is called
        """
        self.updated_at = datetime.now(timezone.utc)
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all key values of instances"""
        inst_dict = self.__dict__.copy()  # making a copy of every dict created
        inst_dict["__class__"] = self.__class__.__name__

        # created_at and updated_at keys and values
        inst_dict["created_at"] = self.created_at.isoformat()
        inst_dict["updated_at"] = self.updated_at.isoformat()

        return inst_dict

    def __str__(self):
        """Prints the class name, id and dict of instances created"""
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)


if __name__ == "__main__":
    my_model = BaseModel()
    my_model.name = "My_First_Model"
    my_model.my_number = 89
    print(my_model.id)
    print(my_model)
    print(type(my_model.created_at))
    print("--")
    my_model_json = my_model.to_dict()
    print(my_model_json)
    print("JSON of my_model:")
    for key in my_model_json.keys():
        print(
            "\t{}: ({}) - {}".format(key,
                                     type(my_model_json[key]), my_model_json[key])
        )
    print("--")
    my_new_model = BaseModel(**my_model_json)
    print(my_new_model.id)
    print(my_new_model)
    print(type(my_new_model.created_at))

    print("--")
    print(my_model is my_new_model)
