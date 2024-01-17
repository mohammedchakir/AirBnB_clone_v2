#!/usr/bin/python3
"""This module defines the State class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class State(BaseModel, Base):
    """A State class for hbnb"""
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete-orphan")
