#!/usr/bin/python3.8
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base, storageType
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """
    Review classto store review information
    """

    if storageType == "db":
        __tablename__ = "reviews"
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""
