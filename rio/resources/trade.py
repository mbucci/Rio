from datetime import datetime

from rio.app import db
from base import Base 
from rio.models.trade import Trade
from rio.schemas.trade import Trade_Schema

import rio.utils as utils


FOLDERS = [
	{'name': 'export', 'id':'0B0fngGlnqNt7VWVTLUJ2TVVHSDQ'},
	{'name': 'import', 'id':'0B0fngGlnqNt7Wl96ZW5sUWJ3Z1k'},
	{'name': 'attributes', 'id':'0B0fngGlnqNt7TERTZExCQzlLSW8'}
]


class Trade(Base):
	_model_class = Trade
	_schema_class = Trade_Schema

	def get(self, id=None, *args, **kwargs):
		# full = utils.parse_bool(kwargs['full'])
		# query = db.session.query(PR_Contest) 
		# if id:
		# 	query = query.filter(PR_Contest.id == id)
		# if kwargs['brand']:
		# 	query = query.filter(PR_Contest.brand == kwargs['brand'])
		# if kwargs['date_created']:
		# 	start = kwargs['date_created']
		# 	now = datetime.utcnow()
		# 	query = query.filter(PR_Contest.date_created.between(start, now))
		# return self._format_results(query.all(), many=True, full=full)
		return {}
