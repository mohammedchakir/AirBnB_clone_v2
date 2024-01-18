#!/usr/bin/python3
"""This module defines the Place class"""

from os import getenv
from sqlalchemy import Column, String, Integer, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models

STORAGE_TYPE = getenv('HBNB_TYPE_STORAGE')

if STORAGE_TYPE == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60), ForeignKey('places.id'),
                                 primary_key=True, nullable=False),
                          Column('amenity_id', String(60), ForeignKey('amenities.id'),
                                 primary_key=True, nullable=False)
                         )


class Place(BaseModel, Base):
    """A Place class for hbnb"""

    if STORAGE_TYPE == 'db':
        __tablename__ = 'places'

        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)

        reviews = relationship("Review", cascade="all, delete", backref="places")
        amenities = relationship("Amenity", secondary='place_amenity',
                                 viewonly=False, backref="place_amenities")
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

    def __init__(self, *args, **kwargs):
        """Initializes Place"""
        super().__init__(*args, **kwargs)

    @property
    def reviews(self):
        """Attribute returns a list of Review instances"""
        return [review for review in models.storage.all("Review").
                values() if review.place_id == self.id]

    if STORAGE_TYPE != 'db':
        @property
        def amenities(self):
            """Attribute returns a list of Amenity instances"""
            return [amenity for amenity in models.storage.all("Amenity").
                    values() if amenity.place_id == self.id]
