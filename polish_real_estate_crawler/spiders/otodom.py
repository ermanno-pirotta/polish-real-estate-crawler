# -*- coding: utf-8 -*-
import scrapy
import re
import locale
from polish_real_estate_crawler.spiders.realEstateCrawler import RealEstateCrawler

class OtodomSpider(RealEstateCrawler):
    name = 'otodom'
    allowed_domains = ['otodom.pl']

    locale.setlocale(locale.LC_ALL, 'pl_PL')

    def start_requests(self):
        url = 'https://www.otodom.pl/'
        self.mode = self.get_crawl_argument('type')
        self.city = self.get_crawl_argument('city')
        self.zone = self.get_crawl_argument('zone')

        url = url + self.mode + '/mieszkanie/' + self.city + '/' + self.zone

        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        #get all url from main page: response.xpath('//article/@data-url').extract()
        properties_links = response.xpath('//article/@data-url').extract()
        next_page_link = response.css(".pager-next a::attr(href)").extract_first()

        for property_link in properties_links:
            yield response.follow(property_link, self.parse_property_details)

        if next_page_link is not None:
            yield response.follow(next_page_link, callback=self.parse)

    def parse_property_details(self, response):
        price_without_currency = locale.atof(self.extract_number(response.css('.param_price span strong::text').extract_first()))
        size_without_unit = locale.atof(self.extract_number(response.css('.param_m span strong::text').extract_first()))
        floor_nr = response.css('.param_floor_no span strong::text').extract_first(),
        total_nr_of_floors = self.extract_nr_of_floors(response.css('.param_floor_no span::text').extract_first(), floor_nr)
        latitude = locale.atof(response.xpath('//div[@id="adDetailInlineMap"]/@data-lat').extract_first())
        longitude = locale.atof(response.xpath('//div[@id="adDetailInlineMap"]/@data-lon').extract_first())

        yield {
            'zone': self.zone,
            'link': response.xpath('//link[@rel="canonical"]/@href').extract_first(),
            'summary': response.xpath('//header//h1/text()').extract_first(),
            'price': price_without_currency,
            'size': size_without_unit,
            'price/mq': price_without_currency / size_without_unit,
            'monthly_rent': self.extract_details_from_text(response, "Czynsz"),
            'floor_nr' : floor_nr,
            'tot_floor_nr': total_nr_of_floors,
            'room_nr': response.xpath('//li//*[contains(text(), "Liczba pokoi ")]//strong//text()').extract_first(),
            'build_date' : self.extract_details_from_text(response, "Rok budowy"),
            'build_type': self.extract_details_from_text(response, "Rodzaj zabudowy"),
            'window_type': self.extract_details_from_text(response, "Okna"),
            'heating_type': self.extract_details_from_text(response, "Ogrzewanie"),
            'house_condition': self.extract_details_from_text(response, "Stan wykończenia"),
            'form_of_the_property': self.extract_details_from_text(response, "Forma własności"),
            'article_creation_date': response.xpath('//div//*[contains(text(), "Data dodania")]//text()').re(r'Data dodania:(.*)'),
            'article_update_date': response.xpath('//div//*[contains(text(), "Data aktualizacji")]//text()').re(r'Data aktualizacji:(.*)'),
            'additional_info': response.xpath('//*[contains(text(), "Informacje dodatkowe")]/parent::li//li//text()').extract(),
            'latitude':latitude,
            'longitude':longitude,
            'distance_from_poi': self.get_distance(self.poi, [latitude, longitude])
        }

    def extract_details_from_text(self, response, label):
        xpath_expression = '//li//*[contains(text(), "' + label + '")]/parent::li//text()'
        results = response.xpath(xpath_expression).extract()
        if (len(results) == 2):
            return results[1]
        else:
            return ''

    def extract_nr_of_floors(self, field, floor_nr):
        match = re.search(r'.*(\d+)+',field)
        if match :
            return match.group(1)
        else :
            return floor_nr
