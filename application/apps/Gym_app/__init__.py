from flask import Blueprint

gyms = Blueprint('gyms' , __name__ , url_prefix='/gym')

from application.apps.Gym_app import views
