#!/usr/bin/python3
"""This module defines the City class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class City(BaseModel, Base):
    """A City class for hbnb"""
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    places = relationship('Place', backref='city', cascade='all, delete-orphan')
