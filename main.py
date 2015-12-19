# coding=utf-8
from pyquery import PyQuery	as pq
try:
	import cPickle as pickle
except:
	import pickle

class Base_Scrapper:
	"""
		Base class defining interface for scrappers. Real implementations should overload some methods
	"""
	def scrape(self):
		d = pq(url=self.get_url())
		return [x for x in [self.process_row(row) for row in d(self.get_row_selector()).items()] if x]

	def get_row_selector(self):
		"""
			Should return jQuery-like selector to select an article row html element
		"""
		pass

	def process_row(self, row):
		"""
			Should process given row and return an entry dict object containing fields 'url' and 'price' or None if the row is not valid
		"""
		pass

class Aruodas_Scrapper(Base_Scrapper):
	"""
		This is a scrapper implementation for aruodas.lt
	"""
	def get_row_selector(self):
		return '.list-row'

	def get_url(self):
		return 'http://www.aruodas.lt/butu-nuoma/vilniuje/?FRegion=461&F&FRoomNumMax=3&FPriceMax=500&FOrder=Actuality'

	def process_row(self, row):
		result = {}
		price = row.find('.list-item-price').text()[:-2].replace(' ', '')
		if len(price) > 0:
			result['url'] = row.find('a').attr('href')
			result['price'] = int(price)
			return result
		return None

SCRAPPERS = [
			Aruodas_Scrapper()
		]

if __name__ == '__main__':
	data = {}
	# Load previously stored data - we want to remember which articles we've already seen
	try:
		with open('data.obj', 'rb') as handle:
			data = pickle.load(handle)
	except:
		pass

	# let's see if we have something new to see
	new_records = []
	for scrapper in SCRAPPERS:
		new_records += [entry for entry in  scrapper.scrape() if entry['url'] not in data]

	# store records for future reference
	for entry in new_records:
		data[entry['url']] = entry
	with open('data.obj', 'wb') as handle:
		pickle.dump(data, handle)
