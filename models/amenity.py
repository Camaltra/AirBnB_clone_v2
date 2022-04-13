#!/usr/bin/python3.8
""" State Module for HBNB project """
from models.base_model import BaseModel, Base, storageType
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Amenity Class"""
    if storageType == "db":
        __tablename__ = "amenities"
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place", secondary="place_amenity",
                                       viewonly=False, back_populates="amenities")
    else:
        name = ""
