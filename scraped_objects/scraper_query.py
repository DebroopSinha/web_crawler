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
from models.Scraper_model import snap_phones, flip_phones

"""
Initiate mongod server instance .

Mongoengine wraps pymongo functionalities . Scraper module is an object model which gives some 
structure to otherwise schema-less documents.

chromedriver executable has to be in system path.

database.py inside a db folder is imported in Scraper module . It connects to the mongod instance. 
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
            for link in soup.find_all('div', {'class': '_3wU53n'}):          #statically find html class
                name = link.get_text()
                names.append(name)
            for link in soup.find_all('div', {'class': '_1vC4OE _2rQ-NK'}):
                money = link.get_text()
                price = int(sub(r'[^\d.]', '', money))
                prices.append(price)
            self.page += 1

        for i in zip(names, prices):
            flip_phones(name=i[0], price=i[1]).save()                        #save to mongodb using mongoengine ODM
        queryset = flip_phones.objects(price__gte=10000).distinct(field='name')         #sample query
        for i in queryset:
            print(i)

    def dynamic_crawler(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get('https://www.snapdeal.com/search?keyword=phones&sort=rlvncy')  #chrome driver simulates a real user
        time.sleep(1)
        elem = driver.find_element_by_tag_name("body")
        no_of_pagedowns = 20
        while no_of_pagedowns:
            prod = driver.find_elements_by_class_name("product-title")       #dynamically find html class
            pric = driver.find_elements_by_css_selector(".product-price")
            time.sleep(0.2)
            for i in zip(prod, pric):
                money = i[1].text
                price = money.lstrip('Rs. ')
                price = int(price.replace(",",""))
                snap_phones(name=i[0].text,price=price).save()               #save to mongodb using mongoengine ODM
            elem.send_keys(Keys.PAGE_DOWN)
            no_of_pagedowns -= 1

        queryset=snap_phones.objects(price__gte=10000).distinct(field='name')          #sample query
        for i in queryset:
            print(i)

if __name__ == '__main__':
    Spider(100)                                                               #max_pages you want to crawl

