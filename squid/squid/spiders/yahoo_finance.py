# -*- coding: utf-8 -*-
import scrapy

from ..items import HistoryItem, KeyStatsItem, AnalystEstimatesItem

TICKERS = 'CSCO AAPL'

HP = 'http://finance.yahoo.com/q/hp?s={ticker}+Historical+Prices'
KS = 'http://finance.yahoo.com/q/ks?s={ticker}+Key+Statistics'
AE = 'http://finance.yahoo.com/q/ae?s={ticker}+Analyst+Estimates'


class YahooApplSpider(scrapy.Spider):
    name = "yahoo.hist"
    allowed_domains = ["http://finance.yahoo.com"]

    def start_requests(self):
        for t in sorted(TICKERS.split()):
            yield scrapy.Request(url=HP.format(ticker=t),
                                 callback=self.parse_history,
                                 meta={'ticker': t})
            yield scrapy.Request(url=KS.format(ticker=t),
                                 callback=self.parse_key_statistics,
                                 meta={'ticker': t})
            yield scrapy.Request(url=AE.format(ticker=t),
                                 callback=self.parse_ae,
                                 meta={'ticker': t})

    def parse_history(self, response):
        table = response.xpath(
            '(//th[@class="yfnc_tablehead1"])[1]/parent::*/parent::*')
        datarows = table.xpath('tr/td[1]/parent::*')
        for row in datarows:
            data = row.xpath('td')
            data = [c.xpath('text()').extract()[0] for c in data]
            # import pdb; pdb.set_trace()
            try:
                item = HistoryItem()
                item['ticker'] = response.request.meta['ticker']
                item['date'] = data[0]
                item['open'] = data[1]
                item['high'] = data[2]
                item['low'] = data[3]
                item['close'] = data[4]
                item['volume'] = data[5]
                yield item
            except:
                pass

    def parse_key_statistics(self, response):
        def unpack(title_starts):
            return response.xpath(
                'string(//text()['
                'contains(., "{title_starts}")'
                ']/parent::*/parent::*/td'
                '[@class="yfnc_tabledata1"])'.
                    format(title_starts=title_starts)).extract()[0]
        try:
            item = KeyStatsItem()
            item['ticker'] = response.request.meta['ticker']
            item['market_cap_interday'] = unpack('Market Cap (intraday')
            item['enterprise_value'] = unpack('Enterprise Value (')
            # John - make more assignments here
            # .
            # .
            yield item
        except:
            pass

    def parse_ae(self, response):
        def unpack(table_title_starts, row_title_starts):
            table = response.xpath(
                '//text()[contains(., "{table_title_starts}")]'
                '/parent::*/parent::*/parent::*/parent::*'.format(
                    table_title_starts=table_title_starts))
            row = table.xpath(
                './/text()[contains(., "{row_title_starts}")]'
                '/parent::*/parent::*'.format(
                    row_title_starts=row_title_starts))
            dat = row.xpath('td[@class="yfnc_tabledata1"]')
            return ' '.join([q.xpath('string()').extract()[0] for q in dat])

        try:
            item = AnalystEstimatesItem()
            item['ticker'] = response.request.meta['ticker']
            item['earnings_avg_estimate'] = unpack('Earnings Est', 'Avg. Estimate')
            item['earnings_low_estimate'] = unpack('Earnings Est', 'Low Estimate')
            # John - make more assignments here
            # .
            # .
            yield item
        except:
            pass
