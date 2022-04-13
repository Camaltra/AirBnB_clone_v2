#!/usr/bin/python3.8
"""This module defines a class User"""
from models.base_model import BaseModel, Base, storageType
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.place import Place


class User(BaseModel, Base):
    """
    This class defines a user by various attributes
    """
    if storageType == "db":
        __tablename__ = "users"
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user", cascade="all, delete")
        reviews = relationship("Review", backref="user", cascade="all, delete")
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
