import os

from rio.app import db, drive
from base import Base 

import rio.utils as utils


class Crawl(Base):
	def __init__(self):
		self.folders = [
			{'name': 'export', 'id':'0B0fngGlnqNt7VWVTLUJ2TVVHSDQ'},
			{'name': 'import', 'id':'0B0fngGlnqNt7Wl96ZW5sUWJ3Z1k'},
			{'name': 'attributes', 'id':'0B0fngGlnqNt7TERTZExCQzlLSW8'}
		]

	def get(self, id=None, *args, **kwargs):
		files = []
		for folder in self.folders:
			files.append(self._scrape_drive('drive', folder, download=True))

		return {"files": files}

	def _scrape_drive(self, spaces, folder, download=True):
		directory = utils.mkdir(folder['name'])
		files = []
		search = {
			"q": "'%s' in parents" % str(folder['id']),
			"spaces": spaces
		}
		for f in drive.ListFile(search).GetList():
			files.append('kind: %s, title: %s' % (folder['name'], f['title']))
			if download:
				file_name = directory + '/' + f['title']
				self._download_file(f, file_name)

		return files

	def _download_file(self, f, file_name):
		if os.path.exists(file_name):
			return

		f.GetContentFile(file_name)
		print('Downloaded: %s' % file_name)
