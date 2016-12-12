from marshmallow import Schema, fields

class Base(Schema):
	id = fields.Integer(dump_only=True)

