# polish_real_estate_crawler

## Overview

This project is a python project, built using the [Scrapy framework](https://scrapy.org/).

## Dependencies

- scrapy
- [geopy](https://pypi.python.org/pypi/geopy)

## Crawlers
- otodom: crawler for the [otodom](https://www.otodom.pl/) site.
- airbnb: crawler for the [airbnb](https://www.airbnb.pl) polish site.

## Usage

Install scrapy, and then run:

scrapy crawl <CRAWLER> [-a type="sprzedaz|wynajem"] -a city="<CITY>" -a zone="<ZONE>" -a poi=<LAT,LON> -o <CSV_FILE> -t csv
