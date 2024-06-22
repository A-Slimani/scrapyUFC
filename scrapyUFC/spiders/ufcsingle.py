from w3lib.html import remove_tags
import scrapy


class UfcsingleSpider(scrapy.Spider):
    name = "ufcsingle"
    allowed_domains = ["www.sherdog.com"]
    start_urls = ["https://www.sherdog.com/events/UFC-on-ESPN-58-Perez-vs-Taira-102196"]

    def parse(self, response):
        event = response.css('h1').css('span[itemprop="name"]::text').get()

        fight_card = response.css('div[class="fight_card"]')

        info_left = fight_card.css('div[class="fighter left_side"]') 
        left_fighter = info_left.css('h3').css('span[itemprop="name"]::text').get()
        left_status = remove_tags(info_left.css('span').getall()[2])
        
        info_right = fight_card.css('div[class="fighter right_side"]')
        right_fighter = info_right.css('h3').css('span[itemprop="name"]::text').get()
        right_status = remove_tags(info_right.css('span').getall()[2])

        weight_class = fight_card.css('span[class="weight_class"]::text').get()

        fight_card_resume = fight_card.css('div[class="fight_card_resume"]').css('td::text').getall()
        method = fight_card_resume[1]
        round = fight_card_resume[3]
        time = fight_card_resume[4]

        yield {
           "event": event,
           "left_fighter": left_fighter,
           "left_status": left_status,
           "right_fighter": right_fighter,
           "right_status": right_status,
           "weight_class": weight_class,
           "method": method,
           "round": round,
           "time": time
        }


