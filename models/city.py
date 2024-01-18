#!/usr/bin/python3
"""City class definition"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class City(BaseModel, Base):
    """A City class for hbnb"""

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'cities'
        
        # Columns
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

        # Relationship with Place
        places = relationship("Place", backref="cities",
                              cascade="all, delete-orphan")
    else:
        # Default values when not using a database
        name = ""
        state_id = ""

    def __init__(self, *args, **kwargs):
        """Initialize the City instance"""
        super().__init__(*args, **kwargs)
