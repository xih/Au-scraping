# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request


class SsenseSpider(Spider):
    name = 'ssense'
    allowed_domains = ['ssense.com']
    start_urls = ['https://www.ssense.com/en-us/men', 'https://www.ssense.com/en-us/women']

    def parse(self, response):
        print(response.body)
        # exclude the first one because that contains ''/en-us/women'
        relative_designer_urls = response.xpath('//*[@id="designer-list"]//a/@href').extract()[1:]
        print(relative_designer_urls)
        for relative_designer_url in relative_designer_urls:
            absolute_designer_url = response.urljoin(relative_designer_url)
            yield Request(absolute_designer_url, callback=self.parse_designer)

    def parse_designer(self, response):
        pass
