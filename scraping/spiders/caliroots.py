# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request

#TODO: getting error 429 too many requests

class CalirootsSpider(Spider):
    name = 'caliroots'
    allowed_domains = ['caliroots.com']
    start_urls = ['https://caliroots.com/brands']

    # TODO: this isn't working
    def start_requests(self):
        return [Request(url="https://caliroots.com/brands", cookies={'currency': 'USD', 'country': 'US'})]

    def parse(self, response):
        relative_brand_urls = response.xpath('//*[@class="brand-list row"]//a/@href').extract()
        for relative_brand_url in relative_brand_urls:
            absolute_designer_url = response.urljoin(relative_brand_url)
            yield Request(absolute_designer_url, callback=self.parse_brand)

    def parse_brand(self, response):
        relative_product_urls = response.xpath('//*[@class="product-list row"]//a/@href').extract()
        for relative_product_url in relative_product_urls:
            absolute_product_url = response.urljoin(relative_product_url)
            yield Request(absolute_product_url, callback=self.parse_product)

        #TODO: work on pagination
        # nextPage = response.xpath('//*[@class="controls"]')
        # if nextPage:


    def parse_product(self, response):
        brand = response.xpath('//*[@class="form c-4 last"]/header//img/@title').extract_first('')
        product_name = response.xpath('//*[@class="form c-4 last"]/header//h1/text()').extract_first('').strip()

        #price will look like '94,90 EUR'
        price_uncleaned = response.xpath('//*[@class="form c-4 last"]/header/p/del/text()').extract_first('')

        yield {
            'brand': brand,
            'product name': product_name,
            'price_uncleaned': price_uncleaned,
        }
