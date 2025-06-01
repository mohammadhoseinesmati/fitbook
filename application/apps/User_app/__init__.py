from flask import Blueprint

users = Blueprint('users' , __name__ , url_prefix='/user')

from application.apps.User_app.model import User,Wallet
from application.apps.User_app.views import signup,signupgoogle