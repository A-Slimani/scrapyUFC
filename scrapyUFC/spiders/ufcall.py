import scrapy
import datetime as dt
from w3lib.html import remove_tags

class UfcallSpider(scrapy.Spider):
    name = "ufcall"
    allowed_domains = ["www.sherdog.com"]
    start_urls = ["https://www.sherdog.com/organizations/Ultimate-Fighting-Championship-UFC-2"]

    unique_urls = set()

    def parse(self, response):
        event_table = response.css('table[class="new_table event"]')
        for event in event_table.css('tr[onclick]'):
            date: dt = dt.datetime.fromisoformat(event.css('meta[itemprop="startDate"]::attr(content)').get()).replace(tzinfo=None)
            if date < dt.datetime.now():
                urls = event.css('a::attr(href)').getall()
                for url in urls:
                    if url not in self.unique_urls:
                        self.unique_urls.add(url)
                        yield scrapy.Request(url=f"https://www.sherdog.com{url}", callback=self.parse_fights)
        for page_no in range(1, 9):
            yield response.follow(f"https://www.sherdog.com/organizations/Ultimate-Fighting-Championship-UFC-2/recent-events/{page_no}", callback=self.parse)
                

    def parse_fights(self, response):
        # for the main event fighters
        event = response.css('h1').css('span[itemprop="name"]::text').get()

        fight_card = response.css('div[class="fight_card"]')

        info_left = fight_card.css('div[class="fighter left_side"]') 
        left_fighter = info_left.css('h3 span[itemprop="name"]::text').get()
        left_status = remove_tags(info_left.css('span').getall()[2])
    
        info_right = fight_card.css('div[class="fighter right_side"]')
        right_fighter = info_right.css('h3 span[itemprop="name"]::text').get()
        right_status = remove_tags(info_right.css('span').getall()[2])

        weight_class = fight_card.css('span[class="weight_class"]::text').get()

        fight_card_resume = response.css('table[class="fight_card_resume"]').css('td::text').getall()
        method = fight_card_resume[1].strip()
        round = fight_card_resume[3].strip()
        time = fight_card_resume[4].strip()

        left_fighter_url = info_left.css('h3 a::attr(href)').get()
        right_fighter_url = info_right.css('h3 a::attr(href)').get()

        yield {
           "event": event,
           "left_fighter": left_fighter,
           "left_status": left_status,
           "right_fighter": right_fighter,
           "right_status": right_status,
           "weight_class": weight_class,
           "method": method,
           "round": round,
           "time": time,
           "left_fighter_url": left_fighter_url,
           "right_fighter_url": right_fighter_url
        }

        # for the rest of the card


