from application import app,db,limiter,redis_client
from application.apps.Category_app import categories
from application.apps.Category_app.model import Category
from flask import jsonify , request
import string

@categories.route("/" , methods = ["POST"])
def add_category():
    data = request.get_json()
    title = data['Title']
    icon = data['Icon']
    
    response = Category.add_category(title , icon)
    
    return response
    
    
    