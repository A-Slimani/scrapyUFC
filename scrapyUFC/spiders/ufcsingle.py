from w3lib.html import remove_tags
import scrapy


class UfcsingleSpider(scrapy.Spider):
    name = "ufcsingle"
    allowed_domains = ["www.sherdog.com"]
    start_urls = ["https://www.sherdog.com/events/UFC-on-ESPN-58-Perez-vs-Taira-102196"]

    def parse(self, response):
        # for the main event fighters
        event = response.css('h1 span[itemprop="name"]::text').get()

        fight_card = response.css('div[class="fight_card"]')

        info_left = fight_card.css('div[class="fighter left_side"]') 
        left_fighter = info_left.css('h3 span[itemprop="name"]::text').get()
        left_status = remove_tags(info_left.css('span').getall()[2])
        left_status = None
    
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


