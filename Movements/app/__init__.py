from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
api = Api(app,
       version='0.1',
       title='The perfect api',
       description='api Bilancio personale',
       endpoint='api')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ivana/BilancioAPI/site.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.controllers import movements

api.add_namespace(movements)