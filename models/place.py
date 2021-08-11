#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
import models
from models.review import Review


class Place(BaseModel):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    review = relationship('Review', cascade= 'all, delete', backref = 'place')
    review = relationship('Amenity')   #punto 10 por acabar con setter y getter

place_amenity = Table('place_amenity', Base.metadata,
                        Column('place_id', ForeignKey('places.id'),
                            nullable = False, String(60),
                            primary_key = True)
                        Column('amenity_id', String(60), 
                            ForeignKey('amenities.id'), nullable = False,
                            primary_key = True)
                    )


