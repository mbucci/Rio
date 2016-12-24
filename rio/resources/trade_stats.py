from datetime import datetime
from sqlalchemy import func, distinct, select, desc, and_, or_

from rio.app import db
from base import Base 
from rio.models import Trade, BrazilLookup, ProductLookup, WorldLookup
from rio.schemas import TradeSchema

import rio.utils as utils


class TradeStats(Base):
	_model_class = Trade

	def get_top_export_by_year(self, year):
		t = self._model_class
		b = BrazilLookup
		exports_q = select([t.municipality_id.label('id'), func.sum(t.transaction_amount_usd).label('export_value')]) \
					.where(and_(t.kind == 'export',
							    t.year == year)) \
					.group_by(t.municipality_id) \
					.alias()

		query = db.session.query(exports_q, b.name) \
					.join(b, b.id == exports_q.c.id) \
					.order_by(exports_q.c.export_value.desc()) \
					.limit(5)

		return {'results': [{'city_id': q[0], 'export_value': q[1], 'city_name': q[2].encode('utf-8')} for q in query.all()]}

	def get_top_product_by_municipality(self, state, year):
		t = self._model_class
		b = BrazilLookup
		p = ProductLookup

		exports_q = select([t.municipality_id.label('id'), t.transacted_product_id.label('product'), func.sum(t.transaction_amount_usd).label('value')]) \
					.where(and_(t.kind == 'export',
								t.state_id == state, 
							    t.year == year)) \
					.group_by(t.municipality_id, t.transacted_product_id) \
					.alias()

		query = db.session.query(exports_q, b.name, p.name) \
					.join(b, b.id == exports_q.c.id) \
					.join(p, p.product_id == exports_q.c.product)

		municipality = {}
		for r in query.all():
			mun_id = r[0]
			municipality[mun_id] = municipality[mun_id] if municipality.get(mun_id) else {'municipality_name': r[3], 'export_value': 0}
			product_id, product_value, product_name = r[1], int(r[2]), r[4]
			if product_value > municipality[mun_id]['export_value']:
				municipality[mun_id]['export_value'] = product_value
				municipality[mun_id]['product_id'] = product_id
				municipality[mun_id]['product_name'] = product_name

		for k, v in municipality.iteritems():
			v.update({'municipality_id': k})

		return {'result': sorted(municipality.values(), key=lambda x: x['export_value'], reverse=True)}

	def get_imports_by_municipality(self, municipality, year):
		t = self._model_class
		p = ProductLookup

		imports_q = select([t.transacted_product_id.label('id'), func.sum(t.transaction_amount_usd).label('value')]) \
					.where(and_(t.kind == 'import',
								t.municipality_id == municipality, 
								t.year == year)) \
					.group_by(t.transacted_product_id) \
					.alias()

		query = db.session.query(imports_q, p.name) \
					.join(p, p.product_id == imports_q.c.id) \
					.order_by(imports_q.c.value.desc())

		return {'results': [{'product_id': q[0], 'import_value': q[1], 'product_name': q[2]} for q in query.all()]}

	def get_exports_by_state(self, state, year):
		t = self._model_class
		w = WorldLookup

		exports_q = select([t.desination.label('destination'), func.sum(t.transaction_amount_usd).label('value')]) \
					.where(and_(t.kind == 'export',
								t.state_id == state,
								t.year == year)) \
					.group_by(t.desination) \
					.alias()

		query = db.session.query(exports_q, w.name) \
					.join(w, w.id == exports_q.c.destination) \
					.order_by(exports_q.c.value.desc())

		return {'results': [{'country_id': q[0], 'export_value': q[1], 'country_name': q[2]} for q in query.all()]}

	def get_municipalites_by_growth(self, state, year):
		t = self._model_class
		b = BrazilLookup

		past_year = int(year) - 1
		growth_q = select([t.year, t.municipality_id.label('id'), func.sum(t.transaction_amount_usd).label('value')]) \
					.where(and_(t.kind == 'export',
								t.state_id == state,
								or_(t.year == year,
									t.year == past_year))) \
					.group_by(t.year, t.municipality_id) \
					.alias()

		query = db.session.query(growth_q, b.name) \
					.join(b, b.id == growth_q.c.id) 

		growth = {}
		for r in query.all():
			record = {'name': r[3], 'past': 0, 'current': 0}
			growth[r[1]] = record

			if r[0] == int(year):
				record['current'] = r[2]
			else:
				record['past'] = r[2]

		for k, v in growth.iteritems():
			v['delta'] = int(v['current']) - int(v['past'])

		growth = sorted(growth.iteritems(), key=lambda (k, v): v['delta'], reverse=True)

		return {'results': [{'municipality_id': x[0], 'municipality_name': x[1]['name'], 'growth': x[1]['delta']} for x in growth[:10]]}

	def get_municipalities_by_import(self, country, product, year):
		t = self._model_class
		b = BrazilLookup

		imports_q = select([t.municipality_id.label('id')]) \
					.where(and_(t.kind == 'import',
								t.desination == country,
								t.transacted_product_id == product,
								t.year == year)) \
					.group_by(t.municipality_id) \
					.alias()

		query = db.session.query(imports_q, b.name) \
					.join(b, b.id == imports_q.c.id) \
					.order_by(b.name.desc())

		return {'results': [{'municipality_id': q[0], 'muncipality_name': q[1]} for q in query.all()]}



