#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base, storageType
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship


class Amenity(BaseModel):
    if storageType == "db":
        __tablename__ = "amenities"
        name = Column(String(128), nullable=False)
        #place_amenities = relationship('Place', secondary=place_amenity, backref="places")

    else:
        name = ""
