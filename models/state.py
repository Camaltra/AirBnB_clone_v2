#!/usr/bin/python3.8
""" State Module for HBNB project """
from models.base_model import BaseModel, Base, storageType
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.city import City
import models


class State(BaseModel, Base):
    """State class"""

    if storageType == "db":
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="all, delete")
    else:
        name = ""

        @property
        def cities(self):
            """
            Getter for all linked cities of a
            state
            Args:
                self (class instance)
            """
            listCity = []
            for city in models.storage.all(City).value():
                if city.state_id == self.id:
                    listCity.append(city)
            return listCity
