from application import db
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, Numeric, ForeignKey , Text , Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func 
from flask import jsonify
from datetime import datetime 
from application.utils import Password_Hash
from application.apps.Gym_app import model
from sqlalchemy.exc import SQLAlchemyError


class Category(db.Model):
    __tablename__ = 'Category'
    
    id = Column(Integer , primary_key= True , autoincrement=True)
    Title = Column(String(25) , nullable=False , unique= True)
    Icon = Column(String(200) , nullable= True)
    
    gyms_category = relationship('Gyms_Category' , backref='categorys')
    options = relationship('Gyms_Options', backref='categories')
    
    def add_category(title , icon = None):
       try:
            new_category = Category(Title = title , Icon = icon)
            db.session.add(new_category)
            db.session.commit()
            
            return jsonify({"message" : f"add {title} Category is succed"}) , 200
        
       except SQLAlchemyError as es:
           return jsonify({'error': es,}), 400
       
    def delete_category(id):
        category = Category.query.filter(Category.id == id).first()
        
        if category == None:
            return jsonify({"error" : "category is not exist"}), 400
        
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({"message" : f"delete {category.Title1} is succed1"}) ,200
    
    def select_category(title) :
        category = Category.query.filter(Category.Title == title).first()
        
        if category == None:
            return None , 400
        
        return category , 200
             
            
    
