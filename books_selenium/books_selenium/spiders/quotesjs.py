import scrapy
from scrapy_splash import SplashRequest


class QuotesjsSpider(scrapy.Spider):
    name = 'quotesjs'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/js']

    def start_requests(self):
        """"""

        for url in self.start_urls:
            yield SplashRequest(
                url=url,
                callback=self.parse,
                endpoint='render.html',
                )


    def parse(self, response):
        """"""

        quotes = response.xpath('//div[@class="quote"]')
        for quote in quotes:
            text = quote.xpath('./span[@class="text"]/text()').get()
            author = quote.xpath('.//*[@class="author"]/text()').get()
            tags = quote.xpath('./div[@class="tags"]//a/text()').extract()

            yield {
                'Quote': text,
                'Author': author,
                'Tags': tags,
            }

        script = """
        function main(splash)
            assert(splash:go(splash.args.url))
            splash:wait(0.3)
            button = splash:select("li[class=next] a")
            splash:set_viewport_full()
            splash:wait(0.1)
            button:mouse_click()
            splash:wait(1)
            return {
                url = splash:url(),
                html = splash:html()
                }
        end
        """
        yield SplashRequest(
            url=response.url,
            callback=self.parse,
            endpoint='execute',
            args={'lua_source': script},
            )
