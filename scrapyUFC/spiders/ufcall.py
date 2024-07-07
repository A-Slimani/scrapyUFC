from w3lib.html import remove_tags
from hashlib import sha256
from ..items import FightItem
from ..pipelines import UfcPipeline
from typing import Optional
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
                    if url not in self.unique_urls and 'Road-to-UFC' not in url:
                        self.unique_urls.add(url)
                        yield scrapy.Request(url=f"https://www.sherdog.com{url}", callback=self.parse_fights, meta={'url': url})
        for page_no in range(1, 10):
            yield response.follow(f"https://www.sherdog.com/organizations/Ultimate-Fighting-Championship-UFC-2/recent-events/{page_no}", callback=self.parse)
                

    def parse_fights(self, response):
        # for the main event fighters
        event_title: str = response.css('h1').css('span[itemprop="name"]::text').get()
        fight_card = response.css('div[class="fight_card"]')

        if fight_card == []:
            return
        
        info_left = fight_card.css('div[class="fighter left_side"]') 
        left_fighter_id: str = info_left.css('h3 a::attr(href)').get().split('/')[-1]
        left_status: str = remove_tags(info_left.css('span').getall()[2])
    
        info_right = fight_card.css('div[class="fighter right_side"]')
        right_fighter_id: str = info_right.css('h3 a::attr(href)').get().split('/')[-1]
        right_status: str = remove_tags(info_right.css('span').getall()[2])

        weight_class: str = fight_card.css('span[class="weight_class"]::text').get()

        fight_card_resume = response.css('table[class="fight_card_resume"]').css('td::text').getall()
        method: str = fight_card_resume[1].strip()
        round_data = fight_card_resume[3].strip()
        try:
            round: Optional[int] = int(round_data) 
        except:
            round: Optional[int] = None
        time: str = fight_card_resume[4].strip()

        # to sort the order of the card 
        fight_weight: int = 1        

        fight_item = FightItem(
            event_title=event_title,
            left_fighter_id =left_fighter_id,
            left_status=left_status,
            right_fighter_id =right_fighter_id,
            right_status=right_status,
            weight_class=weight_class,
            fight_weight=fight_weight,
            method=method,
            round=round,
            time=time,
        )
        yield UfcPipeline().process_fights(fight_item) 

        # for the rest of the card
        event_title = response.css('h1 span[itemprop="name"]::text').get() # unsure why I have to initialize this again

        fight_weight: int = 2

        sub_events = response.css('table[class="new_table result"] tr[itemprop="subEvent"]')
        for event in sub_events:
            left_info = event.css('div[class="fighter_list left"]')
            left_fighter_id = left_info.css('a[itemprop="url"]::attr(href)').get().split('/')[-1]
            left_status = remove_tags(left_info.css('div[class="fighter_result_data"] span').getall()[1])

            right_info = event.css('div[class="fighter_list right"]')
            right_fighter_id = right_info.css('a[itemprop="url"]::attr(href)').get().split('/')[-1]
            right_status = remove_tags(right_info.css('div[class="fighter_result_data"] span').getall()[1])

            weight_class = event.css('span[class="weight_class"]::text').get()
            method = event.css('td[class="winby"] b::text').get()
            round_data = event.css('td::text')[-2].get()
            try:
                round = int(event.css('td::text')[-2].get())
            except:
                round = None
            time = event.css('td::text')[-1].get()

            fight_item = FightItem(
                event_title=event_title,
                left_fighter_id=left_fighter_id,
                left_status=left_status,
                right_fighter_id=right_fighter_id,
                right_status=right_status,
                weight_class=weight_class,
                fight_weight=fight_weight,
                method=method,
                round=round,
                time=time,
            )
            yield UfcPipeline().process_fights(fight_item) 
            fight_weight += 1
