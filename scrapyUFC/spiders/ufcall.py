from ..pipelines import UfcPipeline
from w3lib.html import remove_tags
from ..items import FightItem
from typing import Optional
import datetime as dt
import scrapy
import sys

class UfcallSpider(scrapy.Spider):
    name = "ufcall"
    allowed_domains = ["www.sherdog.com"]
    start_urls = ["https://www.sherdog.com/organizations/Ultimate-Fighting-Championship-UFC-2"]

    unique_urls = set()

    def parse(self, response):
        event_table = response.css('table[class="new_table event"] tr[onclick]')
        for event in event_table:
            date = dt.datetime.fromisoformat(event.css('meta[itemprop="startDate"]::attr(content)').get()).replace(tzinfo=None)
            if date < dt.datetime.now():
                urls = event.css('a::attr(href)').getall()
                for url in urls:
                    if url not in self.unique_urls and 'Road-to-UFC' not in url:
                        self.unique_urls.add(url)
                        yield scrapy.Request(url=f"https://www.sherdog.com{url}", callback=self.parse_prev_fights, meta={'url': url})
            # potentially broken
            elif event_table.index(event) == 0:
                urls = event.css('a::attr(href)').getall()
                for url in urls:
                    if url not in self.unique_urls and 'Road-to-UFC' not in url:
                        self.unique_urls.add(url)
                        yield scrapy.Request(url=f"https://www.sherdog.com{url}", callback=self.parse_upcoming_fights, meta={'url': url})
        for page_no in range(1, 10):
            yield response.follow(f"https://www.sherdog.com/organizations/Ultimate-Fighting-Championship-UFC-2/recent-events/{page_no}", callback=self.parse)
                

    def parse_prev_fights(self, response):
        # for the main event fighters
        event_title: str = response.css('h1').css('span[itemprop="name"]::text').get()
        fight_card = response.css('div[class="fight_card"]')

        if fight_card == []:
            return
        
        info_left = fight_card.css('div[class="fighter left_side"]') 
        left_fighter_id: str = info_left.css('h3 a::attr(href)').get().split('/')[-1]
        left_status: Optional[str] = remove_tags(info_left.css('span').getall()[2])
    
        info_right = fight_card.css('div[class="fighter right_side"]')
        right_fighter_id: str = info_right.css('h3 a::attr(href)').get().split('/')[-1]
        right_status: Optional[str] = remove_tags(info_right.css('span').getall()[2])

        weight_class: str = fight_card.css('span[class="weight_class"]::text').get()

        fight_card_resume = response.css('table[class="fight_card_resume"]').css('td::text').getall()
        method: Optional[str] = fight_card_resume[1].strip()
        round_data = fight_card_resume[3].strip()
        try:
            round: Optional[int] = int(round_data) 
        except:
            round: Optional[int] = None
        time: Optional[str] = fight_card_resume[4].strip()

        # to sort the order of the card 
        fight_weight: int = 1        

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

    def parse_upcoming_fights(self, response):
        # main event fight
        event_title: str = response.css('h1').css('span[itemprop="name"]::text').get()
        fight_card = response.css('div[class="fight_card"]')

        left_fighter_id: str = fight_card.css('div[class="fighter left_side"] h3 a::attr(href)').get().split('/')[-1]
        right_fighter_id: str = fight_card.css('div[class="fighter right_side"] h3 a::attr(href)').get().split('/')[-1]
        weight_class: str = fight_card.css('span[class="weight_class"]::text').get()

        fight_weight: int = 1

        fight_item = FightItem(
            event_title=event_title,
            left_fighter_id=left_fighter_id,
            left_status=None,
            right_fighter_id=right_fighter_id,
            right_status=None,
            weight_class=weight_class,
            fight_weight=fight_weight,
            method=None,
            round=None,
            time=None,
        )
        yield UfcPipeline().process_fights(fight_item)

        # following fights
        event_title = response.css('h1 span[itemprop="name"]::text').get() 

        fight_weight: int = 2

        sub_events = response.css('table[class="new_table upcoming"] tr[itemprop="subEvent"]')
        for event in sub_events:
            left_fighter_id = event.css('div[class="fighter_list left"] a[itemprop="url"]::attr(href)').get().split('/')[-1]
            right_fighter_id = event.css('div[class="fighter_list right"] a[itemprop="url"]::attr(href)').get().split('/')[-1]
            weight_class = event.css('span[class="weight_class"]::text').get()

            fight_item = FightItem(
                event_title=event_title,
                left_fighter_id=left_fighter_id,
                left_status=None,
                right_fighter_id=right_fighter_id,
                right_status=None,
                weight_class=weight_class,
                fight_weight=fight_weight,
                method=None,
                round=None,
                time=None,
            )
            yield UfcPipeline().process_fights(fight_item)
            fight_weight += 1