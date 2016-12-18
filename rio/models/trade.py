from rio.app import db
from base import Base


class Trade(Base):
	__tablename__ = 'rio_trade'

	kind = db.Column(db.String(32), index=True)
	year = db.Column(db.Integer, index=True)
	month = db.Column(db.Integer, index=True)
	desination = db.Column(db.Integer)
	state_id = db.Column(db.Integer)
	customs_unit_boarding_id = db.Column(db.Integer)
	municipality_id = db.Column(db.Integer)
	quantity = db.Column(db.BigInteger)
	transaction_amount_wt = db.Column(db.Float)
	transaction_amount_usd = db.Column(db.Float)
	transacted_product_id = db.Column(db.Integer)

	@classmethod
	def ingest(cls, row):
		return {
			"year": int(row['\xef\xbb\xbfYear']),
			"month": int(row['Month']),
			"desination": int(row['DestinationCoutnry_ID']),
			"state_id": int(row['State_ID']),
			"customs_unit_boarding_id": int(row['Customs_Unit_Boarding_ID']),
			"municipality_id": int(row['Municipality_ID']),
			"quantity": int(row['Quantity']),
			"transaction_amount_wt": int(row['TransactionAmount_kg']),
			"transaction_amount_usd": int(row['TransactionAmount_US$_FOB']),
			"transacted_product_id": int(row['TransactedProduct_ID_HS'])
		}
