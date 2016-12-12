import json

from rio.app import db

from sqlalchemy.ext.declarative import declared_attr, as_declarative


@as_declarative()
class Base(db.Model):
	__abstract__ = True

	id = db.Column(db.BigInteger, primary_key=True)

	@classmethod
	def get(cls, id):
		return cls.query.filter_by(id=id).first()

	@classmethod
	def create(cls, **data):
		return cls(**dict(data))	
