import csv
import rarfile

from rio.app import db, drive
from base import Base 
from rio.models import Trade, BrazilLookup, ProductLookup, WorldLookup
from rio.schemas import TradeSchema, BrazilLookupSchema, ProductLookupSchema, WorldLookupSchema

import rio.utils as utils

rarfile.UNRAR_TOOL = 'unrar'


class Crawl(Base):
	_model_class = Trade
	_schema_class = TradeSchema

	def __init__(self):
		self.folders = [
			{'name': 'export', 'id':'0B0fngGlnqNt7VWVTLUJ2TVVHSDQ'},
			{'name': 'import', 'id':'0B0fngGlnqNt7Wl96ZW5sUWJ3Z1k'},
			{'name': 'attributes', 'id':'0B0fngGlnqNt7TERTZExCQzlLSW8'}
		]

	def get(self, kind=None, year=None, download=False, ingest=False, *args, **kwargs):
		files = {}
		for folder in self.folders:
			if kind and folder['name'] == kind:
				files.update(self._scrape_drive('drive', folder, year, download))

		if ingest:
			self._ingest(files)

		return {"files": files}

	def _ingest(self, files):
		for key, file_list in files.iteritems():
			for ingest_file in file_list:
				count = 0
				records = []
				if key in ['import', 'export']:
					rf = rarfile.RarFile(ingest_file)
					f = next(iter(rf.namelist() or []), None)
					with rf.open(f) as csvfile:
						reader = csv.DictReader(csvfile, delimiter='|')
						for r in reader:
							if count % 10000 == 0:
								print(ingest_file, count)

							body = Trade.ingest(r)
							body['kind'] = key
							records.append(self._validate_request_body(body, schema=TradeSchema))
							count += 1

					n = 0
					while n < len(records):
						n1 = n + 10000
						db.session.bulk_insert_mappings(Trade, records[n:n1])
						print("%s/%s inserted" % (n1, len(records)))
						n = n1
					db.session.commit()

				else:
					with open(ingest_file) as csvfile:
						model, schema = None, None
						if 'attrs_bra' in csvfile.name:
							model = BrazilLookup
							schema = BrazilLookupSchema
						elif 'attrs_hs' in csvfile.name:
							model = ProductLookup
							schema = ProductLookupSchema
						elif 'attrs_wld' in csvfile.name:
							model = WorldLookup
							schema = WorldLookupSchema

						reader = csv.DictReader(csvfile, delimiter=',')
						for r in reader:
							if count % 100 == 0:
								print(ingest_file, count)

							try:
								body = model.ingest(r)
								records.append(self._validate_request_body(body, schema=schema))
								count += 1
							except ValueError as v:
								continue

					db.session.bulk_insert_mappings(model, records)
					db.session.commit()

	@staticmethod
	def _scrape_drive(spaces, folder, year, download):
		folder_name = folder['name']
		directory = utils.mkdir(folder_name)
		files = {folder_name: []}
		year_search = ('MDIC_%s' % str(year)) if year else ''

		search = {
			"q": "'%s' in parents and fullText contains '%s'" % (str(folder['id']), year_search),
			"spaces": spaces
		}
		try:
			for f in drive.ListFile(search).GetList():
				file_name = directory + '/' + f['title']
				files[folder_name].append(file_name)
				if download:
					utils.download_file(f, file_name)

		except Exception as e:
			print(e.message)

		return files
