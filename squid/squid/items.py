# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HistoryItem(scrapy.Item):
    ticker = scrapy.Field()
    date = scrapy.Field()
    open = scrapy.Field()
    high = scrapy.Field()
    low = scrapy.Field()
    close = scrapy.Field()
    volume = scrapy.Field()


class KeyStatsItem(scrapy.Item):
    ticker = scrapy.Field()
    market_cap_interday = scrapy.Field()
    enterprise_value = scrapy.Field()
    trailing_pe = scrapy.Field()
    # John - make more fields here
    # .
    # .

class AnalystEstimatesItem(scrapy.Item):
    ticker = scrapy.Field()
    earnings_avg_estimate = scrapy.Field()
    earnings_low_estimate = scrapy.Field()
    # John - make more fields here
    # .
    # .
    revenue_avg_estimate = scrapy.Field()
    revenue_low_estimate = scrapy.Field()
    # John - make more fields here
    # .
    # .




