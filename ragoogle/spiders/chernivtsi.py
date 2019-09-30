# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import CSVFeedSpider

from ragoogle.items.chernivtsi import MbuItem
from ragoogle.loaders import StripJoinItemLoader


class CSVChernivtsiSpider(CSVFeedSpider):
    name = "chernivtsi"
    allowed_domains = ["data.city.cv.ua"]
    start_urls = ["https://data.city.cv.ua/dataset/mistobudumovy"]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["order_no", "order_date", "customer", "obj", "address", "changes", "cancellation",
                               "scan_url", "status"]
    }

    # at first get link to csv file, then call super().parse to proceed with CSV parsing
    def parse(self, response):
        yield Request(
            response.css(
                '#dataset-resources > ul > li:nth-child(1) > div > ul > li:nth-child(2) > a::attr(href)').get(),
            callback=super().parse
        )

    def adapt_response(self, response):
        return response.replace(body=response.body.decode('cp1251').encode('utf-8'), encoding='utf-8')

    def parse_row(self, response, row):
        l = StripJoinItemLoader(item=MbuItem())
        l.add_value("order_no", row['restrictionNumber '])  # space in the end is needed
        l.add_value("order_date", row['restrictionDate'])
        l.add_value("customer", row['objectOwner'])
        l.add_value("obj", row['objectDescription'])
        l.add_value("address", row['objectAddress'])
        l.add_value("changes", row['objectChanges'])
        l.add_value("cancellation", row['objectCancel'])
        l.add_value("status", row['objectStatus'])

        yield l.load_item()
