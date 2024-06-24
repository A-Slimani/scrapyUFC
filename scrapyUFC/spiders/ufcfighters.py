from ..items import FighterInfoItem 
import scrapy
import csv

class UfcfightersSpider(scrapy.Spider):
    name = "ufcfighters"
    allowed_domains = ["www.sherdog.com"]
    
    def start_requests(self):
        with open('all_fighters_unique_url.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader) # skip the header
            for row in reader:
                url = row[0]
                yield scrapy.Request(url=f'https://www.sherdog.com{url}', callback=self.parse_fighters, meta={'url': url})
    

    def parse_fighters(self, response):
        name = response.css('h1[itemprop="name"] span[class="fn"]::text').get()

        nationality = response.css('strong[itemprop="nationality"]::text').get()
        locality = response.css('span[class="locality"]::text').get()

        fighter_data = response.css('div[class="fighter-data"]')
        age = int(fighter_data.css('div[class="bio-holder"] td b::text').get())
        weight_class = fighter_data.css('div[class="association-class"] a::text').get()

        wins = int(fighter_data.css('div[class="winloses win"] span::text').getall()[1])
        wins_by = fighter_data.css('div[class="wins"] div[class="pl"]::text').getall()
        wins_by_ko_tko = int(wins_by[0])
        wins_by_sub = int(wins_by[1])
        wins_by_dec = int(wins_by[2])

        losses = int(fighter_data.css('div[class="winloses lose"] span::text').getall()[1])
        losses_by = fighter_data.css('div[class="loses"] div[class="pl"]::text').getall()
        losses_by_ko_tko = int(losses_by[0])
        losses_by_sub = int(losses_by[1])
        losses_by_dec = int(losses_by[2])

        fighter_info_item = FighterInfoItem( 
            name=name,
            nationality=nationality,
            locality=locality,
            age=age,
            weight_class=weight_class,
            wins=wins,
            wins_by_ko_tko=wins_by_ko_tko,
            wins_by_sub=wins_by_sub,
            wins_by_dec=wins_by_dec,
            losses=losses,
            losses_by_ko_tko=losses_by_ko_tko,
            losses_by_sub=losses_by_sub,
            losses_by_dec=losses_by_dec
        )
        yield fighter_info_item
