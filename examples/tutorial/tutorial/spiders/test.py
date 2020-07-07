import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['bixuebihui.com']
    start_urls = ['https://bixuebihui.com/']

    def parse(self, response):
        pass
