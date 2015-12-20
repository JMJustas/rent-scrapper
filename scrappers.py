from pyquery import PyQuery as pq
class BaseScrapper:
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

class AruodasScrapper(BaseScrapper):
    """
        This is a scrapper implementation for aruodas.lt
    """
    def __init__ (self, config):
        self.config = config['search']
        self.url = 'http://www.aruodas.lt/butu-nuoma/vilniuje/?FRegion=461&F&FRoomNumMax=3&FPriceMax=%d&FOrder=Actuality&FImages=on' % (self.config['max-price'])


    def get_row_selector(self):
        return '.list-row'

    def get_url(self):
        return self.url

    def process_row(self, row):
        result = {}
        price = row.find('.list-item-price').text()[:-2].replace(' ', '')
        if len(price) > 0:
            price = float(price)
            #Aruodas.lt sometimes provides invalid entries(might be promoted articles or something like that..)
            if self.config['max-price'] < price:
                    return None
            result['url'] = row.find('a').attr('href')
            result['price'] = price
            return result
        return None



