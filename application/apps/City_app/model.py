from application import db
from sqlalchemy import Column,Integer, String
from sqlalchemy.orm import relationship
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from application.apps.Gym_app import model

class City(db.Model):
    __tablename__ = 'City'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_fa = Column(String(64), nullable=False, unique=True)
    name_en = Column(String(64), nullable=False, unique=True)
    
    # Relationship
    users = relationship('User', backref='City', lazy='dynamic')
    gyms = relationship('Gym', backref='City', lazy='dynamic')
    halls = relationship('Halls', backref='City', lazy='dynamic')

    def add_cities_to_db(city_list):
         response = {'added': [], 'errors': []}

         try:
             for city in city_list:
                 new_city = City(name_fa=city['name_fa'], name_en=city['name_en'])
                 db.session.add(new_city)

             db.session.commit()
             response['added'] = [city['name_fa'] for city in city_list]
             return jsonify({'message': 'Cities added successfully', 'data': response}), 200

         except SQLAlchemyError as e:
             db.session.rollback()
             response['errors'].append(str(e))
             return jsonify({'message': 'Error occurred', 'data': response}), 400