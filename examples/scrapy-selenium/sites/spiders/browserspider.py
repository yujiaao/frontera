import json
import logging
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import scrapy

from ..database.business import find_template_by_url, TemplateModel
from ..items import BusinessItem


class BrowserSpider(scrapy.Spider):
    name = 'browser'
    allowed_domains = ['www.psa-retail.com']
    start_urls = ['https://www.psa-retail.com/de/kaufen']
    temp_cache = None
    target_switcher = {"text": "/text()", "src": "/@src", "": None}

    @staticmethod
    def get_card_url(list_response):
        links = list_response.css(".card-list a::attr(href)").extract()
        links = filter(lambda href: not href.startswith('#'), links)
        return links

    @staticmethod
    def join(url, response, cb):
        if url is not None:
            url = response.urljoin(url)
            # https://github.com/clemfromspace/scrapy-selenium
            #             screenshot
            # When used, selenium will take a screenshot of the page and the binary data of the .png captured will be added to the response meta:
            #
            # yield SeleniumRequest(
            #     url=url,
            #     callback=self.parse_result,
            #     screenshot=True
            # )
            #
            # def parse_result(self, response):
            #     with open('image.png', 'wb') as image_file:
            #         image_file.write(response.meta['screenshot'])
            # script
            # When used, selenium will execute custom JavaScript code.
            # yield SeleniumRequest(
            #     url=url,
            #     callback=self.parse_result,
            #     script='window.scrollTo(0, document.body.scrollHeight);',
            # )
            return SeleniumRequest(url=url, callback=cb,
                                   wait_time=10,
                                   # wait_until=EC.element_to_be_clickable((By.ID, 'someid'))
                                   )
            # return scrapy.Request(url, callback=cb)
        return None

    def parse(self, response):
        self.log("process %s" % response.url)

        detail_links = self.get_card_url(response)
        for r in detail_links:
            yield self.join(r, response, self.parse_page2)

        next_page = response.css("a.pagination-element.next::attr(data-page)").extract_first()
        self.log("fire next page %d" % int(next_page))
        yield self.join("?page=" + next_page, response, self.parse)

        pass

    def parse_page2(self, response):
        # detail page, return items only
        print(response.request.meta['driver'].title)

        if self.temp_cache is None:
            self.temp_cache = find_template_by_url(response.url)
        if type(self.temp_cache) != TemplateModel:
            self.log(f"can't find template for %s" % response.url, level=logging.WARN)
            return
        xpath_json = self.temp_cache.xpath_json

        item = BusinessItem()
        item['url'] = response.url

        data = json.loads(xpath_json)
        count = 0
        total = 1
        for field in data['data']:
            selector = field['selector']
            name = field['name']
            target = field['target']

            target = self.target_switcher[target]
            if target is not None:
                txt = response.xpath(selector + target).extract_first()
                # TODO download picture
                # if(target.contains("src")):
                #    yield self.download(txt, response)
                item[name] = txt
                count += 1 if txt != '' else 0
                total += 1
        if count / total > 0.5:
            yield item
        else:
            self.log("item with poor quality {}".format(item), level=logging.WARN)
        pass

    def download(self, txt, response):
        pass
