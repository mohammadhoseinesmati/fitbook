from flask import Blueprint

halls = Blueprint('halls' , __name__ , url_prefix='/hall')

from application.apps.Hall_app import views
