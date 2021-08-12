#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import os
import models
from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME

# tuve problemas de import cannot Base
if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        id = Column(String(60), primary_primary_key=True, nullable=False)
        created_at = Column(DATETIME, default=datetime.utcnow(),
                            nullable=False)
        updated_at = Column(DATETIME, default=datetime.utcnow(),
                            nullable=False)
    else:
        def __init__(self, *args, **kwargs):
            """Instatntiates a new model"""
            if not kwargs:
                from models import storage
                self.id = str(uuid.uuid4())
                self.created_at = datetime.now()
                self.updated_at = datetime.now()
                """ Move the models.storage.new(self) from
                def __init__(self, *args, **kwargs): to def save(self):
                    and call it just before models.storage.save() """
                """ storage.new(self) """
            else:
                """ In def __init__(self, *args, **kwargs):, manage kwargs to
                create instance attribute from this dictionary.
                Ex: kwargs={ 'name': "California" } => self.name = "California"
                if it’s not already the case """
                for key, value in kwargs.items():
                    if key == 'created_at' or key == 'updated_at':
                        # value: %y, %m, %d
                        time = '%Y-%m-%dT%H:%M:%S.%f'
                        setattr(self, key, datetime.strptime(value, time))
                    else:
                        if key != '__class__':
                            setattr(self, key, value)
                if "id" not in kwargs.keys():
                    self.id = str(uuid.uuid4())
                if "updated_at" not in kwargs.keys():
                    self.updated_at = datetime.now()
                if "created_at" not in kwargs.keys():
                    self.created_at = datetime.now()
                if self.__class__ in kwargs:
                    del kwargs['__class__']
                self.__dict__.update(kwargs)
                """ Move the models.storage.new(self) from
                def __init__(self, *args, **kwargs): to
                def save(self): and call it just before models.storage.save()
                """

        def __str__(self):
            """Returns a string representation of the instance"""
            cls = (str(type(self)).split('.')[-1]).split('\'')[0]
            return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

        def save(self):
            """Updates updated_at with current time when instance is changed"""
            from models import storage
            self.updated_at = datetime.now()
            storage.new(self)
            storage.save()

        def to_dict(self):
            """Convert instance into dict format"""
            dictionary = {}
            dictionary.update(self.__dict__)
            dictionary.update({'__class__':
                              (str(type(self)).split('.')[-1]).split('\'')[0]})
            dictionary['created_at'] = self.created_at.isoformat()
            dictionary['updated_at'] = self.updated_at.isoformat()
            """remove the key _sa_instance_state from the dictionary returned by
            this method only if this key exists"""
            if '_sa_instance_state' in dictionary:
                del dictionary['_sa_instance_state']
            return dictionary

        def delete(self):
            """delete the current instance from the storage (models.storage) by
            calling the method delete """
            models.storage.delete(self)
