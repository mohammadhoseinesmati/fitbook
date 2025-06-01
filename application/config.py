import os
from dotenv import load_dotenv

load_dotenv()
class Config:
       SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI') 
       SQLALCHEMY_TRACK_MODIFICATIONS = False 
       SECRET_KEY = os.getenv('SECRET_KEY')
        #google
       client_id = os.getenv('client_id'),
       client_secret = os.getenv('client_secret'),
       authorize_url = os.getenv('authorize_url'),
       access_token_url = os.getenv('access_token_url')
       #mail
       MAIL_SERVER=os.getenv('MAIL_SERVER')
       MAIL_PORT=os.getenv('MAIL_PORT')
       MAIL_USE_TLS=os.getenv('MAIL_USE_TLS')
       MAIL_USERNAME=os.getenv('MAIL_USERNAME')
       MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
       MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER')
      

class Development(Config):
       pass

class Production(Config):
       pass