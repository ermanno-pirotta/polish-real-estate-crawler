# -*- coding: utf-8 -*-
import scrapy
import re
import locale
import json
from polish_real_estate_crawler.spiders.realEstateCrawler import RealEstateCrawler

class AirbnbSpider(RealEstateCrawler):
    name = 'airbnb'
    allowed_domains = ['www.airbnb.com', 'www.airbnb.pl' ]

    locale.setlocale(locale.LC_ALL, 'pl_PL')

    def start_requests(self):
        url = 'http://www.airbnb.pl/s/'
        self.city = getattr(self, 'city', None)
        self.zone = getattr(self, 'zone', None)
        self.poi = self.get_poi_coordinates()

        url = url + self.zone + '--'+self.city + '--Polska'

        yield scrapy.Request(url, self.parse)


    def parse(self, response):
        #get all url from main page: response.xpath('//article/@data-url').extract()
        properties_links = response.xpath('//meta[@itemprop="url"]/@content').extract()
        next_page_link = response.xpath('//ul[@data-id="SearchResultsPagination"]/li/a/@href').extract()[-1]

        for property_link in properties_links:
            yield scrapy.Request('https://' + property_link, self.parse_property_details)

        if next_page_link is not None:
            yield response.follow(next_page_link, callback=self.parse)

    def parse_property_details(self, response):
        bootstrap_data = self.extract_from_html_comment(response.xpath('//*[contains(text(), "bootstrapData")]//text()').extract_first())
        bootstrap_data_json = json.loads(bootstrap_data)
        item = {}
        item['zone'] = self.zone
        item['link'] = response.xpath('//link[@rel="canonical"]/@href').extract_first(),
        item['description'] = "".join(response.xpath('//div[@id="details"]//span//text()').extract())
        item['size'] = self.extract_size_from_text(item['description'])
        item['room_nr'] = self.get_room_nr(response)
        item['latitude'] = bootstrap_data_json['bootstrapData']['reduxData']['marketplacePdp']['listingInfo']['listing']['lat']
        item['longitude'] = bootstrap_data_json['bootstrapData']['reduxData']['marketplacePdp']['listingInfo']['listing']['lng']
        item['distance'] = self.get_distance(self.poi ,[item['latitude'], item['longitude']])

        api_url = 'https://www.airbnb.pl/api/v2/pdp_listing_booking_details?force_boost_unc_priority_message_type=&guests=1&currency=PLN&locale=pl&number_of_adults=1&number_of_children=0&number_of_infants=0&show_smart_promotion=0&_format=for_web_dateless&_interaction_type=pageload&_intents=p3_book_it&'
        link = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        listing_id = self.extract_number(link)
        key = json.loads(response.xpath('//*[@id="_bootstrap-layout-init"]/@content').extract_first())['api_config']['key']
        api_url = api_url + '&listing_id=' + listing_id + '&key='+key
        request = scrapy.Request(api_url, callback=self.parse_api_details, meta={'item': item})
        yield request


    def parse_api_details(self,response):
        item = response.meta['item']
        api_json_response = json.loads(response.body_as_unicode())
        item['price'] = api_json_response['pdp_listing_booking_details'][0]['rate']['amount']

        return item

    def get_room_nr(self, response):
        room_nr_from_summary = self.get_room_nr_from_summary(response)
        room_nr_from_bedroom_configuration = len(response.css(".bedroom-config-icon-container").extract())

        if room_nr_from_summary:
            return room_nr_from_summary
        elif room_nr_from_bedroom_configuration:
            return room_nr_from_bedroom_configuration
        else:
            return 1

    def get_room_nr_from_summary(self, response):
        room_nr_from_text = 0
        text_with_room_keyword_list = response.xpath('//*[contains(text(), "sypialn")]//text()').extract()

        for text in text_with_room_keyword_list:
            room_nr = int(self.extract_number(text))
            if(room_nr >= 1):
                return room_nr

        return room_nr_from_text
