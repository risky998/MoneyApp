from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_bootstrap import Bootstrap

app = Flask(__name__) #set app name
app.config.from_object(Config)
db = SQLAlchemy(app) #set db
migrate = Migrate(app, db) #set migrate
login = LoginManager(app) #set login
login.login_view = 'login' #set login view to login
mail = Mail(app) #sets mail using flask-mail
bootstrap = Bootstrap(app)

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config ['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config ['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost = (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr = 'noreply@' + app.config['MAIL_SERVER'],
            toaddrs = app.config['ADMINS'], subject = 'MoneyApp Failure',
            credentials = auth, secure = secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('MoneyApp Startup')


from app import routes, models, errors
