#!/usr/bin/python3

"""
Module for the Review class
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Review class inherits the BaseModel class"""
    place_id = ""
    user_id = ""
    text = ""
