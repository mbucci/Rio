from marshmallow import Schema, fields

from base import Base, Unicode


class ProductLookupSchema(Base):

	product_type = fields.Integer(required=True)
	product_id = fields.Integer(required=True)
	product_group = fields.Integer(required=True, allow_none=True)
	product_specific = fields.Integer(required=True, allow_none=True)
	name = Unicode(required=True)
