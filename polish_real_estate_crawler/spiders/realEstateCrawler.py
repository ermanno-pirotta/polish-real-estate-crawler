# -*- coding: utf-8 -*-
import scrapy
import sys
import re
import locale
import geopy.distance

class RealEstateCrawler(scrapy.Spider):
    locale.setlocale(locale.LC_ALL, 'pl_PL')

    def get_poi_coordinates(self):
        poi = self.get_crawl_argument('poi')
        return poi.split(",")

    def get_crawl_argument(self, arg_name):
        argument = getattr(self, arg_name, None)
        if argument is not None:
            return argument
        else:
            print('argument' + arg_name + ' is mandatory')
            sys.exit()

    def extract_number(field):
        field_with_no_spaces = str(field).replace(' ', '')
        match = re.search(r'(\d+,?(\d+)?)+',field_with_no_spaces)
        if match :
            return match.group(0)
        else :
            return '0'

    def extract_size_from_text(self, text):
        match = re.search(r'(?!\d|\\.)*(\d* m²)',text)
        if match :
            return match.group()
        else :
            return '0'

    def extract_from_html_comment(self, label):
        match = re.match(r'<\!--(.*)-->', label)
        return match.group(1)

    def get_distance(self, poi_coordinates, coords):
        poi_latitude = locale.atof(poi_coordinates[0])
        poi_longitude = locale.atof(poi_coordinates[1])

        coords_from = (coords[0], coords[1])
        coords_to = (poi_latitude, poi_longitude)

        return geopy.distance.vincenty(coords_from, coords_to).km
