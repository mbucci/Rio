from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import settings


db = SQLAlchemy()
gauth = GoogleAuth()
drive = GoogleDrive(gauth)

def create_app(environment='lcl'):
	application = Flask(__name__)
	
	if environment == 'lcl':
		config = settings.Local()
	elif environment == 'dev':
		config = settings.Development()

	application.config.from_object(config)
	print("Imported %s settings!" % environment)

	db.init_app(application)
	register_blueprints(application)
	return application

def register_blueprints(application):
	from rio.views import API
	application.register_blueprint(API)
