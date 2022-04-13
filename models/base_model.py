#!/usr/bin/python3.8
"""This module defines a base class for all models in our hbnb clone"""
import uuid
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import datetime
from os import getenv
from datetime import datetime

storageType = getenv("HBNB_TYPE_STORAGE")

if storageType == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
    if storageType == "db":
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """
        Instantiates a new model
        """
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if not "id" in kwargs:
                kwargs["id"] = str(uuid.uuid4())

            if not "updated_at" in kwargs:
                kwargs["updated_at"] = datetime.now()
            else:
                kwargs["updated_at"] = datetime.strptime(
                    kwargs['updated_at'],
                    '%Y-%m-%dT%H:%M:%S.%f'
                )

            if not "created_at" in kwargs:
                kwargs["created_at"] = datetime.now()
            else:
                kwargs["created_at"] = datetime.strptime(
                    kwargs['created_at'],
                    '%Y-%m-%dT%H:%M:%S.%f'
                )

            if "__class__" in kwargs:
                del kwargs["__class__"]

            for key, value in kwargs.items():
                setattr(self, key, value)

    def __str__(self):
        """
        Returns a string representation of the instance
        """
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """
        Updates updated_at with current time when instance is changed
        """
        from models import storage
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Convert instance into dict format
        """
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if "_sa_instance_state" in dictionary.keys():
            del dictionary["_sa_instance_state"]
        return dictionary

    def delete(self):
        """
        Delete the current instante from the storage
        """
        models.storage.delete(self)
