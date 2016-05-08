# -*- coding: utf-8 -*-
import scrapy
from ..items import SquidItem


class YahooApplSpider(scrapy.Spider):
    name = "yahoo.AAPL"
    allowed_domains = ["http://finance.yahoo.com"]
    start_urls = (
        'http://finance.yahoo.com/q/hp?s=AAPL+Historical+Prices/',
    )

    def parse(self, response):
        table = response.xpath('(//th[@class="yfnc_tablehead1"])[1]/parent::*/parent::*')
        datarows = table.xpath('tr/td[1]/parent::*')
        for row in datarows:
            data = row.xpath('td')
            data = [c.xpath('text()').extract()[0] for c in data]
            try:
                item = SquidItem()
                item['date'] = data[0]
                item['open'] = data[1]
                item['high'] = data[2]
                item['low'] = data[3]
                item['close'] = data[4]
                item['volume'] = data[5]
                yield item
            except:
                pass

