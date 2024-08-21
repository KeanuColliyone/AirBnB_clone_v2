#!/usr/bin/python3
"""
FileStorage module for handling storage of objects in JSON
"""

import json
from models.base_model import BaseModel
# Add all necessary imports for your models here

class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """Adds new object to __objects"""
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(self.__file_path, 'w') as f:
            temp = {}
            temp.update(self.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(self.__file_path, 'r') as f:
                for key, val in json.load(f).items():
                    self.__objects[key] = eval(val["__class__"])(**val)
        except FileNotFoundError:
            pass

    def close(self):
        """Deserializes the JSON file to objects"""
        self.reload()

