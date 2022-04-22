import scrapy
from scrapy_splash import SplashRequest


class MisiooSpider(scrapy.Spider):
    """"""

    name = 'misioo_spider'
    allowed_domains = ['misioohandmade.pl']
    start_urls = ['https://misioohandmade.pl/sklep/']

    def start_requests(self):
        """"""

        products_script = """
        function main(splash)

        """
