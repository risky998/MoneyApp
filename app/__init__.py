from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__) #set app name
app.config.from_object(Config)
db = SQLAlchemy(app) #set db
migrate = Migrate(app, db) #set migrate
login = LoginManager(app) #set login
login.login_view = 'login' #set login view to login

from app import routes, models, errors
