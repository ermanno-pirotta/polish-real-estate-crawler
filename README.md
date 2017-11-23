# polish_real_estate_crawler

## Overview

This project is a python project, built using the [Scrapy framework](https://scrapy.org/).

## Crawlers
- otodom: crawler for the [otodom](https://www.otodom.pl/) site.

## Usage

Install scrapy, and then run:

scrapy crawl <CRAWLER> -a city="<CITY>" -a zone="<ZONE>" -o <CSV_FILE> -t csv
