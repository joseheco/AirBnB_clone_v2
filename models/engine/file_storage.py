#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        """ Update the prototype of def all(self) to def all(self, cls=None)
        - that returns the list of objects of one type of class. Example below
        with State - it’s an optional filtering"""
        if cls is None:
            return FileStorage.__objects
        return {key: val for key, val in FileStorage.__objects.items()
                if type(val) == cls}

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def delete(self, obj=None):
        """Add a new public instance method: def delete(self, obj=None):
        to delete obj from __objects if it’s inside - if obj is equal to None,
        the method should not do anything"""
        if not obj:
            return
        del FileStorage.__objects['{}.{}'.format(type(obj).__name__, obj.id)]
        # return FileStorage.__objects
    
    def close(self):
        """Deserializes the JSON file to objects"""
        self.reload()

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                        self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass
