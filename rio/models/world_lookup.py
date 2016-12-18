from rio.app import db
from base import Base


class WorldLookup(Base):
	__tablename__ = 'rio_world_lookup'

	name = db.Column(db.Unicode(255, collation='utf8_unicode_ci'), primary_key=True)

	@classmethod
	def ingest(cls, row):
		return {
			"id": int(row['id_mdic']),
			"name": row['name_en'].decode('utf-8')
		}
