from w3lib.html import remove_tags
from ..items import FightItem
import scrapy
import datetime as dt

class UfcallSpider(scrapy.Spider):
    name = "ufcall"
    allowed_domains = ["www.sherdog.com"]
    start_urls = ["https://www.sherdog.com/organizations/Ultimate-Fighting-Championship-UFC-2"]

    unique_urls = set()

    def parse(self, response):
        event_table = response.css('table[class="new_table event"]')
        for event in event_table.css('tr[onclick]'):
            date = dt.datetime.fromisoformat(event.css('meta[itemprop="startDate"]::attr(content)').get()).replace(tzinfo=None)
            if date < dt.datetime.now():
                urls = event.css('a::attr(href)').getall()
                for url in urls:
                    if url not in self.unique_urls:
                        self.unique_urls.add(url)
                        yield scrapy.Request(url=f"https://www.sherdog.com{url}", callback=self.parse_fights, meta={'url': url})
        for page_no in range(1, 10):
            yield response.follow(f"https://www.sherdog.com/organizations/Ultimate-Fighting-Championship-UFC-2/recent-events/{page_no}", callback=self.parse)
                

    def parse_fights(self, response):
        # for the main event fighters
        event_title = response.css('h1').css('span[itemprop="name"]::text').get()

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
        round = int(fight_card_resume[3].strip())
        time = fight_card_resume[4].strip()

        left_fighter_url = info_left.css('h3 a::attr(href)').get()
        right_fighter_url = info_right.css('h3 a::attr(href)').get()

        fight_item = FightItem(
            event_title=event_title,
            left_fighter=left_fighter,
            left_status=left_status,
            right_fighter=right_fighter,
            right_status=right_status,
            weight_class=weight_class,
            method=method,
            round=round,
            time=time,
            left_fighter_url=left_fighter_url,
            right_fighter_url=right_fighter_url 
        )
        yield fight_item

        # for the rest of the card
        event_title = response.css('h1 span[itemprop="name"]::text').get() # unsure why I have to initialize this again
        sub_events = response.css('table[class="new_table result"] tr[itemprop="subEvent"]')
        for event in sub_events:
            left_info = event.css('div[class="fighter_list left"]')
            left_fighter = ' '.join(left_info.css('span[itemprop="name"]::text').getall())
            left_status = remove_tags(left_info.css('div[class="fighter_result_data"] span').getall()[1])

            right_info = event.css('div[class="fighter_list right"]')
            right_fighter = ' '.join(right_info.css('span[itemprop="name"]::text').getall())
            right_status = remove_tags(right_info.css('div[class="fighter_result_data"] span').getall()[1])

            weight_class = event.css('span[class="weight_class"]::text').get()
            method = event.css('td[class="winby"] b::text').get()
            round = event.css('td::text')[-2] 
            time = event.css('td::text')[-1]

            left_fighter_url = left_info.css('a[itemprop="url"]::attr(href)').get()
            right_fighter_url = right_info.css('a[itemprop="url"]::attr(href)').get()

            fight_item = FightItem(
                event_title=event_title,
                left_fighter=left_fighter,
                left_status=left_status,
                right_fighter=right_fighter,
                right_status=right_status,
                weight_class=weight_class,
                method=method,
                round=round,
                time=time,
                left_fighter_url=left_fighter_url,
                right_fighter_url=right_fighter_url 
            )
            yield fight_item
