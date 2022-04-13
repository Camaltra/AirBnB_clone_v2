#!/usr/bin/python3.8
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base, storageType
from sqlalchemy import Table, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.review import Review
from models.amenity import Amenity
import models

if storageType == "db":
    place_amenity = Table('place_amenity', Base.metadata,
                          Column("place_id", String(60),
                                 ForeignKey(
                                     "places.id", onupdate="CASCADE",
                                     ondelete="CASCADE"),
                                 primary_key=True, nullable=False),
                          Column("amenity_id", String(60),
                                 ForeignKey(
                                     "amenities.id", onupdate="CASCADE",
                                     ondelete="CASCADE"),
                                 primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """
    A place to stay
    """
    if storageType == "db":
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="place",
                               cascade="all, delete")
        amenities = relationship("Amenity", secondary="place_amenity",
                                 viewonly=False,
                                 back_populates="place_amenities")
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """
            Getter that returns the list of Review instances
            with place_id equals to the current Place.id
            """
            listReview = []
            for review in models.storage.all(Review).value():
                if review.place_id == self.id:
                    listReview.append(review)
            return listReview

        @property
        def amenities(self):
            """ get list amenty.ids """
            return self.amenity_ids

        @amenities.setter
        def amenities(self):
            """ set amenities """
            self.amenity_ids = []
            for k in storage.__object:
                if (k["__class__"] == "Amenity") and k["amenity_id"] == self.id:
                    self.amenity_ids.append(k.id)
