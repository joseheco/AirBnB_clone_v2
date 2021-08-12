#!/usr/bin/python3
"""DB_storage engine"""
from os import getenv
from models.base_model import BaseModel, Base
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
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                        .format(getenv('HBNB_MYSQL_USER'),
                                                getenv('HBNB_MYSQL_PWD'),
                                                getenv('HBNB_MYSQL_HOST'),
                                                getenv('HBNB_MYSQL_DB')),
                                                pool_pre_ping = True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)
    
    def all(self, cls=None):
        """query on database session"""
        dicc = {}
        cls_list = [State, City, Amenity, Review, Place, User]
        if cls:
            for obj in self.__session.query(eval(cls)).all():
                key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                dicc[key] = obj
        
        else:
            for item in cls_list:
                for obj in self.__session.query(item):
                    key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    dicc[key] = obj
        
        return dicc
    
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
        session_factory = sessionmaker(bind = self.__engine,
                                        expire_on_commit = False)
        self.__session = scoped_session(session_factory )