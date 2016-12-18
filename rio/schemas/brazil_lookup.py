from marshmallow import Schema, fields

from base import Base, Unicode


class BrazilLookupSchema(Base):

	region_id = fields.Integer(required=True)
	state_id = fields.String(required=True)
	mesoregion_id = fields.Integer(required=True)
	microregion_id = fields.Integer(required=True)
	municipality_id = fields.Integer(required=True)
	name = Unicode(required=True)
