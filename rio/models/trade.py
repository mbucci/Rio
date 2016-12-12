from rio.app import db
from base import Base


class Trade(Base):
	__tablename__ = 'rio_trade'

	kind = db.Column(db.String(10), index=True)
	year = db.Column(db.Integer, index=True)
	month = db.Column(db.Integer, index=True)
	desination = db.Column(db.String(120))
	state_id = db.Column(db.Integer)
	customs_unit_boarding_id = db.Column(db.Integer)
	municipality_id = db.Column(db.Integer)
	transaction_amount_wt = db.Column(db.Float)
	transaction_amount_usd = db.Column(db.Float)
	transacted_product_id = db.Column(db.Integer)
