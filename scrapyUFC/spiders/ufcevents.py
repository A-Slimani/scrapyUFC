from ..pipelines import UfcPipeline
from ..items import EventItem
import datetime as dt
import scrapy

class UfcEventsAll(scrapy.Spider):
    name = 'ufcevents'
    allowed_domains = ['www.sherdog.com']
    start_urls = ['https://www.sherdog.com/organizations/Ultimate-Fighting-Championship-UFC-2']

    def parse(self, response):
        event_table = response.css('table[class="new_table event"] tr[onclick]')
        for event in event_table:
            title = event.css('span[itemprop="name"]::text').get()
            if 'Road to UFC' in title: # dont want no Road to UFC events
                continue
            location: str = event.css('td[itemprop="location"]::text').get()
            date_str: str = event.css('meta[itemprop="startDate"]::attr(content)').get()[:10]
            date: dt.date = dt.datetime.strptime(date_str, '%Y-%m-%d').date()
            url: str = event.css('a::attr(href)').get()
            event_item = EventItem(
                title=title,
                date=date,
                location=location,
                url=url
            )
            yield UfcPipeline().process_events(event_item)
        for page_no in range(1, 10):
            yield response.follow(f"https://www.sherdog.com/organizations/Ultimate-Fighting-Championship-UFC-2/recent-events/{page_no}", callback=self.parse)