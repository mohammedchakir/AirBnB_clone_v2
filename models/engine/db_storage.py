#!/usr/bin/python3
"""This module defines the DBStorage class"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.state import State
from models.city import City

class DBStorage:
    """DBStorage class for hbnb"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiates a new DBStorage"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session (self.__session)"""
        classes = [State, City]
        result = {}
        if cls:
            classes = [cls]
        for c in classes:
            objects = self.__session.query(c).all()
            for obj in objects:
                key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                result[key] = obj
        return result

    def new(self, obj):
        """Add the object to the current database session (self.__session)"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session (self.__session)"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session (self.__session)"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database (feature of SQLAlchemy)"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

