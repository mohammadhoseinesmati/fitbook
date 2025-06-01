from flask import Blueprint

cities = Blueprint('cities' , __name__ , url_prefix='/city/')

from application.apps.City_app import views
