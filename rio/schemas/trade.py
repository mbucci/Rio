from marshmallow import Schema, fields

from base import Base


class Trade_Schema(Base):
	kind = fields.String(required=True)
	year = fields.Integer(required=True)
	month = fields.Integer(required=True)
	desination = fields.String(required=True)
	state_id = fields.Integer(required=True)
	customs_unit_boarding_id = fields.Integer(required=True)
	municipality_id = fields.Integer(required=True)
	transaction_amount_wt = fields.Float(required=True)
	transaction_amount_usd = fields.Float(required=True)
	transacted_product_id = fields.Integer(required=True)
