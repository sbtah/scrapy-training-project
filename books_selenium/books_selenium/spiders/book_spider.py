from time import sleep
from scrapy.http import Request
from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from selenium.common.exceptions import NoSuchElementException


class BooksSpider(Spider):
    """"""

    name = 'books'
    allowed_domains = ['books.toscrape.com']

    def start_requests(self):
        """"""

        self.driver = webdriver.Chrome('/home/drone10565/2-Python/SC-3/chromedriver')
        self.driver.get('http://books.toscrape.com')
        selector = Selector(text=self.driver.page_source)
        books = selector.xpath('//article[@class="product_pod"]//h3//a/@href').extract()

        for book in books:

            url = 'http://books.toscrape.com/' + book
            yield Request(url, callback=self.parse_book)

        while True:
            try:
                next_page = self.driver.find_element_by_xpath('//a[text()="next"]')
                sleep(3)
                self.logger.info('Sleeping for 3 seconds!')
                next_page.click()
                selector = Selector(text=self.driver.page_source)
                books = selector.xpath('//article[@class="product_pod"]//h3//a/@href').extract()

                for book in books:
                    url = 'http://books.toscrape.com/catalogue/' + book
                    yield Request(url, callback=self.parse_book)

            except NoSuchElementException as e:
                self.logger.info('No more pages to load.')
                self.driver.quit()
                break


    def parse_book(self, response):
        pass
