#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base, storageType
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.review import Review

class Place(BaseModel, Base):
    """ A place to stay """
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
        latitude = Column(Float, nullable=False)
        longitude = Column(Float, nullable=False)
        reviews = relationship("Review", backref="place", cascade="all, delete")
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
