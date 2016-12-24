from flask import Blueprint, request, current_app, jsonify
from flask_swagger import swagger

from resources.trade_stats import TradeStats
from resources.crawl import Crawl

import utils

API = Blueprint('betamax', __name__, url_prefix='/api')


@API.route('/', methods=['GET'])
def home():
	swag = swagger(current_app, prefix='/api')
	swag['info']['version'] = '0.1'
	swag['info']['title'] = 'Rio API'
	return jsonify(swag)


@API.route('/crawl', methods=['GET'])
def crawl():
	kind = request.args.get('kind') or None
	year = request.args.get('year') or None
	ingest = request.args.get('ingest', '').lower() == 'true'
	download = request.args.get('download', '').lower() == 'true'

	crawl = Crawl()
	response = crawl.get(kind=kind, year=year, ingest=ingest, download=download)
	return jsonify(response)


@API.route('/trade/years/<year>/top', methods=['GET'])
def get_year_stats(year):
	"""
	#1

	http://rio-dev.us-east-1.elasticbeanstalk.com/api/trade/years/2013/top
	"""
	stats = TradeStats()
	response = stats.get_top_export_by_year(year)
	return jsonify(response)


@API.route('/trade/states/<state>/years/<year>/product', methods=['GET'])
def get_municipality_product_stats(state, year):
	"""
	#2

	http://rio-dev.us-east-1.elasticbeanstalk.com/api/trade/states/36/years/2013/product
	"""
	stats = TradeStats()
	response = stats.get_top_product_by_municipality(state, year)
	return jsonify(response)


@API.route('/trade/municipalities/<municipality>/years/<year>/product', methods=['GET'])
def get_municipality_year_product_stats(municipality, year):
	"""
	#3

	http://rio-dev.us-east-1.elasticbeanstalk.com/api/trade/municipalities/3448708/years/2011/product
	"""
	stats = TradeStats()
	response = stats.get_imports_by_municipality(municipality, year)
	return jsonify(response)


@API.route('/trade/states/<state>/years/<year>/export', methods=['GET'])
def get_state_export_stats(state, year):
	"""
	#4

	http://rio-dev.us-east-1.elasticbeanstalk.com/api/trade/states/13/years/2012/export
	"""
	stats = TradeStats()
	response = stats.get_exports_by_state(state, year)
	return jsonify(response)


@API.route('/trade/states/<state>/years/<year>/municipality', methods=['GET'])
def get_municipality_growth_stats(state, year):
	"""
	#5
	
	http://rio-dev.us-east-1.elasticbeanstalk.com/api/trade/states/33/years/2014/municipality
	"""
	stats = TradeStats()
	response = stats.get_municipalites_by_growth(state, year)
	return jsonify(response)


@API.route('/trade/countries/<country>/products/<product>/years/<year>/municipality', methods=['GET'])
def get_import_stats(country, product, year):
	"""
	#6

	http://rio-dev.us-east-1.elasticbeanstalk.com/api/trade/countries/160/products/2516/years/2011/municipality
	"""
	stats = TradeStats()
	response = stats.get_municipalities_by_import(country, product, year)
	return jsonify(response)
