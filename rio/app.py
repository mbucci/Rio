from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

db = SQLAlchemy()

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

LOCAL_DB = 'mysql://root:Hugediablo!6@localhost:3306/rio?charset=utf8mb4'
DEV_DB = 'mysql://mbucci:Hugediablo!6@rio-db.c8wwstsgstz6.us-east-1.rds.amazonaws.com:3306/rio_db?charset=utf8'

def create_app(environment='local'):
	application = Flask(__name__)
	application.config['JSON_AS_ASCII'] = False
	if environment == 'local':
		application.config['SQLALCHEMY_DATABASE_URI'] = LOCAL_DB
	elif environment == 'dev':
		application.config['SQLALCHEMY_DATABASE_URI'] = DEV_DB

	db.init_app(application)
	register_blueprints(application)

	return application

def register_blueprints(application):
	from rio.views import API
	application.register_blueprint(API)
