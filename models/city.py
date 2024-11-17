#!/usr/bin/python3
"""
Module for the City class
"""
from models.base_model import BaseModel


class City(BaseModel):
    """City class inherits from the BaseModel class"""
    state_id = ""
    name = ""
