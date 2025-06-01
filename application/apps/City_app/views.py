from application.apps.City_app import cities
from application.apps.City_app.model import City
from application import db , app
from flask import request ,jsonify

@cities.route('/db_create' , methods = ['POST'])
def db_create():
      try:
            with app.app_context():
               db.create_all()
            return jsonify({'message' : "create db success ...!"}),200
      except Exception as e:
            return jsonify({'message' : f"an error exist : {e}"}),400
      
@cities.route('/db_delete' , methods = ['POST'])
def db_delete():
      try:
            with app.app_context():
               db.drop_all()
            return jsonify({'message' : "delete db success ...!"}),200
      except Exception as e:
            return jsonify({'message' : f"an error exist : {e}"}),400





@cities.route('/' , methods=['POST'])
def index():
      data = request.get_json()
      name_fa =data['name_fa']
      name_en= data['name_en']

      city_list = [
    {'name_fa': f'{name_fa}', 'name_en': f'{name_en}'}
]
      result=City.add_cities_to_db(city_list)
      return result

@cities.route('/' , methods=['GET'])
def get_cities():
      data = request.get_json()
      cities = []
      mylist =City.query.all()
      if data['lan'] == 'en':
            for i in mylist:
                  cities.append(i.name_en)

      else:
            for i in mylist:
                  cities.append(i.name_fa)
      return jsonify(cities)


      
       
       
                        
        
