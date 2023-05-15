import os
from flask import Flask
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_restful import Resource, Api
# from flask_bootstrap import Bootstrap


app = None
api = None
# bootstrap = Bootstrap(app)
def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
      raise Exception("Currently no production config is setup.")
    else:
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    return app, api

app,api = create_app()

# app = Flask(__name__, template_folder='E:\Developement\Book_my_Show\templates')
# Import all the controllers so they are loaded
from application.controllers import *

# Import all the api routes so
from application.api import *
api.add_resource(CinemaAPI, '/api/cinema','/api/resource', '/api/cinema/<int:id>', '/api/cinema/<string:name>')
api.add_resource(MovieAPI, '/api/movie', '/api/movie/<int:id>', '/api/movie/<string:name>')
api.add_resource(ShowtimeAPI, '/api/showtime', '/api/showtime/<int:id>', '/api/showtime/<string:name>')
api.add_resource(BookingAPI, '/api/booking', '/api/booking/<int:id>', '/api/booking/<string:name>')
api.add_resource(UserAPI, '/api/user', '/api/user/<int:id>', '/api/user/<string:name>')



if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',port=8080)
