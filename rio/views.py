from flask import Blueprint, current_app, jsonify
from flask_swagger import swagger

from resources.trade import Trade
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
	crawl = Crawl()
	response = crawl.get()
	return jsonify(response)


@API.route('/trade/years/<year>/top', methods=['GET'])
def get_year_stats(year):
	# 1
	trade = Trade()
	response = trade.get()
	return jsonify(response)


@API.route('/trade/states/<state>/municipalities/<municipality>/product', methods=['GET'])
def get_municipality_product_stats(state, municipality):
	# 2
	pass


@API.route('/trade/states/<state>/municipalities/<municipality>/years/<year>/product', methods=['GET'])
def get_municipality_year_product_stats(state, municipality, year):
	# 3
	pass


@API.route('/trade/states/<state>/years/<year>/export', methods=['GET'])
def get_state_export_stats(state, year):
	# 4
	pass


@API.route('/trade/states/<state>/years/<year>/municipality', methods=['GET'])
def get_municipality_growth_stats(state, year):
	# 5
	pass


@API.route('/countries/<country>/products/<product>/years/<year>/municipality', methods=['GET'])
def get_import_stats(country, product, year):
	# 6
	pass
