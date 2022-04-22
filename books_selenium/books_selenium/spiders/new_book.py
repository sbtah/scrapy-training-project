from scrapy import Spider
from scrapy.http import Request


# Changes string values for rating to numerical.
def change_rating(val):

    if val == 'One':
        return 1
    elif val == 'Two':
        return 2
    elif val == 'Three':
        return 3
    elif val == 'Four':
        return 4
    elif val == 'Five':
        return 5


# Minimazies repeating of same xpath while extracting product data.
def product_info(response, val):
    return response.xpath(f'//th[text()="{val}"]/following-sibling::td/text()').get()


class NewBooksSpider(Spider):
    """"""

    name = 'new_books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']

    def parse(self, response):
        """"""

        # Get all links for all books
        books = response.xpath('//h3/a/@href').extract()

        # Loops over the links and joins them with root url
        for book in books:
            absolute_url = response.urljoin(book)

            # Yield a request for a book link and calls parse book method!.
            yield Request(
                absolute_url,
                callback=self.parse_book,
                )

        # process next page!
        next_page_url = response.xpath('//li[@class="next"]/a/@href').get()
        absolute_next_page_url = response.urljoin(next_page_url)

        # Yield request to next page and calls parse method.
        yield Request(
            absolute_next_page_url,
            callback=self.parse,
        )


    def parse_book(self, response):
        """"""

        title = response.xpath('//h1/text()').get()
        price = response.xpath('//article[@class="product_page"]/div[@class="row"]/div[2]/p[@class="price_color"]/text()').get()[1:]
        img_url = response.xpath('//div[@id="product_gallery"]/div[1]/div[1]/div[1]/img/@src').get()
        absolute_img_url = response.urljoin(img_url)
        raw_rating = response.xpath('//article[@class="product_page"]/div[1]/div[2]/p[3]/@class').get()
        rating = raw_rating.replace('star-rating ', '')
        description = response.xpath('//article[@class="product_page"]/p/text()').get()

        # Product information datapoints!
        upc = product_info(response, 'UPC')
        product_type = product_info(response, 'Product Type')
        price_net = product_info(response, 'Price (excl. tax)')
        price_gross = product_info(response, 'Price (incl. tax)')
        tax = product_info(response, 'Tax')
        availability =  product_info(response, 'Availability')
        reviews_no = product_info(response, 'Number of reviews')


        yield {
            'Title': title,
            'Price': price,
            'Image-URL': absolute_img_url,
            'Rating': change_rating(rating),
            'Description': description,
            'Product Info': {
                'UPC': upc,
                'Product Type': product_type,
                'Price Net': price_net,
                'Price Gross': price_gross,
                'Tax': tax,
                'Availability': availability,
                'Number of reviews': reviews_no,
            },
        }
