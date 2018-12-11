import pprint
import lxml
from bs4 import BeautifulSoup
from re import sub
from decimal import Decimal
import requests
"""
The Spider class uses beautiful soup to parse html from source: https://www.flipkart.com for phones 
along with their prices.
"""


class Spider(object):
    def __init__(self, max_pages):
        self.max_pages = max_pages
        self.page = 1
        self.crawler()

    def crawler(self):
        names = []
        prices = []
        while self.page <= self.max_pages:
            url = f'https://www.flipkart.com/search?q=phones&page={self.page}'
            source_code = requests.get(url)
            #print(source_code.content)
            soup = BeautifulSoup(source_code.content, 'lxml')
            for link in soup.find_all('div', {'class': '_3wU53n'}):
                name = link.get_text()
                names.append(name)
            for link in soup.find_all('div', {'class': '_1vC4OE _2rQ-NK'}):
                money = link.get_text()
                price = int(Decimal(sub(r'[^\d.]', '', money)))
                prices.append(price)
            self.page += 1

        pprint.pprint(dict(zip(names, prices)))


Spider(100)
