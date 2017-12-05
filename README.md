# polish_real_estate_crawler

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/387f5b501f0b48b8b035dd34e1b22047)](https://www.codacy.com/app/ermanno-pirotta/polish-real-estate-crawler?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ermanno-pirotta/polish-real-estate-crawler&amp;utm_campaign=Badge_Grade)

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
