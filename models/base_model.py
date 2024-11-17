#!/usr/bin/python3
"""
This module defines the BaseModel class which serves as the base
class for all models in the project
"""

import uuid
from datetime import datetime


class BaseModel:
    """
    BaseModel class defines all common attributes/methods for other
    classes
    """

    def __init__(self, *args, **kwargs):
        """Initializes new BaseModel instance
        Args:
        *args: Variabe length argument list(won't be used)
        **kwargs: Arbitrary keyword arguments to recreate instance
        """
        # Define the time format used in the dictionary
        time_format = "%Y-%m-%dT%H:%M:%S.%f"

        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key in ["created_at", "updated_at"]:
                        #convert string to datetime object
                        setattr(self, key, datetime.strptime(value, time_format))
                    else:
                        # Set the attribute to datetime object
                        setattr(self, key, value)
        else:
            # Creates a new instance with unique Id and time_format
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            # Add the new instance for storage
            storage.new(self)

    def __str__(self):
        """
        Returns string representation of the BaseModel instance
        format: [<class name>] (<self.id>) <self.__dict__>
        """

        return "[{}] ({}) {}".format(
                self.__class__.__name__,
                self.id,
                self.__dict__
        )

    def save(self):
        """Updates the updated_at attribute with current datetime"""
        from models import storage
        self.updated_at = datetime.now()
        # Save to storage
        storage.save()

    def to_dict(self):
        """Returns the dictionary representation of the BaseModel instance"""

        # start with a copy of the instance's dictionary
        result_dict = self.__dict__.copy()

        # Add class name
        result_dict['__class__'] = self.__class__.__name__

        # Convert datetime objects to ISO format strings
        result_dict['created_at'] = self.created_at.isoformat()
        result_dict['updated_at'] = self.updated_at.isoformat()

        return result_dict
