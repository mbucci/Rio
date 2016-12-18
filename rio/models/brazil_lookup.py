from rio.app import db
from base import Base


class BrazilLookup(Base):
	__tablename__ = 'rio_brazil_lookup'

	region_id = db.Column(db.Integer, primary_key=True)
	state_id = db.Column(db.String(2), primary_key=True)
	mesoregion_id = db.Column(db.Integer)
	microregion_id = db.Column(db.Integer)
	municipality_id = db.Column(db.Integer)
	name = db.Column(db.Unicode(255, collation='utf8_unicode_ci'))

	@classmethod
	def ingest(cls, row):
		region_id = row['id']
		return {
			"id": int(row['id_mdic']),
			"region_id": int(region_id[0]),
			"state_id": region_id[1:3],
			"mesoregion_id": int(region_id[3:5]),
			"microregion_id": int(region_id[5:7]),
			"municipality_id": int(region_id[7:9]),
			"name": row['name_en'].decode('utf-8')
		}