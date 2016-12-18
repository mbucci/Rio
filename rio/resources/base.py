from flask import request
from flask_restful import Resource, reqparse
from marshmallow import fields

from rio.app import db

import rio.utils as utils

class Base(Resource):
	_model_class = None
	_schema_class = None

	def get(self, id=None):
		query = db.session.query(self._model_class)
		if id:
			query = query.filter(self._model_class.id == id)
			return self._format_results(query.first())

		return self._format_results(query.all(), many=True)

	def _format_results(self, results, many=False, full=False):
		schema = self._schema_class(many=many)
		if not full:
			for field, field_data in schema.fields.iteritems():
				if isinstance(field_data, fields.Nested):
					schema.exclude += (field,)
		return schema.dump(results).data

	def _validate_request_body(self, body, schema=None):
		schema = schema if schema else self._schema_class
		response = schema(strict=True).load(body)
		if response.errors:
			raise Exception(response.errors)
		return response.data
