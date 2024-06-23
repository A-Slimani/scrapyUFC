import scrapy


class UfcfightersSpider(scrapy.Spider):
    name = "ufcfighters"
    allowed_domains = ["www.sherdog.com"]
    start_urls = ["https://www.sherdog.com/fighter"]

    def parse(self, response):
        # fighter details
        pass
