#!/usr/bin/python3
"""This module defines the Amenity class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey('amenities.id'),
                             primary_key=True, nullable=False)
                      )

class Amenity(BaseModel, Base):
    """A Amenity class for hbnb"""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    place_amenities = relationship('Place', secondary=place_amenity, viewonly=False)
