#!/usr/bin/python3
"""DB_storage engine"""
import unittest
import models
from os import getenv
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine


class DBStorage:
    '''DBStorage class : '''
    __engine = None
    __session = None

    def __init__(self):
        '''Create a new instance '''
        str_conn = 'mysql+mysqldb://{}:{}@{}/{}'\
            .format(getenv('HBNB_MYSQL_USER'),
                    getenv('HBNB_MYSQL_PWD'),
                    getenv('HBNB_MYSQL_HOST'),
                    getenv('HBNB_MYSQL_DB')),
        self.__engine = create_engine(str_conn, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on database session"""
        if not cls:
            res_list = self.__session.query(Amenity)
            res_list.extend(self.__session.query(City))
            res_list.extend(self.__session.query(Place))
            res_list.extend(self.__session.query(Review))
            res_list.extend(self.__session.query(State))
            res_list.extend(self.__session.query(User))
        else:
            res_list = res_list = self.__session.query(cls)
        return {'{}.{}'.format(type(obj).__name__, obj.id): obj
                for obj in res_list}

    def new(self, obj):
        """ add object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current db session """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current db session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ create tables in db and create db session """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
