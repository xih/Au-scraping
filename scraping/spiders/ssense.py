# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request


class SsenseSpider(Spider):
    name = 'ssense'
    allowed_domains = ['ssense.com']
    start_urls = ['https://www.ssense.com/en-us/men', 'https://www.ssense.com/en-us/women']

    custom_settings = {
        #----------------------------
        # PROXIES
        # https://free-proxy-list.net/
        #----------------------------
        'RETRY_TIMES': 10,
        'RETRY_HTTP_CODES': [500, 503, 504, 400, 403, 404, 408],

        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
            'scrapy_proxies.RandomProxy': 401,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        },

        'RANDOM_UA_PER_PROXY': True,

        'PROXY_LIST': '../proxies.txt',

        # Proxy mode
        # 0 = Every requests have different proxy
        # 1 = Take only one proxy from the list and assign it to every requests
        # 2 = Put a custom proxy to use in the settings
        'PROXY_MODE': 1,
    }


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
