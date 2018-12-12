import pprint
import time
import lxml
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from re import sub
from decimal import Decimal
import requests
import threading

"""
The Spider class crawls flipkart.com and snapdeal.com to gather phone listings (model and price)

crawler() method uses 'requests', url formatting and bs4 soup.find method to get the data .

dynamic_crawler() deals with javascript rendered pages. It uses selenium web driver . 
An alternative could be Scrapy library or pyQT5 . .

threading causes data from both websites to be printed asynchronously . 
In a more realistic situation they will be inserted in some database.
"""


class Spider(object):
    def __init__(self, max_pages):
        self.max_pages = max_pages
        self.page = 1
        a = threading.Thread(name='craw1', target=self.crawler)
        a.start()
        b = threading.Thread(name='dycraw', target=self.dynamic_crawler)
        b.start()

    def crawler(self):
        names = []
        prices = []
        while self.page <= self.max_pages:
            url = f'https://www.flipkart.com/search?q=phones&page={self.page}'
            source_code = requests.get(url)
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

    def dynamic_crawler(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get('https://www.snapdeal.com/search?keyword=phones&sort=rlvncy')
        time.sleep(1)
        elem = driver.find_element_by_tag_name("body")
        no_of_pagedowns = 20

        while no_of_pagedowns:
            prod = driver.find_elements_by_class_name("product-title")
            pric = driver.find_elements_by_css_selector(".product-price")
            time.sleep(1.5)
            for i in zip(prod, pric):
                money = i[1].text
                price = money.lstrip('Rs.')
                print(i[0].text, " ", price)
            elem.send_keys(Keys.PAGE_DOWN)
            no_of_pagedowns -= 1


if __name__ == '__main__':
    Spider(100)
