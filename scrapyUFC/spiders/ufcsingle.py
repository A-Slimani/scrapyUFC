from w3lib.html import remove_tags
import scrapy


class UfcsingleSpider(scrapy.Spider):
    name = "ufcsingle"
    allowed_domains = ["www.sherdog.com"]
    start_urls = ["https://www.sherdog.com/events/UFC-on-ESPN-58-Perez-vs-Taira-102196"]

    def parse(self, response):
        # for the main event 
        event_title = response.css('h1 span[itemprop="name"]::text').get()

        fight_card = response.css('div[class="fight_card"]')

        info_left = fight_card.css('div[class="fighter left_side"]') 
        left_fighter = info_left.css('h3 span[itemprop="name"]::text').get()
        left_status = remove_tags(info_left.css('span').getall()[2])
    
        info_right = fight_card.css('div[class="fighter right_side"]')
        right_fighter = info_right.css('h3 span[itemprop="name"]::text').get()
        right_status = remove_tags(info_right.css('span').getall()[2])

        weight_class = fight_card.css('span[class="weight_class"]::text').get()

        fight_card_resume = response.css('table[class="fight_card_resume"] td::text').getall()
        method = fight_card_resume[1].strip()
        round = fight_card_resume[3].strip()
        time = fight_card_resume[4].strip()

        left_fighter_url = info_left.css('h3 a::attr(href)').get()
        right_fighter_url = info_right.css('h3 a::attr(href)').get()

        yield {
           "event_title": event_title,
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

            yield {
                "event_title": event_title,
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

