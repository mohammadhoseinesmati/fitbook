from flask import Flask , jsonify , request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from rauth import OAuth2Service
from sqlalchemy import text
from flasgger import Swagger
import redis



from application.config import Development


app = Flask(__name__)
app.config.from_object(Development)

db = SQLAlchemy(app)
migrate = Migrate(app , db)

mail = Mail(app)
jwt_manage = JWTManager(app)

limiter = Limiter(
     get_remote_address,
     app=app,
     default_limits=["200 per day", "50 per hour"]
)

google_oauth = OAuth2Service(
        name='google',
        client_id= str(Development.client_id[0])  ,
        client_secret= str(Development.client_secret[0]) ,
        authorize_url= str(Development.authorize_url[0]),
        access_token_url= str(Development.access_token_url)
)
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Fitbook Api",
        "description": "API description",
        "version": "1.0.0"
    }
})
redis_client = redis.StrictRedis(host='redis', port=6379, db=0)


@app.errorhandler(429)
def ratelimit_handler(e):
    data = request.get_json()
    language_code = data['language_code']

    if language_code == 'en':
        message = 'You have made too many requests. Please try again later.'
    else:
        message = 'شما درخواست‌های زیادی ارسال کرده‌اید. لطفاً بعداً دوباره تلاش کنید.'
    
    return jsonify({
        'message': message,
    }), 429







@app.route('/')
def home():
        """
          Home endpoint for the Fitbook application.
    ---
    responses:
      200:
        description: A successful response with a welcome message
        schema:
          type: object
          properties:
            message:
              type: string
              example: "hello to fitbook"
        """
        redis_client.set('key', 'Hello, Redis!', ex=30)
        return {'message' : "hello to fitbook",
                


                }


@app.route('/test')
def test_db():
    """
    Test the database connection.
    ---
    responses:
      200:
        description: A successful response indicating database connection
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Database connection successful!"
      500:
        description: A failed response indicating database connection issue
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Database connection failed: [error details]"
    """
    value = redis_client.get('key')
    try:
        # Use text() to declare the SQL expression
        result = db.session.execute(text('SELECT 1'))
        return jsonify({'message' : f"Database connection successful! __ {value}"}),200
    except Exception as e:
        return jsonify({"message" : f"Database connection failed: {value}"}),500


from application.apps.City_app import cities
from application.apps.User_app import users
from application.apps.Gym_app import gyms
from application.apps.Category_app import categories
from application.apps.Hall_app import halls

app.register_blueprint(cities)
app.register_blueprint(users)
app.register_blueprint(gyms)
app.register_blueprint(categories)
app.register_blueprint(halls)


