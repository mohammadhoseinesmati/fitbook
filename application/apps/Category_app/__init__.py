from flask import Blueprint

categories = Blueprint('categories' , __name__ , url_prefix='/category')

from application.apps.Category_app import views
