from rio.app import db
from base import Base


class ProductLookup(Base):
	__tablename__ = 'rio_product_lookup'

	product_type = db.Column(db.Integer(), primary_key=True)
	product_id = db.Column(db.Integer(), primary_key=True)
	product_group = db.Column(db.Integer())
	product_specific = db.Column(db.Integer())
	name = db.Column(db.Unicode(255, collation='utf8_unicode_ci'))

	@classmethod
	def ingest(cls, row):
		id_parts = row['id']
		return {
			"id": int(id_parts),
			"product_type": int(id_parts[0:2]),
			"product_id": int(id_parts[2:]),
			"product_group": (int(id_parts[2:4]) if len(id_parts) > 4 else None),
			"product_specific": (int(id_parts[6:]) if len(id_parts) > 6 else None),
			"name": row['name_en'].decode('utf-8')
		}