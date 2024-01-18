#!/usr/bin/python3
"""
This module defines a base class for all models
in our hbnb clone
"""
import uuid
from datetime import datetime
from os import getenv
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

base_type_storage = getenv("HBNB_TYPE_STORAGE")

if base_type_storage == 'db':
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        for key, value in kwargs.items():
            if key == '__class__':
                continue
            setattr(self, key, value)
            if type(self.created_at) is str:
                self.created_at = datetime.strptime(self.created_at, TIME_FORMAT)
            if type(self.updated_at) is str:    
                self.updated_at = datetime.strptime(self.updated_at, TIME_FORMAT)

    def __str__(self):
        """Returns a string representation of the instance"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_to_disk=False):
        """Returns a dictionary containing all keys/values of the instance"""
        new_dict = {**self.__dict__}

        for attr in ["created_at", "updated_at"]:
            if attr in new_dict:
                new_dict[attr] = new_dict[attr].isoformat()

        new_dict.pop('_sa_instance_state', None)

        if '_password' in new_dict:
            new_dict['password'] = new_dict.pop('_password')

        for excl_attr in ["amenities", "reviews"]:
            new_dict.pop(excl_attr, None)

        new_dict["__class__"] = self.__class__.__name__

        if not save_to_disk:
            new_dict.pop('password', None)

        return new_dict

    def delete(self):
        """Delete current instance from storage by calling its delete method"""
        models.storage.delete(self)
